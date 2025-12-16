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
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_pinned INTEGER DEFAULT 0,
                tags TEXT DEFAULT '',
                category TEXT DEFAULT 'Personal',
                word_count INTEGER DEFAULT 0
            )
        """)
        
        # Migrate existing tables to add new columns
        self._migrate_database(cursor)
        
        conn.commit()
        conn.close()
    
    def _migrate_database(self, cursor):
        """Add new columns to existing database if they don't exist"""
        # Get existing columns
        cursor.execute("PRAGMA table_info(notes)")
        columns = [column[1] for column in cursor.fetchall()]
        
        # Add missing columns
        if 'is_pinned' not in columns:
            cursor.execute("ALTER TABLE notes ADD COLUMN is_pinned INTEGER DEFAULT 0")
        
        if 'tags' not in columns:
            cursor.execute("ALTER TABLE notes ADD COLUMN tags TEXT DEFAULT ''")
        
        if 'category' not in columns:
            cursor.execute("ALTER TABLE notes ADD COLUMN category TEXT DEFAULT 'Personal'")
        
        if 'word_count' not in columns:
            cursor.execute("ALTER TABLE notes ADD COLUMN word_count INTEGER DEFAULT 0")
    
    def create_note(self, title: str, content: str, tags: str = "", category: str = "Personal") -> int:
        """
        Create a new note
        
        Args:
            title: Note title
            content: Note content
            tags: Comma-separated tags
            category: Note category
            
        Returns:
            ID of the created note
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        word_count = len(content.split())
        
        cursor.execute(
            "INSERT INTO notes (title, content, tags, category, word_count) VALUES (?, ?, ?, ?, ?)",
            (title, content, tags, category, word_count)
        )
        
        note_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return note_id
    
    def get_all_notes(self, sort_by: str = "updated") -> List[Dict]:
        """
        Get all notes from database
        
        Args:
            sort_by: Sort method - 'updated', 'alphabetical', or 'pinned'
        
        Returns:
            List of note dictionaries
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        if sort_by == "alphabetical":
            order = "title ASC"
        elif sort_by == "pinned":
            order = "is_pinned DESC, updated_at DESC"
        else:  # default to updated
            order = "is_pinned DESC, updated_at DESC"
        
        cursor.execute(f"SELECT * FROM notes ORDER BY {order}")
        
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
    
    def update_note(self, note_id: int, title: str, content: str, tags: str = "", category: str = "Personal") -> bool:
        """
        Update an existing note
        
        Args:
            note_id: ID of the note
            title: New title
            content: New content
            tags: Comma-separated tags
            category: Note category
            
        Returns:
            True if updated successfully
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        word_count = len(content.split())
        
        cursor.execute(
            """UPDATE notes 
               SET title = ?, content = ?, tags = ?, category = ?, 
                   word_count = ?, updated_at = CURRENT_TIMESTAMP 
               WHERE id = ?""",
            (title, content, tags, category, word_count, note_id)
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
        Search notes by title, content, or tags
        
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
               WHERE title LIKE ? OR content LIKE ? OR tags LIKE ?
               ORDER BY is_pinned DESC, updated_at DESC""",
            (search_pattern, search_pattern, search_pattern)
        )
        
        rows = cursor.fetchall()
        notes = [dict(row) for row in rows]
        
        conn.close()
        return notes
    
    def toggle_pin(self, note_id: int) -> bool:
        """
        Toggle pin status of a note
        
        Args:
            note_id: ID of the note
            
        Returns:
            True if toggled successfully
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get current pin status
        cursor.execute("SELECT is_pinned FROM notes WHERE id = ?", (note_id,))
        row = cursor.fetchone()
        
        if row:
            new_status = 0 if row[0] else 1
            cursor.execute("UPDATE notes SET is_pinned = ? WHERE id = ?", (new_status, note_id))
            conn.commit()
            conn.close()
            return True
        
        conn.close()
        return False
    
    def get_notes_by_category(self, category: str) -> List[Dict]:
        """
        Get notes filtered by category
        
        Args:
            category: Category to filter by
            
        Returns:
            List of notes in the category
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT * FROM notes WHERE category = ? ORDER BY is_pinned DESC, updated_at DESC",
            (category,)
        )
        
        rows = cursor.fetchall()
        notes = [dict(row) for row in rows]
        
        conn.close()
        return notes
    
    def get_notes_by_tag(self, tag: str) -> List[Dict]:
        """
        Get notes filtered by tag
        
        Args:
            tag: Tag to filter by
            
        Returns:
            List of notes with the tag
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        search_pattern = f"%{tag}%"
        cursor.execute(
            "SELECT * FROM notes WHERE tags LIKE ? ORDER BY is_pinned DESC, updated_at DESC",
            (search_pattern,)
        )
        
        rows = cursor.fetchall()
        notes = [dict(row) for row in rows]
        
        conn.close()
        return notes
