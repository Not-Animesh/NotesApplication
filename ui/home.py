"""
WhiskerNotes - Home Screen UI
Dashboard displaying note cards with create, edit, delete functionality
"""

import customtkinter as ctk
from typing import Callable, List, Dict
from themes import Theme, CAT_MESSAGES
from PIL import Image
import os


class HomeScreen(ctk.CTkFrame):
    """Home screen with note cards display"""
    
    def __init__(self, parent, on_create_note: Callable, on_edit_note: Callable, 
                 on_delete_note: Callable, on_toggle_theme: Callable, 
                 on_toggle_pin: Callable, db):
        """
        Initialize home screen
        
        Args:
            parent: Parent widget
            on_create_note: Callback for creating a note
            on_edit_note: Callback for editing a note (receives note_id)
            on_delete_note: Callback for deleting a note (receives note_id)
            on_toggle_theme: Callback for toggling theme
            on_toggle_pin: Callback for toggling pin (receives note_id)
            db: Database instance for search/filter operations
        """
        super().__init__(parent)
        
        self.on_create_note = on_create_note
        self.on_edit_note = on_edit_note
        self.on_delete_note = on_delete_note
        self.on_toggle_theme = on_toggle_theme
        self.on_toggle_pin = on_toggle_pin
        self.db = db
        
        self.notes = []
        self.filtered_notes = []
        self.current_filter = None
        self.current_sort = "updated"
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the home screen UI"""
        colors = Theme.get_colors()
        
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
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
        
        # Search and filter frame
        search_frame = ctk.CTkFrame(self, fg_color=colors["bg"], corner_radius=0)
        search_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 10))
        search_frame.grid_columnconfigure(0, weight=1)
        
        # Search bar
        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="🔍 Search notes by title, content, or tags...",
            height=40,
            corner_radius=20,
            border_width=2,
            border_color=colors["border"],
            fg_color=colors["card_bg"],
            text_color=colors["fg"]
        )
        self.search_entry.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        self.search_entry.bind("<KeyRelease>", self.on_search)
        
        # Sort dropdown
        self.sort_var = ctk.StringVar(value="Last Edited")
        self.sort_dropdown = ctk.CTkOptionMenu(
            search_frame,
            values=["Last Edited", "Alphabetical", "Pinned First"],
            variable=self.sort_var,
            command=self.on_sort_change,
            width=150,
            height=40,
            corner_radius=20,
            fg_color=colors["button_bg"],
            button_color=colors["accent"],
            button_hover_color=colors["card_hover"]
        )
        self.sort_dropdown.grid(row=0, column=1)
        
        # Category filter frame
        category_frame = ctk.CTkFrame(self, fg_color=colors["bg"], corner_radius=0)
        category_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=(50, 5))
        
        # Category buttons
        self.category_buttons = {}
        for i, category in enumerate(["All"] + Theme.CATEGORIES):
            btn = ctk.CTkButton(
                category_frame,
                text=category,
                width=80,
                height=30,
                corner_radius=15,
                fg_color=colors["accent"] if category == "All" else colors["card_bg"],
                text_color=colors["button_fg"] if category == "All" else colors["fg"],
                hover_color=colors["card_hover"],
                command=lambda c=category: self.filter_by_category(c)
            )
            btn.pack(side="left", padx=5)
            self.category_buttons[category] = btn
        
        # Scrollable frame for notes
        self.scrollable_frame = ctk.CTkScrollableFrame(
            self,
            fg_color=colors["bg"],
            corner_radius=0
        )
        self.scrollable_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=10)
        self.scrollable_frame.grid_columnconfigure(0, weight=1)
        
        # Status message
        self.status_label = ctk.CTkLabel(
            self,
            text="",
            font=ctk.CTkFont(size=12),
            text_color=colors["accent"]
        )
        self.status_label.grid(row=3, column=0, sticky="ew", padx=20, pady=(0, 10))
    
    def on_search(self, event=None):
        """Handle search input"""
        query = self.search_entry.get().strip()
        if query:
            # Search using database
            self.filtered_notes = self.db.search_notes(query)
            self.display_notes(self.filtered_notes)
        else:
            # Show all notes
            self.display_notes(self.notes)
    
    def on_sort_change(self, choice):
        """Handle sort option change"""
        sort_map = {
            "Last Edited": "updated",
            "Alphabetical": "alphabetical",
            "Pinned First": "pinned"
        }
        self.current_sort = sort_map.get(choice, "updated")
        
        # Re-fetch and display sorted notes
        notes = self.db.get_all_notes(sort_by=self.current_sort)
        self.display_notes(notes)
    
    def filter_by_category(self, category):
        """Filter notes by category"""
        colors = Theme.get_colors()
        
        # Update button colors
        for cat, btn in self.category_buttons.items():
            if cat == category:
                btn.configure(fg_color=colors["accent"], text_color=colors["button_fg"])
            else:
                btn.configure(fg_color=colors["card_bg"], text_color=colors["fg"])
        
        # Filter notes
        if category == "All":
            self.current_filter = None
            self.display_notes(self.notes)
        else:
            # Remove emoji from category name for database query
            cat_name = category.split()[0]
            self.current_filter = cat_name
            filtered = self.db.get_notes_by_category(cat_name)
            self.display_notes(filtered)
    
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
            # Empty state with cat reading image
            empty_frame = ctk.CTkFrame(self.scrollable_frame, fg_color=colors["bg"])
            empty_frame.pack(pady=50)
            
            # Try to load cat reading image
            cat_image_path = Theme.get_asset_path("cat_reading.png")
            if cat_image_path and os.path.exists(cat_image_path):
                try:
                    img = Image.open(cat_image_path)
                    cat_image = ctk.CTkImage(light_image=img, dark_image=img, size=(150, 150))
                    image_label = ctk.CTkLabel(empty_frame, image=cat_image, text="")
                    image_label.pack(pady=10)
                except:
                    pass
            
            empty_label = ctk.CTkLabel(
                empty_frame,
                text=CAT_MESSAGES["no_notes"],
                font=ctk.CTkFont(size=18),
                text_color=colors["fg"]
            )
            empty_label.pack(pady=10)
            return
        
        # Create note cards
        for note in notes:
            self.create_note_card(note)
    
    def create_note_card(self, note: Dict):
        """
        Create a note card widget with enhanced features
        
        Args:
            note: Note dictionary
        """
        colors = Theme.get_colors()
        is_pinned = note.get("is_pinned", 0)
        
        # Card frame with hover effect
        card = ctk.CTkFrame(
            self.scrollable_frame,
            fg_color=colors["card_bg"],
            corner_radius=15,
            border_width=2 if is_pinned else 1,
            border_color=colors["pin_color"] if is_pinned else colors["border"]
        )
        card.pack(fill="x", pady=10, padx=5)
        card.grid_columnconfigure(0, weight=1)
        
        # Add hover effect
        card.bind("<Enter>", lambda e: card.configure(fg_color=colors["card_hover"]))
        card.bind("<Leave>", lambda e: card.configure(fg_color=colors["card_bg"]))
        
        # Title row with pin indicator
        title_frame = ctk.CTkFrame(card, fg_color=colors["card_bg"])
        title_frame.grid(row=0, column=0, sticky="ew", padx=15, pady=(15, 5))
        title_frame.grid_columnconfigure(1, weight=1)
        
        # Pin indicator
        if is_pinned:
            pin_icon_path = Theme.get_asset_path("paw_star_icon.png")
            if pin_icon_path and os.path.exists(pin_icon_path):
                try:
                    pin_img = Image.open(pin_icon_path)
                    pin_image = ctk.CTkImage(light_image=pin_img, dark_image=pin_img, size=(20, 20))
                    pin_label = ctk.CTkLabel(title_frame, image=pin_image, text="")
                    pin_label.grid(row=0, column=0, padx=(0, 5))
                except:
                    # Fallback to emoji
                    pin_label = ctk.CTkLabel(title_frame, text="📌", font=ctk.CTkFont(size=14))
                    pin_label.grid(row=0, column=0, padx=(0, 5))
            else:
                pin_label = ctk.CTkLabel(title_frame, text="📌", font=ctk.CTkFont(size=14))
                pin_label.grid(row=0, column=0, padx=(0, 5))
        
        # Title
        title = note.get("title", "Untitled")
        title_label = ctk.CTkLabel(
            title_frame,
            text=title if len(title) <= 50 else title[:50] + "...",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=colors["fg"],
            anchor="w"
        )
        title_label.grid(row=0, column=1, sticky="w")
        
        # Content preview
        content = note.get("content", "")
        preview = content[:150] + "..." if len(content) > 150 else content
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
        
        # Tags display
        tags = note.get("tags", "")
        if tags:
            tags_frame = ctk.CTkFrame(card, fg_color=colors["card_bg"])
            tags_frame.grid(row=2, column=0, sticky="w", padx=15, pady=(0, 5))
            
            for tag in tags.split(","):
                tag = tag.strip()
                if tag:
                    tag_label = ctk.CTkLabel(
                        tags_frame,
                        text=f"#{tag}",
                        font=ctk.CTkFont(size=10),
                        fg_color=colors["tag_bg"],
                        text_color=colors["accent"],
                        corner_radius=10,
                        padx=8,
                        pady=2
                    )
                    tag_label.pack(side="left", padx=3)
        
        # Category and timestamp row
        info_frame = ctk.CTkFrame(card, fg_color=colors["card_bg"])
        info_frame.grid(row=3, column=0, sticky="ew", padx=15, pady=(0, 10))
        info_frame.grid_columnconfigure(0, weight=1)
        
        # Category
        category = note.get("category", "Personal")
        category_label = ctk.CTkLabel(
            info_frame,
            text=f"📁 {category}",
            font=ctk.CTkFont(size=10),
            text_color=colors["fg"]
        )
        category_label.grid(row=0, column=0, sticky="w")
        
        # Word count
        word_count = note.get("word_count", 0)
        wc_label = ctk.CTkLabel(
            info_frame,
            text=f"📝 {word_count} words",
            font=ctk.CTkFont(size=10),
            text_color=colors["fg"]
        )
        wc_label.grid(row=0, column=1, padx=10)
        
        # Updated time
        updated_at = note.get("updated_at", "")
        if updated_at:
            time_label = ctk.CTkLabel(
                info_frame,
                text=f"🐾 {updated_at}",
                font=ctk.CTkFont(size=10),
                text_color=colors["accent"]
            )
            time_label.grid(row=0, column=2, sticky="e")
        
        # Button frame (top right of card)
        button_frame = ctk.CTkFrame(card, fg_color=colors["card_bg"])
        button_frame.grid(row=0, column=1, rowspan=4, padx=10, pady=10, sticky="ne")
        
        # Pin/Unpin button
        pin_text = "Unpin" if is_pinned else "Pin"
        pin_btn = ctk.CTkButton(
            button_frame,
            text=pin_text,
            width=70,
            height=30,
            corner_radius=15,
            fg_color=colors["pin_color"] if is_pinned else colors["button_bg"],
            text_color=colors["button_fg"],
            hover_color=colors["card_hover"],
            command=lambda: self.on_toggle_pin(note["id"])
        )
        pin_btn.pack(pady=3)
        
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
        edit_btn.pack(pady=3)
        
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
        delete_btn.pack(pady=3)
    
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
