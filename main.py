"""
WhiskerNotes - Main Application Entry Point
A cozy cat-themed notes application with Python backend
"""

import customtkinter as ctk
from database import Database
from themes import Theme, CAT_MESSAGES
from ui.home import HomeScreen
from ui.editor import EditorScreen


class WhiskerNotes(ctk.CTk):
    """Main application class for WhiskerNotes"""
    
    def __init__(self):
        """Initialize the application"""
        super().__init__()
        
        # Window configuration
        self.title("WhiskerNotes 🐱")
        self.geometry("900x700")
        self.minsize(800, 600)
        
        # Initialize database
        self.db = Database()
        
        # Set theme
        ctk.set_appearance_mode("light")
        colors = Theme.get_colors()
        self.configure(fg_color=colors["bg"])
        
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Initialize screens
        self.home_screen = None
        self.editor_screen = None
        
        # Show home screen
        self.show_home_screen()
    
    def show_home_screen(self):
        """Display the home screen"""
        # Hide editor if visible
        if self.editor_screen:
            self.editor_screen.grid_forget()
        
        # Create or show home screen
        if not self.home_screen:
            self.home_screen = HomeScreen(
                self,
                on_create_note=self.create_note,
                on_edit_note=self.edit_note,
                on_delete_note=self.delete_note,
                on_toggle_theme=self.toggle_theme
            )
        
        colors = Theme.get_colors()
        self.home_screen.configure(fg_color=colors["bg"])
        self.home_screen.grid(row=0, column=0, sticky="nsew")
        
        # Load and display notes
        self.refresh_notes()
    
    def show_editor_screen(self, note=None):
        """
        Display the editor screen
        
        Args:
            note: Note to edit, or None for new note
        """
        # Hide home screen
        if self.home_screen:
            self.home_screen.grid_forget()
        
        # Create or show editor screen
        if not self.editor_screen:
            self.editor_screen = EditorScreen(
                self,
                on_save=self.save_note,
                on_back=self.show_home_screen
            )
        
        colors = Theme.get_colors()
        self.editor_screen.configure(fg_color=colors["bg"])
        self.editor_screen.grid(row=0, column=0, sticky="nsew")
        
        # Load note data
        self.editor_screen.load_note(note)
    
    def create_note(self):
        """Create a new note"""
        self.show_editor_screen(note=None)
    
    def edit_note(self, note_id: int):
        """
        Edit an existing note
        
        Args:
            note_id: ID of the note to edit
        """
        note = self.db.get_note(note_id)
        if note:
            self.show_editor_screen(note=note)
    
    def save_note(self, title: str, content: str, note_id: int = None):
        """
        Save a note (create or update)
        
        Args:
            title: Note title
            content: Note content
            note_id: ID of existing note, or None for new note
        """
        if note_id:
            # Update existing note
            self.db.update_note(note_id, title, content)
        else:
            # Create new note
            new_id = self.db.create_note(title, content)
            # Update editor with new note ID
            if self.editor_screen:
                self.editor_screen.current_note_id = new_id
    
    def delete_note(self, note_id: int):
        """
        Delete a note
        
        Args:
            note_id: ID of the note to delete
        """
        if self.db.delete_note(note_id):
            self.refresh_notes()
            if self.home_screen:
                self.home_screen.show_status(CAT_MESSAGES["note_deleted"])
    
    def refresh_notes(self):
        """Refresh the notes display"""
        if self.home_screen:
            notes = self.db.get_all_notes()
            self.home_screen.display_notes(notes)
    
    def toggle_theme(self):
        """Toggle between light and dark themes"""
        Theme.toggle_theme()
        
        # Update appearance mode
        mode = "dark" if Theme.is_dark() else "light"
        ctk.set_appearance_mode(mode)
        
        # Update window colors
        colors = Theme.get_colors()
        self.configure(fg_color=colors["bg"])
        
        # Update screens
        if self.home_screen:
            self.home_screen.update_colors()
        
        if self.editor_screen:
            self.editor_screen.update_colors()


def main():
    """Main entry point"""
    app = WhiskerNotes()
    app.mainloop()


if __name__ == "__main__":
    main()
