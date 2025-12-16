"""
WhiskerNotes - Database Management
Handles SQLite database operations for note persistence
"""

import sqlite3
import os
from datetime import datetime
from typing import List, Dict, Optional


class Database:
    """SQLite database manager for WhiskerNotes"""
    
    def __init__(self, db_path: str = "whiskernotes.db"):
        """Initialize database connection"""
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Create notes table if it doesn't exist"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        conn.close()
    
    def create_note(self, title: str, content: str) -> int:
        """
        Create a new note
        
        Args:
            title: Note title
            content: Note content
            
        Returns:
            ID of the created note
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO notes (title, content) VALUES (?, ?)",
            (title, content)
        )
        
        note_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return note_id
    
    def get_all_notes(self) -> List[Dict]:
        """
        Get all notes from database
        
        Returns:
            List of note dictionaries
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT * FROM notes ORDER BY updated_at DESC"
        )
        
        rows = cursor.fetchall()
        notes = [dict(row) for row in rows]
        
        conn.close()
        return notes
    
    def get_note(self, note_id: int) -> Optional[Dict]:
        """
        Get a specific note by ID
        
        Args:
            note_id: ID of the note
            
        Returns:
            Note dictionary or None if not found
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM notes WHERE id = ?", (note_id,))
        row = cursor.fetchone()
        
        note = dict(row) if row else None
        conn.close()
        
        return note
    
    def update_note(self, note_id: int, title: str, content: str) -> bool:
        """
        Update an existing note
        
        Args:
            note_id: ID of the note
            title: New title
            content: New content
            
        Returns:
            True if updated successfully
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            """UPDATE notes 
               SET title = ?, content = ?, updated_at = CURRENT_TIMESTAMP 
               WHERE id = ?""",
            (title, content, note_id)
        )
        
        updated = cursor.rowcount > 0
        conn.commit()
        conn.close()
        
        return updated
    
    def delete_note(self, note_id: int) -> bool:
        """
        Delete a note
        
        Args:
            note_id: ID of the note
            
        Returns:
            True if deleted successfully
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM notes WHERE id = ?", (note_id,))
        
        deleted = cursor.rowcount > 0
        conn.commit()
        conn.close()
        
        return deleted
    
    def search_notes(self, query: str) -> List[Dict]:
        """
        Search notes by title or content
        
        Args:
            query: Search query
            
        Returns:
            List of matching notes
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        search_pattern = f"%{query}%"
        cursor.execute(
            """SELECT * FROM notes 
               WHERE title LIKE ? OR content LIKE ? 
               ORDER BY updated_at DESC""",
            (search_pattern, search_pattern)
        )
        
        rows = cursor.fetchall()
        notes = [dict(row) for row in rows]
        
        conn.close()
        return notes
