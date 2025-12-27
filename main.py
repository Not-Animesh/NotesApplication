"""
WhiskerNotes - Main Application Entry Point
A cozy cat-themed notes application with Python backend
Enhanced architecture with service layer
"""

import customtkinter as ctk
from database import Database
from repository.note_repository import NoteRepository
from services.note_service import NoteService
from services.config_service import ConfigService
from themes import Theme, CAT_MESSAGES
from ui.home import HomeScreen
from ui.editor import EditorScreen
from utils.exceptions import ValidationError, NoteNotFoundError
import os


class WhiskerNotes(ctk.CTk):
    """Main application class for WhiskerNotes"""
    
    def __init__(self):
        """Initialize the application"""
        super().__init__()
        
        # Load configuration
        self.config = ConfigService()
        
        # Window configuration
        self.title("WhiskerNotes 🐱")
        width = self.config.get_setting("window_width", 900)
        height = self.config.get_setting("window_height", 700)
        self.geometry(f"{width}x{height}")
        self.minsize(800, 600)
        
        # Set window icon
        icon_path = Theme.get_asset_path("app_icon.png")
        if icon_path and os.path.exists(icon_path):
            try:
                self.iconphoto(True, ctk.CTkImage(light_image=self._load_image(icon_path)))
            except:
                pass  # Fallback if icon loading fails
        
        # Initialize architecture layers
        self.db = Database()
        self.repository = NoteRepository(self.db)
        self.note_service = NoteService(self.repository)
        
        # Set to light mode only
        ctk.set_appearance_mode("light")
        colors = Theme.get_colors()
        
        # Setup background image first (before other widgets)
        self._setup_background()
        
        # Set window background to blend with lavender gradient
        # Using a very light lavender that allows background image to show through
        self.configure(fg_color="#F5F0FF")
        
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Initialize screens
        self.home_screen = None
        self.editor_screen = None
        
        # Show home screen
        self.show_home_screen()
    
    def _load_image(self, path):
        """Load image from path"""
        from PIL import Image
        return Image.open(path)
    
    def _setup_background(self):
        """Setup background image for the entire application window"""
        try:
            from PIL import Image, ImageTk
            import tkinter as tk
            
            bg_path = Theme.get_background_image()
            if bg_path and os.path.exists(bg_path):
                # Load background image
                self.bg_image_original = Image.open(bg_path)
                
                # Create a canvas widget that fills the entire window
                self.bg_canvas = tk.Canvas(
                    self, 
                    highlightthickness=0, 
                    bd=0,
                    bg="#FAF8F3"  # Fallback color matching theme
                )
                # Place canvas to fill entire window
                self.bg_canvas.place(x=0, y=0, relwidth=1, relheight=1)
                
                # Function to update background image size on window resize
                def update_bg(event=None):
                    try:
                        if hasattr(self, 'bg_canvas') and hasattr(self, 'bg_image_original'):
                            width = self.winfo_width()
                            height = self.winfo_height()
                            if width > 1 and height > 1:
                                # Resize image to match window size
                                resized = self.bg_image_original.resize(
                                    (width, height), 
                                    Image.Resampling.LANCZOS
                                )
                                # Convert to PhotoImage
                                self.bg_photo = ImageTk.PhotoImage(resized)
                                # Clear canvas and add new image
                                self.bg_canvas.delete("all")
                                self.bg_canvas.create_image(
                                    0, 0, 
                                    anchor="nw", 
                                    image=self.bg_photo
                                )
                    except Exception:
                        pass
                
                # Bind window resize event
                self.bind("<Configure>", update_bg)
                
                # Initial background setup after window is ready
                self.after(100, update_bg)
                
                # Store reference to prevent garbage collection
                self.background_image_path = bg_path
            else:
                self.background_image_path = None
        except Exception as e:
            # Fallback if background loading fails
            self.background_image_path = None
            pass
    
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
                on_toggle_pin=self.toggle_pin,
                note_service=self.note_service
            )
        
        colors = Theme.get_colors()
        # Configure home screen to blend with background image
        self.home_screen.configure(fg_color="#F5F0FF")
        self.home_screen.grid(row=0, column=0, sticky="nsew")
        
        # Background canvas is placed first, so it stays behind other widgets automatically
        
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
        # Configure editor screen to blend with background
        self.editor_screen.configure(fg_color="#F5F0FF")
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
        try:
            note = self.note_service.get_note(note_id)
            if note:
                self.show_editor_screen(note=note)
            else:
                self._show_error("Note not found")
        except Exception as e:
            self._show_error(f"Error loading note: {str(e)}")
    
    def save_note(self, title: str, content: str, note_id: int = None, tags: str = "", category: str = "Personal"):
        """
        Save a note (create or update)
        
        Args:
            title: Note title
            content: Note content
            note_id: ID of existing note, or None for new note
            tags: Comma-separated tags
            category: Note category
        """
        try:
            if note_id:
                # Update existing note
                self.note_service.update_note(note_id, title, content, tags, category)
            else:
                # Create new note
                new_id = self.note_service.create_note(title, content, tags, category)
                # Update editor with new note ID
                if self.editor_screen:
                    self.editor_screen.current_note_id = new_id
        except ValidationError as e:
            self._show_error(f"Validation error: {str(e)}")
        except Exception as e:
            self._show_error(f"Error saving note: {str(e)}")
    
    def delete_note(self, note_id: int):
        """
        Delete a note
        
        Args:
            note_id: ID of the note to delete
        """
        try:
            self.note_service.delete_note(note_id)
            self.refresh_notes()
            if self.home_screen:
                self.home_screen.show_status(CAT_MESSAGES["note_deleted"])
        except NoteNotFoundError:
            self._show_error("Note not found")
        except Exception as e:
            self._show_error(f"Error deleting note: {str(e)}")
    
    def toggle_pin(self, note_id: int):
        """
        Toggle pin status of a note
        
        Args:
            note_id: ID of the note to pin/unpin
        """
        try:
            self.note_service.toggle_pin(note_id)
            self.refresh_notes()
            if self.home_screen:
                # Get current pin status to show appropriate message
                note = self.note_service.get_note(note_id)
                if note and note.get("is_pinned"):
                    self.home_screen.show_status(CAT_MESSAGES["note_pinned"])
                else:
                    self.home_screen.show_status(CAT_MESSAGES["note_unpinned"])
        except NoteNotFoundError:
            self._show_error("Note not found")
        except Exception as e:
            self._show_error(f"Error toggling pin: {str(e)}")
    
    def refresh_notes(self, sort_by: str = "updated"):
        """
        Refresh the notes display
        
        Args:
            sort_by: Sort method - 'updated', 'alphabetical', or 'pinned'
        """
        if self.home_screen:
            try:
                notes = self.note_service.get_all_notes(sort_by=sort_by)
                self.home_screen.display_notes(notes)
            except Exception as e:
                self._show_error(f"Error loading notes: {str(e)}")
    
    def _show_error(self, message: str):
        """Show error message"""
        if self.home_screen:
            self.home_screen.show_status(f"😿 {message}")
        elif self.editor_screen:
            self.editor_screen.show_status(f"😿 {message}")
    


def main():
    """Main entry point"""
    app = WhiskerNotes()
    app.mainloop()


if __name__ == "__main__":
    main()
