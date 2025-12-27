"""
WhiskerNotes - Custom Exceptions
Application-specific exceptions
"""


class WhiskerNotesError(Exception):
    """Base exception for WhiskerNotes"""
    pass


class ValidationError(WhiskerNotesError):
    """Raised when validation fails"""
    pass


class NoteNotFoundError(WhiskerNotesError):
    """Raised when a note is not found"""
    pass


class DatabaseError(WhiskerNotesError):
    """Raised when a database operation fails"""
    pass

