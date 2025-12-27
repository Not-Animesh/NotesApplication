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
                 on_delete_note: Callable, on_toggle_pin: Callable, note_service):
        """
        Initialize home screen
        
        Args:
            parent: Parent widget
            on_create_note: Callback for creating a note
            on_edit_note: Callback for editing a note (receives note_id)
            on_delete_note: Callback for deleting a note (receives note_id)
            on_toggle_pin: Callback for toggling pin (receives note_id)
            note_service: NoteService instance for operations
        """
        super().__init__(parent)
        
        self.on_create_note = on_create_note
        self.on_edit_note = on_edit_note
        self.on_delete_note = on_delete_note
        self.on_toggle_pin = on_toggle_pin
        self.note_service = note_service
        
        self.notes = []
        self.filtered_notes = []
        self.current_filter = None
        self.current_sort = "updated"
        self.background_label = None
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the home screen UI with background support"""
        colors = Theme.get_colors()
        
        # Configure grid - updated for proper row separation
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)  # Scrollable frame is now row 3
        
        spacing = Theme.get_spacing()
        radius = Theme.get_radius()
        
        # Header frame - use light lavender to blend with background image
        header_frame = ctk.CTkFrame(self, fg_color="#F5F0FF", corner_radius=0)
        header_frame.grid(row=0, column=0, sticky="ew", padx=spacing["lg"], pady=(spacing["lg"], spacing["md"]))
        header_frame.grid_columnconfigure(1, weight=1)
        
        # App title with icon image
        # Title text font (keep this size as-is)
        title_font = ctk.CTkFont(size=30, weight="bold")

        # Icon size is independent so you can tweak only the cat size here
        icon_size = 50  # change this value to make the cat bigger/smaller

        icon_path = Theme.get_asset_path("app_icon.png")
        self.app_icon_image = None
        if icon_path and os.path.exists(icon_path):
            try:
                img = Image.open(icon_path)
                self.app_icon_image = ctk.CTkImage(
                    light_image=img,
                    dark_image=img,
                    size=(icon_size, icon_size)
                )
            except:
                self.app_icon_image = None

        title_text = "KittyNotes"
        title_image = self.app_icon_image
        if title_image is None:
            # Fallback to emoji if icon not available
            title_text = "🐱 KittyNotes"

        title_label = ctk.CTkLabel(
            header_frame,
            text=title_text,
            image=title_image,
            compound="left",  # icon + text on the same line
            font=title_font,
            text_color=colors["fg"],
            anchor="center"  # center-align text with the cat icon
        )
        title_label.grid(row=0, column=0, sticky="w", padx=(0, spacing["md"]))
        
        # Button container - blend with background
        button_frame = ctk.CTkFrame(header_frame, fg_color="#F5F0FF", corner_radius=0)
        button_frame.grid(row=0, column=2, sticky="e")
        
        # Create note button with refined styling
        self.create_button = ctk.CTkButton(
            button_frame,
            text="✨ + New Note",
            width=150,
            height=48,
            corner_radius=radius["lg"],
            fg_color=colors["accent"],
            text_color=colors["button_fg"],
            hover_color=colors["button_hover"] if "button_hover" in colors else colors["accent_dark"],
            font=ctk.CTkFont(size=15, weight="bold"),
            command=self.on_create_note
        )
        self.create_button.pack(side="left", padx=spacing["xs"])
        
        # Search frame - blend with background
        search_frame = ctk.CTkFrame(self, fg_color="#F5F0FF", corner_radius=0)
        search_frame.grid(row=1, column=0, sticky="ew", padx=spacing["lg"], pady=(0, spacing["sm"]))
        search_frame.grid_columnconfigure(0, weight=1)
        
        # Search bar with refined styling
        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="🔍 Search notes by title, content, or tags...",
            placeholder_text_color=colors["fg_secondary"],
            height=42,
            corner_radius=radius["lg"],
            border_width=2,
            border_color=colors["border"],
            fg_color=colors["card_bg"],
            text_color=colors["fg"],
            font=ctk.CTkFont(size=14)
        )
        self.search_entry.grid(row=0, column=0, sticky="ew", padx=(0, spacing["sm"]))
        self.search_entry.bind("<KeyRelease>", self.on_search)
        
        # Sort dropdown with refined styling - dark background to match header
        self.sort_var = ctk.StringVar(value="Last Edited")
        self.sort_dropdown = ctk.CTkOptionMenu(
            search_frame,
            values=["Last Edited", "Alphabetical", "Pinned First"],
            variable=self.sort_var,
            command=self.on_sort_change,
            width=170,
            height=42,
            corner_radius=radius["lg"],
            fg_color=colors["button_bg"],  # black background
            text_color= "black",  # white text for contrast
            button_color=colors["accent"],
            button_hover_color=colors["button_hover"] if "button_hover" in colors else colors["accent_dark"],
            font=ctk.CTkFont(size=14)
        )
        self.sort_dropdown.grid(row=0, column=1)
        
        # Category filter frame - blend with background
        category_frame = ctk.CTkFrame(self, fg_color="#F5F0FF", corner_radius=0)
        category_frame.grid(row=2, column=0, sticky="ew", padx=spacing["lg"], pady=(spacing["md"], spacing["sm"]))
        
        # Category buttons with refined styling
        self.category_buttons = {}
        for i, category in enumerate(["All"] + Theme.CATEGORIES):
            is_active = category == "All"
            btn = ctk.CTkButton(
                category_frame,
                text=category,
                width=110,
                height=38,
                corner_radius=radius["md"],
                fg_color=colors["accent"] if is_active else colors["card_bg"],
                text_color=colors["button_fg"] if is_active else colors["fg"],
                hover_color=colors["button_hover"] if "button_hover" in colors else colors["accent_light"],
                font=ctk.CTkFont(size=13, weight="bold" if is_active else "normal"),
                command=lambda c=category: self.filter_by_category(c)
            )
            btn.pack(side="left", padx=spacing["xs"])
            self.category_buttons[category] = btn
        
        # Scrollable frame for notes - blend with background
        self.scrollable_frame = ctk.CTkScrollableFrame(
            self,
            fg_color="#F5F0FF",
            corner_radius=0
        )
        self.scrollable_frame.grid(row=3, column=0, sticky="nsew", padx=spacing["lg"], pady=spacing["md"])
        self.scrollable_frame.grid_columnconfigure(0, weight=1)
        
        # Status message - moved to row 4
        self.status_label = ctk.CTkLabel(
            self,
            text="",
            font=ctk.CTkFont(size=13),
            text_color=colors["accent"]
        )
        self.status_label.grid(row=4, column=0, sticky="ew", padx=spacing["lg"], pady=(0, spacing["md"]))
    
    def on_search(self, event=None):
        """Handle search input"""
        query = self.search_entry.get().strip()
        if query:
            # Search using service
            self.filtered_notes = self.note_service.search_notes(query)
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
        notes = self.note_service.get_all_notes(sort_by=self.current_sort)
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
            # Remove emoji from category name for service query
            cat_name = category.split()[0]
            self.current_filter = cat_name
            filtered = self.note_service.get_notes_by_category(cat_name)
            self.display_notes(filtered)
    
    def update_colors(self):
        """Update colors when theme changes"""
        colors = Theme.get_colors()
        spacing = Theme.get_spacing()
        radius = Theme.get_radius()
        
        # Update frame colors to blend with background
        self.configure(fg_color="#F5F0FF")
        self.scrollable_frame.configure(fg_color="#F5F0FF")
        
        self.create_button.configure(
            fg_color=colors["accent"],
            text_color=colors["button_fg"],
            hover_color=colors["button_hover"] if "button_hover" in colors else colors["accent_dark"]
        )
        
        self.status_label.configure(text_color=colors["accent"])
        
        # Update search entry
        self.search_entry.configure(
            border_color=colors["border"],
            fg_color=colors["card_bg"],
            text_color=colors["fg"]
        )
        
        # Update sort dropdown
        self.sort_dropdown.configure(
            fg_color=colors["button_bg"],
            button_color=colors["accent"],
            button_hover_color=colors["button_hover"] if "button_hover" in colors else colors["accent_dark"]
        )
        
        # Update category buttons
        for category, btn in self.category_buttons.items():
            is_active = category == "All" or category.split()[0] == self.current_filter
            btn.configure(
                fg_color=colors["accent"] if is_active else colors["card_bg"],
                text_color=colors["button_fg"] if is_active else colors["fg"],
                hover_color=colors["button_hover"] if "button_hover" in colors else colors["accent_light"]
            )
        
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
            spacing = Theme.get_spacing()
            empty_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="#F5F0FF")
            empty_frame.pack(pady=spacing["xxl"])
            
            # Try to load cat reading image
            cat_image_path = Theme.get_asset_path("cat_reading.png")
            if cat_image_path and os.path.exists(cat_image_path):
                try:
                    img = Image.open(cat_image_path)
                    cat_image = ctk.CTkImage(light_image=img, dark_image=img, size=(150, 150))
                    image_label = ctk.CTkLabel(empty_frame, image=cat_image, text="")
                    image_label.pack(pady=spacing["md"])
                except:
                    pass
            
            empty_label = ctk.CTkLabel(
                empty_frame,
                text=CAT_MESSAGES["no_notes"],
                font=ctk.CTkFont(size=18),
                text_color=colors["fg"]
            )
            empty_label.pack(pady=spacing["md"])
            return
        
        # Create note cards
        for note in notes:
            self.create_note_card(note)
    
    def create_note_card(self, note: Dict):
        """
        Create a note card widget with enhanced features and modern design
        
        Args:
            note: Note dictionary
        """
        colors = Theme.get_colors()
        spacing = Theme.get_spacing()
        radius = Theme.get_radius()
        is_pinned = note.get("is_pinned", 0)
        
        # Card frame with enhanced styling
        card = ctk.CTkFrame(
            self.scrollable_frame,
            fg_color=colors["card_bg"],
            corner_radius=radius["lg"],
            border_width=2 if is_pinned else 1,
            border_color=colors["pin_color"] if is_pinned else colors["border_light"]
        )
        card.pack(fill="x", pady=spacing["md"], padx=spacing["sm"])
        card.grid_columnconfigure(0, weight=1)
        
        # Enhanced hover effect with smooth transition
        original_bg = colors["card_bg"]
        hover_bg = colors["card_hover"]
        
        def on_enter(e):
            card.configure(fg_color=hover_bg, border_color=colors["accent_light"])
            # Update child frames
            for child in card.winfo_children():
                if isinstance(child, ctk.CTkFrame):
                    child.configure(fg_color=hover_bg)
        
        def on_leave(e):
            card.configure(fg_color=original_bg, border_color=colors["pin_color"] if is_pinned else colors["border_light"])
            # Update child frames
            for child in card.winfo_children():
                if isinstance(child, ctk.CTkFrame):
                    child.configure(fg_color=original_bg)
        
        card.bind("<Enter>", on_enter)
        card.bind("<Leave>", on_leave)
        
        # Title row with pin indicator - enhanced spacing
        title_frame = ctk.CTkFrame(card, fg_color=colors["card_bg"], corner_radius=0)
        title_frame.grid(row=0, column=0, sticky="ew", padx=spacing["lg"], pady=(spacing["lg"], spacing["sm"]))
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
        
        # Title with refined typography
        title = note.get("title", "Untitled")
        title_label = ctk.CTkLabel(
            title_frame,
            text=title if len(title) <= 50 else title[:50] + "...",
            font=ctk.CTkFont(size=17, weight="bold"),
            text_color=colors["fg"],
            anchor="w"
        )
        title_label.grid(row=0, column=1, sticky="w", padx=(spacing["sm"], 0))
        
        # Content preview with refined typography
        content = note.get("content", "")
        preview = content[:150] + "..." if len(content) > 150 else content
        content_label = ctk.CTkLabel(
            card,
            text=preview or "No content...",
            font=ctk.CTkFont(size=13),
            text_color=colors["fg_secondary"],
            anchor="w",
            justify="left",
            wraplength=550
        )
        content_label.grid(row=1, column=0, sticky="w", padx=spacing["lg"], pady=(0, spacing["sm"]))
        
        # Tags display with refined styling
        tags = note.get("tags", "")
        if tags:
            tags_frame = ctk.CTkFrame(card, fg_color=colors["card_bg"], corner_radius=0)
            tags_frame.grid(row=2, column=0, sticky="w", padx=spacing["lg"], pady=(0, spacing["xs"]))
            
            for tag in tags.split(","):
                tag = tag.strip()
                if tag:
                    tag_label = ctk.CTkLabel(
                        tags_frame,
                        text=f"#{tag}",
                        font=ctk.CTkFont(size=11, weight="normal"),
                        # Soft theme-matching pink/lavender background
                        fg_color="#FCE4EC",
                        # Dark text for elegant contrast
                        text_color=colors["fg"],
                        corner_radius=radius["md"],
                        padx=spacing["sm"],
                        pady=3
                    )
                    tag_label.pack(side="left", padx=3)
        
        # Category and timestamp row with refined styling
        info_frame = ctk.CTkFrame(card, fg_color=colors["card_bg"], corner_radius=0)
        info_frame.grid(row=3, column=0, sticky="ew", padx=spacing["lg"], pady=(spacing["xs"], spacing["md"]))
        info_frame.grid_columnconfigure(0, weight=1)
        
        # Category with better styling
        category = note.get("category", "Personal")
        category_label = ctk.CTkLabel(
            info_frame,
            text=f"📁 {category}",
            font=ctk.CTkFont(size=11),
            text_color=colors["fg_secondary"]
        )
        category_label.grid(row=0, column=0, sticky="w")
        
        # Updated time
        updated_at = note.get("updated_at", "")
        if updated_at:
            # Use raw stored timestamp; formatting will be handled in editor view when needed
            time_display = updated_at
            time_label = ctk.CTkLabel(
                info_frame,
                text=f"🐾 {time_display}",
                font=ctk.CTkFont(size=11),
                text_color="#702A44"
            )
            time_label.grid(row=0, column=1, sticky="e")
        
        # Button frame (top right of card) with refined positioning
        button_frame = ctk.CTkFrame(card, fg_color=colors["card_bg"], corner_radius=0)
        button_frame.grid(row=0, column=1, rowspan=4, padx=spacing["sm"], pady=spacing["md"], sticky="ne")
        
        # Standardized button dimensions
        button_width = 100
        button_height = 36
        
        # Pin/Unpin button with refined styling
        
        pin_fg = colors["accent"] if not is_pinned else colors["pin_color"]
        pin_btn = ctk.CTkButton(
            button_frame,
            text="📌      Pin",
            width=button_width,
            height=button_height,
            corner_radius=radius["md"],
            fg_color=pin_fg,
            text_color=colors["button_fg"],
            hover_color=colors["button_hover"] if "button_hover" in colors else colors["accent_dark"],
            font=ctk.CTkFont(size=13),
            command=lambda: self.on_toggle_pin(note["id"])
        )
        pin_btn.pack(pady=spacing["xs"])
        
        # Edit button with refined styling
        edit_btn = ctk.CTkButton(
            button_frame,
            text="✏️ Edit",
            width=button_width,
            height=button_height,
            corner_radius=radius["md"],
            fg_color=colors["accent"],
            text_color=colors["button_fg"],
            hover_color=colors["button_hover"] if "button_hover" in colors else colors["accent_dark"],
            font=ctk.CTkFont(size=13),
            command=lambda: self.on_edit_note(note["id"])
        )
        edit_btn.pack(pady=spacing["xs"])
        
        # Delete button with refined styling
        delete_btn = ctk.CTkButton(
            button_frame,
            text="🗑️ Delete",
            width=button_width,
            height=button_height,
            corner_radius=radius["md"],
            fg_color=colors["accent"],
            text_color=colors["button_fg"],
            hover_color=colors["error"],  # red on hover
            font=ctk.CTkFont(size=13),
            command=lambda: self.delete_note_with_confirm(note["id"])
        )
        delete_btn.pack(pady=spacing["xs"])
    
    def delete_note_with_confirm(self, note_id: int):
        """
        Delete note with confirmation
        
        Args:
            note_id: ID of note to delete
        """
        self.on_delete_note(note_id)
    
    def _setup_background(self):
        """Setup background image for the home screen"""
        try:
            from PIL import Image
            bg_path = Theme.get_background_image()
            if bg_path and os.path.exists(bg_path):
                bg_image = Image.open(bg_path)
                # Create a label with the background image
                # Place it at the back of the frame
                self.bg_image_obj = ctk.CTkImage(light_image=bg_image, dark_image=bg_image, size=(1000, 800))
                # Note: We'll use the parent window's background instead
                # as CTkFrame doesn't directly support background images
        except:
            pass
    
    def show_status(self, message: str):
        """
        Show status message
        
        Args:
            message: Status message to display
        """
        self.status_label.configure(text=message)
        # Auto-hide after 3 seconds
        self.after(3000, lambda: self.status_label.configure(text=""))
