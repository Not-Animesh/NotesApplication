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
import tkinter.messagebox as messagebox


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
        self._is_dirty = False  # track unsaved changes

        self.setup_ui()
    
    def setup_ui(self):
        """Setup the editor UI with enhanced styling"""
        colors = Theme.get_colors()
        spacing = Theme.get_spacing()
        radius = Theme.get_radius()

        # Placeholders for title and tags
        self._title_placeholder = "🐱 Note Title..."
        self._tags_placeholder = "🏷️ Tags (comma-separated, e.g., todo, study, important)"
        self._title_placeholder_active = True
        self._tags_placeholder_active = True
        
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        # Row 3 will be content body, row 4 toolbar at bottom
        self.grid_rowconfigure(3, weight=1)
        
        # Header frame - blend with background
        header_frame = ctk.CTkFrame(self, fg_color="#F5F0FF", corner_radius=0)
        header_frame.grid(row=0, column=0, sticky="ew", padx=spacing["lg"], pady=(spacing["lg"], spacing["md"]))
        header_frame.grid_columnconfigure(1, weight=1)
        
        # Back button with refined styling (with unsaved-changes check)
        self.back_button = ctk.CTkButton(
            header_frame,
            text="← Back",
            width=120,
            height=48,
            corner_radius=radius["lg"],
            fg_color=colors["button_bg"],
            text_color=colors["button_fg"],
            hover_color=colors["button_hover"] if "button_hover" in colors else colors["accent_dark"],
            font=ctk.CTkFont(size=14),
            command=self.handle_back
        )
        self.back_button.grid(row=0, column=0, sticky="w")
        
        # Save button with refined styling
        self.save_button = ctk.CTkButton(
            header_frame,
            text="💾 Save",
            width=120,
            height=48,
            corner_radius=radius["lg"],
            fg_color=colors["accent"],
            text_color=colors["button_fg"],
            hover_color=colors["button_hover"] if "button_hover" in colors else colors["accent_dark"],
            font=ctk.CTkFont(size=15, weight="bold"),
            command=self.save_note
        )
        self.save_button.grid(row=0, column=2, sticky="e")
        
        # Title entry with refined styling (top)
        self.title_entry = ctk.CTkEntry(
            self,
            height=52,
            corner_radius=radius["lg"],
            border_width=2,
            border_color=colors["border"],
            fg_color=colors["card_bg"],
            text_color=colors["fg_secondary"],  # placeholder color by default
            font=ctk.CTkFont(size=19, weight="bold")
        )
        self.title_entry.grid(row=1, column=0, sticky="ew", padx=spacing["lg"], pady=(spacing["md"], spacing["xs"]))
        self.title_entry.insert(0, self._title_placeholder)
        self.title_entry.bind("<FocusIn>", self._on_title_focus_in)
        self.title_entry.bind("<FocusOut>", self._on_title_focus_out)
        self.title_entry.bind("<KeyRelease>", self.on_content_change)

        # Timestamp label directly under title
        self.timestamp_label = ctk.CTkLabel(
            self,
            text="",
            font=ctk.CTkFont(size=12),
            text_color=colors["fg_secondary"]
        )
        self.timestamp_label.grid(row=2, column=0, sticky="w", padx=spacing["lg"], pady=(0, spacing["xs"]))
        
        # Metadata frame (tags and category) with enhanced styling
        meta_frame = ctk.CTkFrame(self, fg_color="#F5F0FF", corner_radius=0)
        meta_frame.grid(row=3, column=0, sticky="ew", padx=spacing["lg"], pady=(0, spacing["xs"]))
        meta_frame.grid_columnconfigure(0, weight=1)
        
        # Tags entry with refined styling
        self.tags_entry = ctk.CTkEntry(
            meta_frame,
            height=42,
            corner_radius=radius["md"],
            border_width=2,
            border_color=colors["border"],
            fg_color=colors["card_bg"],
            text_color=colors["fg_secondary"],  # placeholder color by default
            font=ctk.CTkFont(size=14)
        )
        self.tags_entry.grid(row=0, column=0, sticky="ew", padx=(0, spacing["sm"]))
        self.tags_entry.insert(0, self._tags_placeholder)
        self.tags_entry.bind("<FocusIn>", self._on_tags_focus_in)
        self.tags_entry.bind("<FocusOut>", self._on_tags_focus_out)
        self.tags_entry.bind("<KeyRelease>", self.on_content_change)
        
        # Category dropdown with refined styling
        self.category_var = ctk.StringVar(value="Personal")
        self.category_dropdown = ctk.CTkOptionMenu(
            meta_frame,
            values=[cat.split()[0] for cat in Theme.CATEGORIES],
            variable=self.category_var,
            width=170,
            height=42,
            corner_radius=radius["md"],
            fg_color=colors["button_bg"],
            button_color=colors["accent"],
            button_hover_color=colors["button_hover"] if "button_hover" in colors else colors["accent_dark"],
            font=ctk.CTkFont(size=14)
        )
        self.category_dropdown.grid(row=0, column=1)
        
        # Content text box with enhanced styling (main body)
        self._content_placeholder = "📝 Write your thoughts here... Use the formatting buttons below to add emphasis, headings, or lists."
        self._content_has_placeholder = True
        self.content_text = ctk.CTkTextbox(
            self,
            corner_radius=radius["lg"],
            border_width=2,
            border_color=colors["border"],
            fg_color=colors["card_bg"],
            text_color=colors["fg_secondary"],
            font=ctk.CTkFont(size=15),
            wrap="word"
        )
        self.content_text.grid(row=4, column=0, sticky="nsew", padx=spacing["lg"], pady=spacing["md"])
        # Initialize placeholder text similar to search bar behavior
        self._set_content_placeholder()
        self.content_text.bind("<KeyRelease>", self.on_content_change)
        self.content_text.bind("<FocusIn>", self._on_content_focus_in)
        self.content_text.bind("<FocusOut>", self._on_content_focus_out)

        # Formatting toolbar frame with enhanced styling moved to bottom
        toolbar_frame = ctk.CTkFrame(self, fg_color=colors["card_bg"], corner_radius=radius["md"])
        toolbar_frame.grid(row=5, column=0, sticky="ew", padx=spacing["lg"], pady=(0, spacing["md"]))
        
        toolbar_label = ctk.CTkLabel(
            toolbar_frame,
            text="✨ Formatting:",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=colors["fg"]
        )
        toolbar_label.pack(side="left", padx=spacing["md"], pady=spacing["sm"])
        
        # Bold button with refined styling
        bold_btn = ctk.CTkButton(
            toolbar_frame,
            text="B",
            width=40,
            height=36,
            corner_radius=radius["sm"],
            fg_color=colors["accent"],
            text_color=colors["button_fg"],
            hover_color=colors["button_hover"] if "button_hover" in colors else colors["accent_dark"],
            font=ctk.CTkFont(size=13, weight="bold"),
            command=lambda: self.insert_format("**", "**")
        )
        bold_btn.pack(side="left", padx=spacing["xs"])
        
        # Italic button with refined styling
        italic_btn = ctk.CTkButton(
            toolbar_frame,
            text="I",
            width=40,
            height=36,
            corner_radius=radius["sm"],
            fg_color=colors["accent"],
            text_color=colors["button_fg"],
            hover_color=colors["button_hover"] if "button_hover" in colors else colors["accent_dark"],
            font=ctk.CTkFont(size=13, slant="italic"),
            command=lambda: self.insert_format("*", "*")
        )
        italic_btn.pack(side="left", padx=spacing["xs"])
        
        # Underline button with refined styling
        underline_btn = ctk.CTkButton(
            toolbar_frame,
            text="U",
            width=40,
            height=36,
            corner_radius=radius["sm"],
            fg_color=colors["accent"],
            text_color=colors["button_fg"],
            hover_color=colors["button_hover"] if "button_hover" in colors else colors["accent_dark"],
            font=ctk.CTkFont(size=13, underline=True),
            command=lambda: self.insert_format("__", "__")
        )
        underline_btn.pack(side="left", padx=spacing["xs"])
        
        # Heading button with refined styling
        heading_btn = ctk.CTkButton(
            toolbar_frame,
            text="H",
            width=40,
            height=36,
            corner_radius=radius["sm"],
            fg_color=colors["accent"],
            text_color=colors["button_fg"],
            hover_color=colors["button_hover"] if "button_hover" in colors else colors["accent_dark"],
            font=ctk.CTkFont(size=14, weight="bold"),
            command=lambda: self.insert_format("## ", "")
        )
        heading_btn.pack(side="left", padx=spacing["xs"])
        
        # Bullet list button with refined styling
        bullet_btn = ctk.CTkButton(
            toolbar_frame,
            text="•",
            width=40,
            height=36,
            corner_radius=radius["sm"],
            fg_color=colors["accent"],
            text_color=colors["button_fg"],
            hover_color=colors["button_hover"] if "button_hover" in colors else colors["accent_dark"],
            font=ctk.CTkFont(size=16),
            command=lambda: self.insert_format("- ", "")
        )
        bullet_btn.pack(side="left", padx=spacing["xs"])
        
        # Font size dropdown with refined styling
        font_size_label = ctk.CTkLabel(
            toolbar_frame,
            text="Size:",
            font=ctk.CTkFont(size=12),
            text_color=colors["fg"]
        )
        font_size_label.pack(side="left", padx=(spacing["md"], spacing["xs"]))
        
        self.font_size_var = ctk.StringVar(value="14")
        font_size_menu = ctk.CTkOptionMenu(
            toolbar_frame,
            values=["12", "14", "16", "18", "20"],
            variable=self.font_size_var,
            width=70,
            height=36,
            corner_radius=radius["sm"],
            fg_color=colors["button_bg"],
            button_color=colors["accent"],
            button_hover_color=colors["button_hover"] if "button_hover" in colors else colors["accent_dark"],
            font=ctk.CTkFont(size=12),
            command=self.change_font_size
        )
        font_size_menu.pack(side="left", padx=spacing["xs"])
        
        # Bottom info frame with enhanced styling (status only)
        bottom_frame = ctk.CTkFrame(self, fg_color="#F5F0FF", corner_radius=0)
        bottom_frame.grid(row=6, column=0, sticky="ew", padx=spacing["lg"], pady=(0, spacing["md"]))
        bottom_frame.grid_columnconfigure(0, weight=1)
        
        # Status label with enhanced styling
        self.status_label = ctk.CTkLabel(
            bottom_frame,
            text="",
            font=ctk.CTkFont(size=13),
            text_color=colors["accent"]
        )
        self.status_label.grid(row=0, column=0, sticky="e")
    
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
        """Handle content change - mark dirty and schedule auto-save"""
        # If the user started typing, clear the placeholder now
        self._clear_content_placeholder_if_needed()
        self._is_dirty = True
        self.schedule_auto_save(event)
    
    def update_colors(self):
        """Update colors when theme changes"""
        colors = Theme.get_colors()
        
        self.configure(fg_color="#F5F0FF")
        
        self.back_button.configure(
            fg_color=colors["button_bg"],
            text_color=colors["button_fg"],
            hover_color=colors["button_hover"] if "button_hover" in colors else colors["accent_dark"]
        )
        
        self.save_button.configure(
            fg_color=colors["accent"],
            text_color=colors["button_fg"],
            hover_color=colors["button_hover"] if "button_hover" in colors else colors["accent_dark"]
        )
        
        title_color = colors["fg_secondary"] if getattr(self, "_title_placeholder_active", False) else colors["fg"]
        self.title_entry.configure(
            border_color=colors["border"],
            fg_color=colors["card_bg"],
            text_color=title_color
        )
        
        tags_color = colors["fg_secondary"] if getattr(self, "_tags_placeholder_active", False) else colors["fg"]
        self.tags_entry.configure(
            border_color=colors["border"],
            fg_color=colors["card_bg"],
            text_color=tags_color
        )
        
        self.category_dropdown.configure(
            fg_color=colors["button_bg"],
            button_color=colors["accent"],
            button_hover_color=colors["button_hover"] if "button_hover" in colors else colors["accent_dark"]
        )
        
        # Use lighter text when placeholder is active, normal when user has typed
        content_text_color = colors["fg_secondary"] if getattr(self, "_content_has_placeholder", False) else colors["fg"]
        self.content_text.configure(
            border_color=colors["border"],
            fg_color=colors["card_bg"],
            text_color=content_text_color
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
            self._is_dirty = False
            # Title: show real title, disable placeholder
            self.title_entry.delete(0, "end")
            self.title_entry.insert(0, note["title"])
            self._title_placeholder_active = False
            self.title_entry.configure(text_color=Theme.get_colors()["fg"])
            # When loading an existing note, remove placeholder behavior
            self._content_has_placeholder = False
            self.content_text.configure(text_color=Theme.get_colors()["fg"])  # normal text color
            self.content_text.delete("1.0", "end")
            self.content_text.insert("1.0", note["content"])
            
            # Load tags
            self.current_tags = note.get("tags", "")
            self.tags_entry.delete(0, "end")
            if self.current_tags:
                self.tags_entry.insert(0, self.current_tags)
                self._tags_placeholder_active = False
                self.tags_entry.configure(text_color=Theme.get_colors()["fg"])
            else:
                # No tags stored: show placeholder
                self.tags_entry.insert(0, self._tags_placeholder)
                self._tags_placeholder_active = True
                self.tags_entry.configure(text_color=Theme.get_colors()["fg_secondary"])
            
            # Load category
            self.current_category = note.get("category", "Personal")
            self.category_var.set(self.current_category)

            # Load and format timestamp
            created_at = note.get("created_at")
            updated_at = note.get("updated_at")
            self._update_timestamp_label(created_at, updated_at)
        else:
            self.current_note_id = None
            # Reset title placeholder for new note
            self.title_entry.delete(0, "end")
            self.title_entry.insert(0, self._title_placeholder)
            self._title_placeholder_active = True
            self.title_entry.configure(text_color=Theme.get_colors()["fg_secondary"])

            self.content_text.delete("1.0", "end")
            # Reset placeholder for new notes
            self._content_has_placeholder = True
            self._set_content_placeholder()

            # Reset tags placeholder for new note
            self.tags_entry.delete(0, "end")
            self.tags_entry.insert(0, self._tags_placeholder)
            self._tags_placeholder_active = True
            self.tags_entry.configure(text_color=Theme.get_colors()["fg_secondary"])

            self.category_var.set("Personal")
            self.current_tags = ""
            self.current_category = "Personal"
            self.timestamp_label.configure(text="")
            self._is_dirty = False
    
    def _update_timestamp_label(self, created_at: str, updated_at: str):
        """Update the human-friendly timestamp label"""
        from datetime import datetime
        if not created_at and not updated_at:
            self.timestamp_label.configure(text="")
            return
        # Prefer updated_at if available; otherwise use created_at
        ts_raw = updated_at or created_at
        try:
            # SQLite default format is usually YYYY-MM-DD HH:MM:SS
            dt = datetime.fromisoformat(ts_raw.replace(" ", "T")) if "T" not in ts_raw else datetime.fromisoformat(ts_raw)
            formatted = dt.strftime("%d %B %Y %H:%M")
        except Exception:
            formatted = ts_raw
        prefix = "Last edited" if updated_at else "Created"
        self.timestamp_label.configure(text=f"{prefix}: {formatted}")

    def handle_back(self):
        """Handle back navigation with unsaved changes check"""
        if not self._is_dirty:
            self.on_back()
            return

        result = messagebox.askquestion(
            "Unsaved Changes",
            "Do you want to save?",
            icon="warning",
            type="yesnocancel"
        )
        # yes -> save then go back, no -> discard, cancel -> stay
        if result == "yes":
            self.save_note()
            self.on_back()
        elif result == "no":
            # Discard changes
            self._is_dirty = False
            self.show_status("Notes has been discarded.")
            self.on_back()
        else:
            # cancel: do nothing
            return

    def save_note(self):
        """Save the current note"""
        raw_title = self.title_entry.get().strip()
        raw_tags = self.tags_entry.get().strip()
        # Treat placeholders as empty values
        title = "" if getattr(self, "_title_placeholder_active", False) or raw_title == self._title_placeholder else raw_title
        tags = "" if getattr(self, "_tags_placeholder_active", False) or raw_tags == self._tags_placeholder else raw_tags

        content = self._get_content_without_placeholder()
        category = self.category_var.get()
        
        if not title:
            title = "Untitled Note"
        
        if not content:
            self.show_status("Cannot save empty note 😿")
            return
        
        self.current_tags = tags
        self.current_category = category
        self.on_save(title, content, self.current_note_id, tags, category)
        self._is_dirty = False
        # Show toast-style notification
        self.show_status("Notes has been saved.")
    
    def schedule_auto_save(self, event=None):
        """Schedule auto-save after typing stops"""
        # Cancel previous auto-save job
        if self.auto_save_job:
            self.after_cancel(self.auto_save_job)
        
        # Schedule new auto-save after 2 seconds of inactivity
        self.auto_save_job = self.after(2000, self.auto_save)

    def _set_content_placeholder(self):
        """Show placeholder text in the content box with subtle color."""
        colors = Theme.get_colors()
        self.content_text.configure(text_color=colors["fg_secondary"])
        self.content_text.delete("1.0", "end")
        self.content_text.insert("1.0", self._content_placeholder)
        self._is_dirty = False
        self._content_has_placeholder = True

    def _clear_content_placeholder_if_needed(self):
        """Clear placeholder text when user starts typing or focuses the box."""
        if getattr(self, "_content_has_placeholder", False):
            colors = Theme.get_colors()
            self.content_text.delete("1.0", "end")
            self.content_text.configure(text_color=colors["fg"])
            self._content_has_placeholder = False

    def _on_content_focus_in(self, event=None):
        """Keep placeholder on focus; it will clear only when user types."""
        # Intentionally do nothing here so the hint stays visible until typing
        return

    def _on_content_focus_out(self, event=None):
        """Re-add placeholder if user leaves content box empty."""
        content = self.content_text.get("1.0", "end").strip()
        if not content:
            self._set_content_placeholder()

    def _on_title_focus_in(self, event=None):
        """Clear title placeholder only when user is about to type."""
        if getattr(self, "_title_placeholder_active", False):
            colors = Theme.get_colors()
            self.title_entry.delete(0, "end")
            self.title_entry.configure(text_color=colors["fg"])
            self._title_placeholder_active = False

    def _on_title_focus_out(self, event=None):
        """Restore title placeholder if field left empty."""
        text = self.title_entry.get().strip()
        if not text:
            colors = Theme.get_colors()
            self.title_entry.delete(0, "end")
            self.title_entry.insert(0, self._title_placeholder)
            self.title_entry.configure(text_color=colors["fg_secondary"])
            self._title_placeholder_active = True

    def _on_tags_focus_in(self, event=None):
        """Clear tags placeholder only when user is about to type."""
        if getattr(self, "_tags_placeholder_active", False):
            colors = Theme.get_colors()
            self.tags_entry.delete(0, "end")
            self.tags_entry.configure(text_color=colors["fg"])
            self._tags_placeholder_active = False

    def _on_tags_focus_out(self, event=None):
        """Restore tags placeholder if field left empty."""
        text = self.tags_entry.get().strip()
        if not text:
            colors = Theme.get_colors()
            self.tags_entry.delete(0, "end")
            self.tags_entry.insert(0, self._tags_placeholder)
            self.tags_entry.configure(text_color=colors["fg_secondary"])
            self._tags_placeholder_active = True

    def _get_content_without_placeholder(self) -> str:
        """Return content text, treating placeholder text as empty."""
        content = self.content_text.get("1.0", "end").strip()
        if getattr(self, "_content_has_placeholder", False) and content == self._content_placeholder:
            return ""
        return content

    def auto_save(self):
        """Auto-save the note"""
        raw_title = self.title_entry.get().strip()
        raw_tags = self.tags_entry.get().strip()
        title = "" if getattr(self, "_title_placeholder_active", False) or raw_title == self._title_placeholder else raw_title
        tags = "" if getattr(self, "_tags_placeholder_active", False) or raw_tags == self._tags_placeholder else raw_tags

        content = self._get_content_without_placeholder()
        category = self.category_var.get()
        
        # Only auto-save if we have content and this is an existing note
        if content and self.current_note_id:
            if not title:
                title = "Untitled Note"
            self.current_tags = tags
            self.current_category = category
            self.on_save(title, content, self.current_note_id, tags, category)
            self._is_dirty = False
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
