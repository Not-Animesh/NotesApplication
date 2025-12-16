# WhiskerNotes - Application Flow Diagram

## System Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     WhiskerNotes Application                 │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
              ┌───────────────────────────┐
              │      main.py (Entry)      │
              │   - Window management     │
              │   - Screen navigation     │
              │   - Event coordination    │
              └───────────────────────────┘
                     │              │
        ┌────────────┴──────┐      │
        ▼                   ▼      ▼
┌──────────────┐    ┌──────────────────┐    ┌──────────────┐
│   ui/home.py │    │  ui/editor.py    │    │  themes.py   │
│  - Note cards│    │  - Title input   │    │  - Colors    │
│  - Scrolling │    │  - Content area  │    │  - Messages  │
│  - Buttons   │    │  - Auto-save     │    │  - Toggle    │
└──────────────┘    └──────────────────┘    └──────────────┘
        │                   │
        └────────┬──────────┘
                 ▼
        ┌─────────────────┐
        │   database.py   │
        │  - Create note  │
        │  - Read notes   │
        │  - Update note  │
        │  - Delete note  │
        │  - Search       │
        └─────────────────┘
                 │
                 ▼
        ┌─────────────────┐
        │ whiskernotes.db │
        │    (SQLite)     │
        └─────────────────┘
```

## User Interaction Flow

### Creating a New Note

```
User                Home Screen           Editor Screen         Database
 │                       │                      │                   │
 │  Click "+ New Note"   │                      │                   │
 ├──────────────────────>│                      │                   │
 │                       │  Navigate to Editor  │                   │
 │                       ├─────────────────────>│                   │
 │                       │                      │                   │
 │  Type title & content │                      │                   │
 ├──────────────────────────────────────────────>│                   │
 │                       │                      │                   │
 │  [Wait 2 seconds]     │                      │                   │
 │                       │                      │                   │
 │                       │         Auto-save triggers               │
 │                       │                      ├──────────────────>│
 │                       │                      │   CREATE note     │
 │                       │                      │<──────────────────┤
 │  "Auto-saved 🐾"      │                      │   note_id         │
 │<──────────────────────────────────────────────┤                   │
 │                       │                      │                   │
 │  Click "← Back"       │                      │                   │
 ├──────────────────────────────────────────────>│                   │
 │                       │  Navigate to Home    │                   │
 │                       │<─────────────────────┤                   │
 │                       │                      │                   │
 │                       │  Refresh notes list  │                   │
 │                       ├──────────────────────────────────────────>│
 │                       │                      │   SELECT * FROM   │
 │                       │<──────────────────────────────────────────┤
 │  See new note card    │  Display notes       │   notes[]         │
 │<──────────────────────┤                      │                   │
```

### Editing an Existing Note

```
User                Home Screen           Editor Screen         Database
 │                       │                      │                   │
 │  Click "Edit" button  │                      │                   │
 ├──────────────────────>│                      │                   │
 │                       │  Fetch note data     │                   │
 │                       ├──────────────────────────────────────────>│
 │                       │                      │   SELECT WHERE id │
 │                       │<──────────────────────────────────────────┤
 │                       │  Load into editor    │   note{}          │
 │                       ├─────────────────────>│                   │
 │                       │                      │  Populate fields  │
 │  Modify content       │                      │                   │
 ├──────────────────────────────────────────────>│                   │
 │                       │                      │                   │
 │  [Wait 2 seconds]     │                      │                   │
 │                       │         Auto-save triggers               │
 │                       │                      ├──────────────────>│
 │                       │                      │   UPDATE note     │
 │                       │                      │<──────────────────┤
 │  "Auto-saved 🐾"      │                      │   success         │
 │<──────────────────────────────────────────────┤                   │
```

### Deleting a Note

```
User                Home Screen                              Database
 │                       │                                       │
 │  Click "Delete"       │                                       │
 ├──────────────────────>│                                       │
 │                       │  Delete from DB                       │
 │                       ├──────────────────────────────────────>│
 │                       │         DELETE WHERE id               │
 │                       │<──────────────────────────────────────┤
 │                       │  Refresh display                      │
 │  "Note deleted...     │                                       │
 │   your cat is sad 😿" │                                       │
 │<──────────────────────┤                                       │
 │  Note card removed    │                                       │
 │<──────────────────────┤                                       │
