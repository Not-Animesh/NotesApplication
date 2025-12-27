"""
WhiskerNotes - Note Service
Business logic layer for note operations
"""

from typing import List, Dict, Optional
from repository.note_repository import NoteRepository
from utils.validators import NoteValidator
from utils.exceptions import ValidationError, NoteNotFoundError


class NoteService:
    """Service for note business logic"""
    
    def __init__(self, repository: NoteRepository):
        """
        Initialize note service
        
        Args:
            repository: Note repository instance
        """
        self.repository = repository
        self.validator = NoteValidator()
    
    def create_note(self, title: str, content: str, tags: str = "", category: str = "Personal") -> int:
        """
        Create a new note with validation
        
        Args:
            title: Note title
            content: Note content
            tags: Comma-separated tags
            category: Note category
            
        Returns:
            ID of the created note
            
        Raises:
            ValidationError: If validation fails
        """
        # Validate inputs
        self.validator.validate_title(title)
        self.validator.validate_content(content)
        self.validator.validate_category(category)
        
        # Create note
        return self.repository.create(title, content, tags, category)
    
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
            
        Raises:
            ValidationError: If validation fails
            NoteNotFoundError: If note doesn't exist
        """
        # Check if note exists
        if not self.repository.exists(note_id):
            raise NoteNotFoundError(f"Note with ID {note_id} not found")
        
        # Validate inputs
        self.validator.validate_title(title)
        self.validator.validate_content(content)
        self.validator.validate_category(category)
        
        # Update note
        return self.repository.update(note_id, title, content, tags, category)
    
    def delete_note(self, note_id: int) -> bool:
        """
        Delete a note
        
        Args:
            note_id: ID of the note
            
        Returns:
            True if deleted successfully
            
        Raises:
            NoteNotFoundError: If note doesn't exist
        """
        if not self.repository.exists(note_id):
            raise NoteNotFoundError(f"Note with ID {note_id} not found")
        
        return self.repository.delete(note_id)
    
    def get_note(self, note_id: int) -> Optional[Dict]:
        """
        Get a note by ID
        
        Args:
            note_id: ID of the note
            
        Returns:
            Note dictionary or None if not found
        """
        return self.repository.get_by_id(note_id)
    
    def get_all_notes(self, sort_by: str = "updated") -> List[Dict]:
        """
        Get all notes
        
        Args:
            sort_by: Sort method - 'updated', 'alphabetical', or 'pinned'
            
        Returns:
            List of note dictionaries
        """
        return self.repository.get_all(sort_by)
    
    def search_notes(self, query: str) -> List[Dict]:
        """
        Search notes
        
        Args:
            query: Search query
            
        Returns:
            List of matching notes
        """
        if not query or not query.strip():
            return self.get_all_notes()
        
        return self.repository.search(query.strip())
    
    def toggle_pin(self, note_id: int) -> bool:
        """
        Toggle pin status of a note
        
        Args:
            note_id: ID of the note
            
        Returns:
            True if toggled successfully
            
        Raises:
            NoteNotFoundError: If note doesn't exist
        """
        if not self.repository.exists(note_id):
            raise NoteNotFoundError(f"Note with ID {note_id} not found")
        
        return self.repository.toggle_pin(note_id)
    
    def get_notes_by_category(self, category: str) -> List[Dict]:
        """
        Get notes by category
        
        Args:
            category: Category to filter by
            
        Returns:
            List of notes in the category
        """
        return self.repository.get_by_category(category)
    
    def get_notes_by_tag(self, tag: str) -> List[Dict]:
        """
        Get notes by tag
        
        Args:
            tag: Tag to filter by
            
        Returns:
            List of notes with the tag
        """
        return self.repository.get_by_tag(tag)

