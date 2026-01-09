'use client';

import { useEffect, useState } from 'react';
import { useRouter, useParams } from 'next/navigation';
import { useAuth } from '@/contexts/AuthContext';
import { notesAPI } from '@/lib/api';

interface Note {
    id: string;
    title: string;
    content: string;
    created_at: string;
    updated_at: string;
}

interface Version {
    version_id: string;
    version_number: number;
    content_snapshot: string;
    timestamp: string;
}

export default function NoteDetailPage() {
    const params = useParams();
    const noteId = params?.id as string;
    const router = useRouter();
    const { user } = useAuth();

    const [note, setNote] = useState<Note | null>(null);
    const [isEditing, setIsEditing] = useState(false);
    const [title, setTitle] = useState('');
    const [content, setContent] = useState('');
    const [versions, setVersions] = useState<Version[]>([]);
    const [showVersions, setShowVersions] = useState(false);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        if (!user) {
            router.push('/');
        }
    }, [user, router]);

    useEffect(() => {
        if (noteId && user) {
            fetchNote();
        }
    }, [noteId, user]);

    const fetchNote = async () => {
        try {
            const response = await notesAPI.getAll();
            const foundNote = response.data.find((n: Note) => n.id === noteId);
            if (foundNote) {
                setNote(foundNote);
                setTitle(foundNote.title);
                setContent(foundNote.content);
            }
        } catch (error) {
            console.error('Error fetching note:', error);
        } finally {
            setLoading(false);
        }
    };

    const handleUpdate = async () => {
        try {
            await notesAPI.update(noteId, title, content);
            setIsEditing(false);
            fetchNote();
        } catch (error) {
            console.error('Error updating note:', error);
        }
    };

    const fetchVersions = async () => {
        try {
            const response = await notesAPI.getVersions(noteId);
            setVersions(response.data.versions || []);
            setShowVersions(true);
        } catch (error) {
            console.error('Error fetching versions:', error);
        }
    };

    const handleRestoreVersion = async (versionNumber: number) => {
        if (confirm(`Restore to version ${versionNumber}?`)) {
            try {
                await notesAPI.restoreVersion(noteId, versionNumber);
                fetchNote();
                setShowVersions(false);
            } catch (error) {
                console.error('Error restoring version:', error);
            }
        }
    };

    if (loading) {
        return (
            <div className="min-h-screen flex items-center justify-center">
                <div className="text-xl">Loading...</div>
            </div>
        );
    }

    if (!note) {
        return (
            <div className="min-h-screen flex items-center justify-center">
                <div className="text-xl">Note not found</div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-gray-50">
            {/* Header */}
            <header className="bg-white shadow-sm">
                <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center">
                    <button
                        onClick={() => router.push('/dashboard')}
                        className="text-indigo-600 hover:text-indigo-800"
                    >
                        ← Back to Dashboard
                    </button>
                    <div className="flex gap-3">
                        <button
                            onClick={fetchVersions}
                            className="px-4 py-2 text-sm bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300"
                        >
                            Version History
                        </button>
                        {!isEditing ? (
                            <button
                                onClick={() => setIsEditing(true)}
                                className="px-4 py-2 text-sm bg-indigo-600 text-white rounded-lg hover:bg-indigo-700"
                            >
                                Edit
                            </button>
                        ) : (
                            <>
                                <button
                                    onClick={handleUpdate}
                                    className="px-4 py-2 text-sm bg-green-600 text-white rounded-lg hover:bg-green-700"
                                >
                                    Save
                                </button>
                                <button
                                    onClick={() => {
                                        setIsEditing(false);
                                        setTitle(note.title);
                                        setContent(note.content);
                                    }}
                                    className="px-4 py-2 text-sm bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300"
                                >
                                    Cancel
                                </button>
                            </>
                        )}
                    </div>
                </div>
            </header>

            <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                <div className="bg-white rounded-lg shadow p-8">
                    {isEditing ? (
                        <>
                            <input
                                type="text"
                                value={title}
                                onChange={(e) => setTitle(e.target.value)}
                                className="w-full text-gray-700 text-3xl font-bold mb-4 border-b-2 border-gray-300 focus:border-indigo-500 outline-none pb-2"
                            />
                            <textarea
                                value={content}
                                onChange={(e) => setContent(e.target.value)}
                                className="w-full text-gray-700 border border-gray-300 rounded-lg p-4 focus:ring-2 focus:ring-indigo-500 outline-none"
                                rows={15}
                            />
                        </>
                    ) : (
                        <>
                            <h1 className="text-3xl font-bold text-gray-900 mb-4">{note.title}</h1>
                            <p className="text-gray-700 whitespace-pre-wrap">{note.content}</p>
                        </>
                    )}
                    <div className="mt-6 text-sm text-gray-500">
                        Last updated: {new Date(note.updated_at).toLocaleString()}
                    </div>
                </div>
            </div>

            {/* Version History Modal */}
            {showVersions && (
                <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4">
                    <div className="bg-white rounded-lg p-6 w-full max-w-2xl max-h-[80vh] overflow-y-auto">
                        <h2 className="text-xl font-bold mb-4">Version History</h2>
                        {versions.length === 0 ? (
                            <p className="text-gray-500">No version history available</p>
                        ) : (
                            <div className="space-y-3">
                                {versions.map((version) => (
                                    <div key={version.version_id} className="border border-gray-200 rounded-lg p-4">
                                        <div className="flex justify-between items-start mb-2">
                                            <div>
                                                <span className="font-semibold">Version {version.version_number}</span>
                                                <span className="text-sm text-gray-500 ml-3">
                                                    {new Date(version.timestamp).toLocaleString()}
                                                </span>
                                            </div>
                                            <button
                                                onClick={() => handleRestoreVersion(version.version_number)}
                                                className="text-sm text-indigo-600 hover:text-indigo-800"
                                            >
                                                Restore
                                            </button>
                                        </div>
                                        <p className="text-gray-600 text-sm line-clamp-2">
                                            {version.content_snapshot}
                                        </p>
                                    </div>
                                ))}
                            </div>
                        )}
                        <button
                            onClick={() => setShowVersions(false)}
                            className="mt-4 w-full bg-gray-200 text-gray-700 py-2 rounded-lg hover:bg-gray-300"
                        >
                            Close
                        </button>
                    </div>
                </div>
            )}
        </div>
    );
}
