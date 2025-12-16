"""
WhiskerNotes - Editor Screen UI
Note editor with auto-save functionality
"""

import customtkinter as ctk
from typing import Callable, Optional, Dict
from themes import Theme, CAT_MESSAGES


class EditorScreen(ctk.CTkFrame):
    """Note editor screen"""
    
    def __init__(self, parent, on_save: Callable, on_back: Callable):
        """
        Initialize editor screen
        
        Args:
            parent: Parent widget
            on_save: Callback for saving note (receives title, content, note_id)
            on_back: Callback for going back to home
        """
        super().__init__(parent)
        
        self.on_save = on_save
        self.on_back = on_back
        self.current_note_id = None
        self.auto_save_job = None
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the editor UI"""
        colors = Theme.get_colors()
        
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
        # Header frame
        header_frame = ctk.CTkFrame(self, fg_color=colors["bg"], corner_radius=0)
        header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
        header_frame.grid_columnconfigure(1, weight=1)
        
        # Back button
        self.back_button = ctk.CTkButton(
            header_frame,
            text="← Back",
            width=100,
            height=40,
            corner_radius=20,
            fg_color=colors["button_bg"],
            text_color=colors["button_fg"],
            hover_color=colors["card_hover"],
            font=ctk.CTkFont(size=14),
            command=self.on_back
        )
        self.back_button.grid(row=0, column=0, sticky="w")
        
        # Save button
        self.save_button = ctk.CTkButton(
            header_frame,
            text="💾 Save",
            width=100,
            height=40,
            corner_radius=20,
            fg_color=colors["button_bg"],
            text_color=colors["button_fg"],
            hover_color=colors["card_hover"],
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self.save_note
        )
        self.save_button.grid(row=0, column=2, sticky="e")
        
        # Title entry
        self.title_entry = ctk.CTkEntry(
            self,
            placeholder_text="🐱 Note Title...",
            height=50,
            corner_radius=15,
            border_width=2,
            border_color=colors["border"],
            fg_color=colors["card_bg"],
            text_color=colors["fg"],
            font=ctk.CTkFont(size=18, weight="bold")
        )
        self.title_entry.grid(row=1, column=0, sticky="ew", padx=20, pady=10)
        self.title_entry.bind("<KeyRelease>", self.schedule_auto_save)
        
        # Content text box
        self.content_text = ctk.CTkTextbox(
            self,
            corner_radius=15,
            border_width=2,
            border_color=colors["border"],
            fg_color=colors["card_bg"],
            text_color=colors["fg"],
            font=ctk.CTkFont(size=14),
            wrap="word"
        )
        self.content_text.grid(row=2, column=0, sticky="nsew", padx=20, pady=10)
        self.content_text.bind("<KeyRelease>", self.schedule_auto_save)
        
        # Status label
        self.status_label = ctk.CTkLabel(
            self,
            text="",
            font=ctk.CTkFont(size=12),
            text_color=colors["accent"]
        )
        self.status_label.grid(row=3, column=0, sticky="ew", padx=20, pady=(0, 20))
    
    def update_colors(self):
        """Update colors when theme changes"""
        colors = Theme.get_colors()
        
        self.configure(fg_color=colors["bg"])
        
        self.back_button.configure(
            fg_color=colors["button_bg"],
            text_color=colors["button_fg"],
            hover_color=colors["card_hover"]
        )
        
        self.save_button.configure(
            fg_color=colors["button_bg"],
            text_color=colors["button_fg"],
            hover_color=colors["card_hover"]
        )
        
        self.title_entry.configure(
            border_color=colors["border"],
            fg_color=colors["card_bg"],
            text_color=colors["fg"]
        )
        
        self.content_text.configure(
            border_color=colors["border"],
            fg_color=colors["card_bg"],
            text_color=colors["fg"]
        )
        
        self.status_label.configure(text_color=colors["accent"])
    
    def load_note(self, note: Optional[Dict] = None):
        """
        Load a note into the editor
        
        Args:
            note: Note dictionary or None for new note
        """
        if note:
            self.current_note_id = note["id"]
            self.title_entry.delete(0, "end")
            self.title_entry.insert(0, note["title"])
            self.content_text.delete("1.0", "end")
            self.content_text.insert("1.0", note["content"])
        else:
            self.current_note_id = None
            self.title_entry.delete(0, "end")
            self.content_text.delete("1.0", "end")
    
    def save_note(self):
        """Save the current note"""
        title = self.title_entry.get().strip()
        content = self.content_text.get("1.0", "end").strip()
        
        if not title:
            title = "Untitled Note"
        
        if not content:
            self.show_status("Cannot save empty note 😿")
            return
        
        self.on_save(title, content, self.current_note_id)
        self.show_status(CAT_MESSAGES["note_saved"])
    
    def schedule_auto_save(self, event=None):
        """Schedule auto-save after typing stops"""
        # Cancel previous auto-save job
        if self.auto_save_job:
            self.after_cancel(self.auto_save_job)
        
        # Schedule new auto-save after 2 seconds of inactivity
        self.auto_save_job = self.after(2000, self.auto_save)
    
    def auto_save(self):
        """Auto-save the note"""
        title = self.title_entry.get().strip()
        content = self.content_text.get("1.0", "end").strip()
        
        # Only auto-save if we have content and this is an existing note
        if content and self.current_note_id:
            if not title:
                title = "Untitled Note"
            self.on_save(title, content, self.current_note_id)
            self.show_status(CAT_MESSAGES["auto_saved"], duration=1500)
    
    def show_status(self, message: str, duration: int = 3000):
        """
        Show status message
        
        Args:
            message: Status message to display
            duration: How long to show the message in milliseconds
        """
        self.status_label.configure(text=message)
        # Auto-hide after duration
        self.after(duration, lambda: self.status_label.configure(text=""))
