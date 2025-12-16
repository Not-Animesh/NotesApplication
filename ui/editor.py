"""
WhiskerNotes - Editor Screen UI
Note editor with auto-save functionality and formatting toolbar
"""

import customtkinter as ctk
from typing import Callable, Optional, Dict
from themes import Theme, CAT_MESSAGES, RANDOM_CAT_MESSAGES
import random
from PIL import Image
import os


class EditorScreen(ctk.CTkFrame):
    """Note editor screen with rich formatting"""
    
    def __init__(self, parent, on_save: Callable, on_back: Callable):
        """
        Initialize editor screen
        
        Args:
            parent: Parent widget
            on_save: Callback for saving note (receives title, content, note_id, tags, category)
            on_back: Callback for going back to home
        """
        super().__init__(parent)
        
        self.on_save = on_save
        self.on_back = on_back
        self.current_note_id = None
        self.current_tags = ""
        self.current_category = "Personal"
        self.auto_save_job = None
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the editor UI"""
        colors = Theme.get_colors()
        
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)
        
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
        
        # Metadata frame (tags and category)
        meta_frame = ctk.CTkFrame(self, fg_color=colors["bg"], corner_radius=0)
        meta_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=(0, 10))
        meta_frame.grid_columnconfigure(0, weight=1)
        
        # Tags entry
        self.tags_entry = ctk.CTkEntry(
            meta_frame,
            placeholder_text="🏷️ Tags (comma-separated, e.g., todo, study, important)",
            height=35,
            corner_radius=15,
            border_width=2,
            border_color=colors["border"],
            fg_color=colors["card_bg"],
            text_color=colors["fg"],
            font=ctk.CTkFont(size=12)
        )
        self.tags_entry.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        
        # Category dropdown
        self.category_var = ctk.StringVar(value="Personal")
        self.category_dropdown = ctk.CTkOptionMenu(
            meta_frame,
            values=[cat.split()[0] for cat in Theme.CATEGORIES],
            variable=self.category_var,
            width=150,
            height=35,
            corner_radius=15,
            fg_color=colors["button_bg"],
            button_color=colors["accent"],
            button_hover_color=colors["card_hover"]
        )
        self.category_dropdown.grid(row=0, column=1)
        
        # Formatting toolbar frame
        toolbar_frame = ctk.CTkFrame(self, fg_color=colors["card_bg"], corner_radius=15)
        toolbar_frame.grid(row=3, column=0, sticky="ew", padx=20, pady=(0, 10))
        
        toolbar_label = ctk.CTkLabel(
            toolbar_frame,
            text="✨ Formatting Toolbar:",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=colors["fg"]
        )
        toolbar_label.pack(side="left", padx=10)
        
        # Bold button
        bold_btn = ctk.CTkButton(
            toolbar_frame,
            text="B",
            width=35,
            height=30,
            corner_radius=10,
            fg_color=colors["accent"],
            font=ctk.CTkFont(size=12, weight="bold"),
            command=lambda: self.insert_format("**", "**")
        )
        bold_btn.pack(side="left", padx=3)
        
        # Italic button
        italic_btn = ctk.CTkButton(
            toolbar_frame,
            text="I",
            width=35,
            height=30,
            corner_radius=10,
            fg_color=colors["accent"],
            font=ctk.CTkFont(size=12, slant="italic"),
            command=lambda: self.insert_format("*", "*")
        )
        italic_btn.pack(side="left", padx=3)
        
        # Underline button
        underline_btn = ctk.CTkButton(
            toolbar_frame,
            text="U",
            width=35,
            height=30,
            corner_radius=10,
            fg_color=colors["accent"],
            font=ctk.CTkFont(size=12, underline=True),
            command=lambda: self.insert_format("__", "__")
        )
        underline_btn.pack(side="left", padx=3)
        
        # Heading button
        heading_btn = ctk.CTkButton(
            toolbar_frame,
            text="H",
            width=35,
            height=30,
            corner_radius=10,
            fg_color=colors["accent"],
            font=ctk.CTkFont(size=14, weight="bold"),
            command=lambda: self.insert_format("## ", "")
        )
        heading_btn.pack(side="left", padx=3)
        
        # Bullet list button
        bullet_btn = ctk.CTkButton(
            toolbar_frame,
            text="•",
            width=35,
            height=30,
            corner_radius=10,
            fg_color=colors["accent"],
            font=ctk.CTkFont(size=16),
            command=lambda: self.insert_format("- ", "")
        )
        bullet_btn.pack(side="left", padx=3)
        
        # Font size dropdown
        font_size_label = ctk.CTkLabel(
            toolbar_frame,
            text="Size:",
            font=ctk.CTkFont(size=10),
            text_color=colors["fg"]
        )
        font_size_label.pack(side="left", padx=(10, 5))
        
        self.font_size_var = ctk.StringVar(value="14")
        font_size_menu = ctk.CTkOptionMenu(
            toolbar_frame,
            values=["12", "14", "16", "18", "20"],
            variable=self.font_size_var,
            width=60,
            height=30,
            corner_radius=10,
            command=self.change_font_size
        )
        font_size_menu.pack(side="left", padx=3)
        
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
        self.content_text.grid(row=4, column=0, sticky="nsew", padx=20, pady=10)
        self.content_text.bind("<KeyRelease>", self.on_content_change)
        
        # Bottom info frame
        bottom_frame = ctk.CTkFrame(self, fg_color=colors["bg"], corner_radius=0)
        bottom_frame.grid(row=5, column=0, sticky="ew", padx=20, pady=(0, 10))
        bottom_frame.grid_columnconfigure(1, weight=1)
        
        # Word count label
        self.word_count_label = ctk.CTkLabel(
            bottom_frame,
            text="📝 Word count: 0",
            font=ctk.CTkFont(size=11),
            text_color=colors["fg"]
        )
        self.word_count_label.grid(row=0, column=0, sticky="w")
        
        # Status label
        self.status_label = ctk.CTkLabel(
            bottom_frame,
            text="",
            font=ctk.CTkFont(size=12),
            text_color=colors["accent"]
        )
        self.status_label.grid(row=0, column=1, sticky="e")
    
    def insert_format(self, prefix: str, suffix: str):
        """Insert formatting around selected text"""
        try:
            # Get selected text
            selected = self.content_text.selection_get()
            # Get selection indices
            start = self.content_text.index("sel.first")
            end = self.content_text.index("sel.last")
            # Replace with formatted text
            self.content_text.delete(start, end)
            self.content_text.insert(start, f"{prefix}{selected}{suffix}")
        except:
            # No selection, insert at cursor
            self.content_text.insert("insert", f"{prefix}{suffix}")
            # Move cursor between markers
            if suffix:
                cursor_pos = self.content_text.index("insert")
                line, col = cursor_pos.split(".")
                new_col = int(col) - len(suffix)
                self.content_text.mark_set("insert", f"{line}.{new_col}")
    
    def change_font_size(self, size: str):
        """Change the font size of the content text"""
        self.content_text.configure(font=ctk.CTkFont(size=int(size)))
    
    def on_content_change(self, event=None):
        """Handle content change - update word count and schedule auto-save"""
        self.update_word_count()
        self.schedule_auto_save(event)
    
    def update_word_count(self):
        """Update the word count display"""
        content = self.content_text.get("1.0", "end").strip()
        word_count = len(content.split()) if content else 0
        self.word_count_label.configure(text=f"📝 Word count: {word_count}")
    
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
            
            # Load tags
            self.current_tags = note.get("tags", "")
            self.tags_entry.delete(0, "end")
            if self.current_tags:
                self.tags_entry.insert(0, self.current_tags)
            
            # Load category
            self.current_category = note.get("category", "Personal")
            self.category_var.set(self.current_category)
            
            # Update word count
            self.update_word_count()
        else:
            self.current_note_id = None
            self.title_entry.delete(0, "end")
            self.content_text.delete("1.0", "end")
            self.tags_entry.delete(0, "end")
            self.category_var.set("Personal")
            self.current_tags = ""
            self.current_category = "Personal"
            self.update_word_count()
    
    def save_note(self):
        """Save the current note"""
        title = self.title_entry.get().strip()
        content = self.content_text.get("1.0", "end").strip()
        tags = self.tags_entry.get().strip()
        category = self.category_var.get()
        
        if not title:
            title = "Untitled Note"
        
        if not content:
            self.show_status("Cannot save empty note 😿")
            return
        
        self.current_tags = tags
        self.current_category = category
        self.on_save(title, content, self.current_note_id, tags, category)
        self.show_status(random.choice(RANDOM_CAT_MESSAGES))
        
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
        tags = self.tags_entry.get().strip()
        category = self.category_var.get()
        
        # Only auto-save if we have content and this is an existing note
        if content and self.current_note_id:
            if not title:
                title = "Untitled Note"
            self.current_tags = tags
            self.current_category = category
            self.on_save(title, content, self.current_note_id, tags, category)
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
