from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import get_db, check_db_connection, engine
from models import Base, User, Notes, NoteVersion
from auth import create_access_token, get_current_user, hash_password, verify_password
from schemas import UserRegister, UserLogin, UserResponse, Token, NoteCreate, NoteUpdate, NoteResponse, VersionResponse
from datetime import timedelta
import os
from dotenv import load_dotenv
from typing import List
load_dotenv()

app = FastAPI()

# CORS middleware - configurable for prod via ALLOWED_ORIGINS (comma-separated)
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000")
origins_list = [origin.strip() for origin in allowed_origins.split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins_list,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

access_token_time = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
print(f"Access token expiry time: {access_token_time} minutes")
@app.get("/")
def greet():
    return {"message": "Server is up and running!"}

@app.get("/health")
def health_check():
    """Check if API and database are working"""
    is_connected, message = check_db_connection()
    return {
        "status": "healthy" if is_connected else "unhealthy",
        "database": message
    }

@app.post("/register", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def register_user(user_data: UserRegister, db: Session = Depends(get_db)):

    db_user = db.query(User).filter(User.email == user_data.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = User(username=user_data.username, email=user_data.email, password_hash=hash_password(user_data.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/login", status_code=status.HTTP_200_OK, response_model=Token)
def login_user(user_data: UserLogin, db: Session = Depends(get_db)):
    
    db_user = db.query(User).filter(User.email == user_data.email).first()
    if not db_user or not verify_password(user_data.password, str(db_user.password_hash)):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    access_token = create_access_token(
        data={"sub": db_user.user_id},
        expires_delta=timedelta(minutes=30),
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/note", response_model=List[NoteResponse])
def get_all_notes(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    notes = db.query(Notes).filter(Notes.owner_id == current_user.user_id).all()
    return notes

@app.post("/note", status_code=status.HTTP_201_CREATED, response_model=NoteResponse)
def create_note(note_data: NoteCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    new_note = Notes(title=note_data.title, content=note_data.content, owner_id=current_user.user_id)
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note   


@app.put("/note/{note_id}", status_code=status.HTTP_200_OK, response_model=NoteResponse)
def update_note(
    note_id: str,
    note_data: NoteUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    note = (
        db.query(Notes)
        .filter(
            Notes.id == note_id,
            Notes.owner_id == current_user.user_id
        )
        .first()
    )

    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    # Get latest version number for this note
    last_version = db.query(NoteVersion).filter(NoteVersion.note_id == note_id).order_by(NoteVersion.version_number.desc()).first()
    next_version = 1 if not last_version else last_version.version_number + 1

    # Save current note as a version before updating
    version = NoteVersion(
        note_id=note_id,
        version_number=next_version,
        content_snapshot=note.content,
        editor_id=current_user.user_id,
    )
    db.add(version)
    db.commit()

    note.title = note_data.title #type: ignore
    note.content = note_data.content #type: ignore

    db.commit()
    db.refresh(note)

    return note


@app.delete("/note/{note_id}", status_code=status.HTTP_200_OK)
def delete_note(
    note_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    note = (
        db.query(Notes)
        .filter(
            Notes.id == note_id,
            Notes.owner_id == current_user.user_id
        )
        .first()
    )

    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    # Delete all versions linked to this note first to satisfy FK constraints
    db.query(NoteVersion).filter(NoteVersion.note_id == note_id).delete()

    db.delete(note)
    db.commit()

    return {"message": "Note deleted successfully"}

@app.post("/note/{note_id}/restore/{version_number}", status_code=status.HTTP_200_OK)
def restore_note_version(note_id: str, version_number: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    note = db.query(Notes).filter(Notes.id == note_id, Notes.owner_id == current_user.user_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    version = db.query(NoteVersion).filter(NoteVersion.note_id == note_id, NoteVersion.version_number == version_number).first()
    if not version:
        raise HTTPException(status_code=404, detail="Version not found")
    
    last_version = db.query(NoteVersion).filter(NoteVersion.note_id == note_id).order_by(NoteVersion.version_number.desc()).first()
    next_version = 1 if not last_version else last_version.version_number + 1
    backup_version = NoteVersion(
        note_id=note_id,
        version_number=next_version,
        content_snapshot=note.content,
        editor_id=current_user.user_id,
    )
    db.add(backup_version)
    db.commit()
    note.content = version.content_snapshot
    db.commit()
    db.refresh(note)
    return {"message": f"Note restored to version {version_number}", "note": note}

@app.get("/note/{note_id}/versions/{version_number}", status_code=status.HTTP_200_OK)
def get_note_version(note_id: str, version_number: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
   
    note = db.query(Notes).filter(Notes.id == note_id, Notes.owner_id == current_user.user_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    version = db.query(NoteVersion).filter(NoteVersion.note_id == note_id, NoteVersion.version_number == version_number).first()

    if not version:
        raise HTTPException(status_code=404, detail="Version not found")
    
    return {"note_id": note_id, "version_number": version_number, "version": version}

@app.get("/note/{note_id}/versions", status_code=status.HTTP_200_OK)
def list_note_versions(note_id: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):

    note = db.query(Notes).filter(Notes.id == note_id, Notes.owner_id == current_user.user_id).first()

    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    versions = db.query(NoteVersion).filter(NoteVersion.note_id == note_id).order_by(NoteVersion.version_number).all()
    
    return {"note_id": note_id, "versions": versions}