```

### Theme Toggle

```
User                Home Screen           Themes Module
 │                       │                      │
 │  Click 🌙/☀️         │                      │
 ├──────────────────────>│                      │
 │                       │  Toggle theme        │
 │                       ├─────────────────────>│
 │                       │                      │  Switch colors
 │                       │<─────────────────────┤  "light"↔"dark"
 │                       │  Update all colors   │
 │  UI refreshes with    │                      │
 │  new theme colors     │                      │
 │<──────────────────────┤                      │
```

## Data Flow

### Note Creation Flow
```
Title Entry → Content TextBox → Auto-save Timer
                                      ↓
                               Validate Input
                                      ↓
                               database.create_note()
                                      ↓
                           INSERT INTO notes (title, content)
                                      ↓
                           Return note_id
                                      ↓
                           Update Editor state
                                      ↓
                           Show success message
```

### Note Retrieval Flow
```
User opens app → Home screen loads → database.get_all_notes()
                                            ↓
                          SELECT * FROM notes ORDER BY updated_at DESC
                                            ↓
                                      notes[] array
                                            ↓
                                   Create note cards
                                            ↓
                              Display in scrollable frame
```

## State Management

### Application State
```
WhiskerNotes (main.py)
├── current_screen: "home" | "editor"
├── home_screen: HomeScreen instance
├── editor_screen: EditorScreen instance
└── db: Database instance
```

### Theme State
```
Theme (themes.py)
├── current_theme: "light" | "dark"
├── LIGHT: { colors dict }
└── DARK: { colors dict }
```

### Editor State
```
EditorScreen
├── current_note_id: int | None
├── title_entry: Entry widget
├── content_text: TextBox widget
└── auto_save_job: Timer | None
```

## Event Handling

### Auto-Save Mechanism
```
1. User types in editor
        ↓
2. <KeyRelease> event fires
        ↓
3. schedule_auto_save() called
        ↓
4. Cancel previous timer
        ↓
5. Start new 2-second timer
        ↓
6. [2 seconds pass]
        ↓
7. auto_save() executes
        ↓
8. Validate content exists
        ↓
9. Call database.update_note()
        ↓
10. Show "Auto-saved 🐾"
```

### Button Click Handling
```
User clicks button
        ↓
Tkinter generates event
        ↓
Command callback fires
        ↓
Controller method executes
        ↓
Update model (database)
        ↓
Update view (UI)
        ↓
Show feedback message
```

## Module Dependencies

```
main.py
├── imports customtkinter
├── imports database
├── imports themes
└── imports ui.home, ui.editor

ui/home.py
├── imports customtkinter
└── imports themes

ui/editor.py
├── imports customtkinter
└── imports themes

database.py
├── imports sqlite3
├── imports os
└── imports datetime

themes.py
└── (no external dependencies)
```

## Execution Flow

### Startup Sequence
```
1. python main.py
2. Import all modules
3. main() function executes
4. WhiskerNotes() constructor
5. Initialize CustomTkinter window
6. Initialize Database (create tables if needed)
7. Set default theme (light)
8. Create HomeScreen instance
9. Load notes from database
10. Display home screen
11. Enter event loop (app.mainloop())
12. Wait for user interaction
```

### Shutdown Sequence
```
1. User closes window
2. Tkinter cleanup
3. Database connections auto-close
4. Python garbage collection
5. Process exits
```

## Error Handling

### Database Errors
- SQLite operations wrapped in try/except (implicit in sqlite3)
- Connection auto-closes on errors
- Transactions rolled back on failure

### UI Errors
- Empty note validation before save
- Auto-save only for existing notes
- Graceful handling of missing notes

### File System Errors
- Database file created if doesn't exist
- Write permissions checked implicitly
- SQLite handles file locking

---

*This flow diagram helps understand the complete architecture and interaction patterns in WhiskerNotes*
