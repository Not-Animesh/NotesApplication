"""
WhiskerNotes - Home Screen UI
Dashboard displaying note cards with create, edit, delete functionality
"""

import customtkinter as ctk
from typing import Callable, List, Dict
from themes import Theme, CAT_MESSAGES


class HomeScreen(ctk.CTkFrame):
    """Home screen with note cards display"""
    
    def __init__(self, parent, on_create_note: Callable, on_edit_note: Callable, 
                 on_delete_note: Callable, on_toggle_theme: Callable):
        """
        Initialize home screen
        
        Args:
            parent: Parent widget
            on_create_note: Callback for creating a note
            on_edit_note: Callback for editing a note (receives note_id)
            on_delete_note: Callback for deleting a note (receives note_id)
            on_toggle_theme: Callback for toggling theme
        """
        super().__init__(parent)
        
        self.on_create_note = on_create_note
        self.on_edit_note = on_edit_note
        self.on_delete_note = on_delete_note
        self.on_toggle_theme = on_toggle_theme
        
        self.notes = []
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the home screen UI"""
        colors = Theme.get_colors()
        
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Header frame
        header_frame = ctk.CTkFrame(self, fg_color=colors["bg"], corner_radius=0)
        header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
        header_frame.grid_columnconfigure(1, weight=1)
        
        # Title
        title_label = ctk.CTkLabel(
            header_frame,
            text="🐱 WhiskerNotes",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=colors["fg"]
        )
        title_label.grid(row=0, column=0, sticky="w")
        
        # Button container
        button_frame = ctk.CTkFrame(header_frame, fg_color=colors["bg"])
        button_frame.grid(row=0, column=2, sticky="e")
        
        # Theme toggle button
        self.theme_button = ctk.CTkButton(
            button_frame,
            text="🌙" if Theme.current_theme == "light" else "☀️",
            width=40,
            height=40,
            corner_radius=20,
            fg_color=colors["button_bg"],
            text_color=colors["button_fg"],
            hover_color=colors["card_hover"],
            command=self.toggle_theme
        )
        self.theme_button.pack(side="left", padx=5)
        
        # Create note button
        self.create_button = ctk.CTkButton(
            button_frame,
            text="+ New Note",
            width=120,
            height=40,
            corner_radius=20,
            fg_color=colors["button_bg"],
            text_color=colors["button_fg"],
            hover_color=colors["card_hover"],
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self.on_create_note
        )
        self.create_button.pack(side="left", padx=5)
        
        # Scrollable frame for notes
        self.scrollable_frame = ctk.CTkScrollableFrame(
            self,
            fg_color=colors["bg"],
            corner_radius=0
        )
        self.scrollable_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        self.scrollable_frame.grid_columnconfigure(0, weight=1)
        
        # Status message
        self.status_label = ctk.CTkLabel(
            self,
            text="",
            font=ctk.CTkFont(size=12),
            text_color=colors["accent"]
        )
        self.status_label.grid(row=2, column=0, sticky="ew", padx=20, pady=(0, 10))
    
    def toggle_theme(self):
        """Toggle between light and dark themes"""
        self.on_toggle_theme()
        self.update_colors()
    
    def update_colors(self):
        """Update colors when theme changes"""
        colors = Theme.get_colors()
        
        self.configure(fg_color=colors["bg"])
        self.scrollable_frame.configure(fg_color=colors["bg"])
        
        # Update theme button icon
        self.theme_button.configure(
            text="🌙" if Theme.current_theme == "light" else "☀️",
            fg_color=colors["button_bg"],
            text_color=colors["button_fg"],
            hover_color=colors["card_hover"]
        )
        
        self.create_button.configure(
            fg_color=colors["button_bg"],
            text_color=colors["button_fg"],
            hover_color=colors["card_hover"]
        )
        
        self.status_label.configure(text_color=colors["accent"])
        
        # Refresh notes display
        self.display_notes(self.notes)
    
    def display_notes(self, notes: List[Dict]):
        """
        Display notes as cards
        
        Args:
            notes: List of note dictionaries
        """
        self.notes = notes
        colors = Theme.get_colors()
        
        # Clear existing cards
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        if not notes:
            # Empty state
            empty_label = ctk.CTkLabel(
                self.scrollable_frame,
                text=CAT_MESSAGES["no_notes"],
                font=ctk.CTkFont(size=18),
                text_color=colors["fg"]
            )
            empty_label.pack(pady=100)
            return
        
        # Create note cards
        for note in notes:
            self.create_note_card(note)
    
    def create_note_card(self, note: Dict):
        """
        Create a note card widget
        
        Args:
            note: Note dictionary
        """
        colors = Theme.get_colors()
        
        # Card frame
        card = ctk.CTkFrame(
            self.scrollable_frame,
            fg_color=colors["card_bg"],
            corner_radius=15,
            border_width=1,
            border_color=colors["border"]
        )
        card.pack(fill="x", pady=10, padx=5)
        card.grid_columnconfigure(0, weight=1)
        
        # Title
        title = note.get("title", "Untitled")
        title_label = ctk.CTkLabel(
            card,
            text=title if len(title) <= 50 else title[:50] + "...",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=colors["fg"],
            anchor="w"
        )
        title_label.grid(row=0, column=0, sticky="w", padx=15, pady=(15, 5))
        
        # Content preview
        content = note.get("content", "")
        preview = content[:100] + "..." if len(content) > 100 else content
        content_label = ctk.CTkLabel(
            card,
            text=preview,
            font=ctk.CTkFont(size=12),
            text_color=colors["fg"],
            anchor="w",
            justify="left",
            wraplength=600
        )
        content_label.grid(row=1, column=0, sticky="w", padx=15, pady=(0, 10))
        
        # Button frame
        button_frame = ctk.CTkFrame(card, fg_color=colors["card_bg"])
        button_frame.grid(row=0, column=1, rowspan=2, padx=10, pady=10)
        
        # Edit button
        edit_btn = ctk.CTkButton(
            button_frame,
            text="Edit",
            width=70,
            height=30,
            corner_radius=15,
            fg_color=colors["accent"],
            text_color=colors["button_fg"],
            hover_color=colors["card_hover"],
            command=lambda: self.on_edit_note(note["id"])
        )
        edit_btn.pack(side="left", padx=5)
        
        # Delete button
        delete_btn = ctk.CTkButton(
            button_frame,
            text="Delete",
            width=70,
            height=30,
            corner_radius=15,
            fg_color="#FF6B6B",
            text_color="#FFFFFF",
            hover_color="#FF5252",
            command=lambda: self.delete_note_with_confirm(note["id"])
        )
        delete_btn.pack(side="left", padx=5)
        
        # Updated time
        updated_at = note.get("updated_at", "")
        if updated_at:
            time_label = ctk.CTkLabel(
                card,
                text=f"🐾 {updated_at}",
                font=ctk.CTkFont(size=10),
                text_color=colors["accent"]
            )
            time_label.grid(row=2, column=0, sticky="w", padx=15, pady=(0, 10))
    
    def delete_note_with_confirm(self, note_id: int):
        """
        Delete note with confirmation
        
        Args:
            note_id: ID of note to delete
        """
        self.on_delete_note(note_id)
    
    def show_status(self, message: str):
        """
        Show status message
        
        Args:
            message: Status message to display
        """
        self.status_label.configure(text=message)
        # Auto-hide after 3 seconds
        self.after(3000, lambda: self.status_label.configure(text=""))
