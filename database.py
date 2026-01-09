from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()

db_url = os.getenv("DATABASE_URL")
if not db_url:
	raise ValueError("DATABASE_URL environment variable is not set")
print(f"Database URL: {db_url}")
engine = create_engine(db_url, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()


def check_db_connection():
	try:
		with engine.connect() as connection:
			result = connection.execute(text("SELECT 1"))
			return True, "Database connection successful!"
	except Exception as e:
		return False, f"Database connection failed: {str(e)}"

