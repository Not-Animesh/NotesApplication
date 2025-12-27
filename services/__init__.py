"""
WhiskerNotes - Services Package
Business logic layer for the application
"""

from .note_service import NoteService
from .config_service import ConfigService

__all__ = ['NoteService', 'ConfigService']

