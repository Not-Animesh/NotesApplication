"""
WhiskerNotes - Note Repository
Data access layer for note operations
"""

from typing import List, Dict, Optional
from database import Database


class NoteRepository:
    """Repository for note data access"""
    
    def __init__(self, database: Database):
        """
        Initialize note repository
        
        Args:
            database: Database instance
        """
        self.db = database
    
    def create(self, title: str, content: str, tags: str = "", category: str = "Personal") -> int:
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
        return self.db.create_note(title, content, tags, category)
    
    def get_by_id(self, note_id: int) -> Optional[Dict]:
        """
        Get a note by ID
        
        Args:
            note_id: ID of the note
            
        Returns:
            Note dictionary or None if not found
        """
        return self.db.get_note(note_id)
    
    def get_all(self, sort_by: str = "updated") -> List[Dict]:
        """
        Get all notes
        
        Args:
            sort_by: Sort method
            
        Returns:
            List of note dictionaries
        """
        return self.db.get_all_notes(sort_by)
    
    def update(self, note_id: int, title: str, content: str, tags: str = "", category: str = "Personal") -> bool:
        """
        Update a note
        
        Args:
            note_id: ID of the note
            title: New title
            content: New content
            tags: Comma-separated tags
            category: Note category
            
        Returns:
            True if updated successfully
        """
        return self.db.update_note(note_id, title, content, tags, category)
    
    def delete(self, note_id: int) -> bool:
        """
        Delete a note
        
        Args:
            note_id: ID of the note
            
        Returns:
            True if deleted successfully
        """
        return self.db.delete_note(note_id)
    
    def exists(self, note_id: int) -> bool:
        """
        Check if a note exists
        
        Args:
            note_id: ID of the note
            
        Returns:
            True if note exists
        """
        note = self.db.get_note(note_id)
        return note is not None
    
    def search(self, query: str) -> List[Dict]:
        """
        Search notes
        
        Args:
            query: Search query
            
        Returns:
            List of matching notes
        """
        return self.db.search_notes(query)
    
    def toggle_pin(self, note_id: int) -> bool:
        """
        Toggle pin status
        
        Args:
            note_id: ID of the note
            
        Returns:
            True if toggled successfully
        """
        return self.db.toggle_pin(note_id)
    
    def get_by_category(self, category: str) -> List[Dict]:
        """
        Get notes by category
        
        Args:
            category: Category to filter by
            
        Returns:
            List of notes in the category
        """
        return self.db.get_notes_by_category(category)
    
    def get_by_tag(self, tag: str) -> List[Dict]:
        """
        Get notes by tag
        
        Args:
            tag: Tag to filter by
            
        Returns:
            List of notes with the tag
        """
        return self.db.get_notes_by_tag(tag)

