# WhiskerNotes - Visual Documentation

This document provides visual representations of the WhiskerNotes application interface and workflows.

## Application Screens

### 1. Home Screen (Light Theme)

The home screen displays all your notes as cards with edit and delete options.

```
╔════════════════════════════════════════════════════════════╗
║  🐱 WhiskerNotes                      🌙  [+ New Note]     ║
╠════════════════════════════════════════════════════════════╣
║                                                            ║
║  ┌────────────────────────────────────────────────────┐   ║
║  │ Welcome to WhiskerNotes                      [Edit]│   ║
║  │ ─────────────────────────────────────────  [Delete]│   ║
║  │ This is your first note! WhiskerNotes is a cozy... │   ║
║  │ 🐾 2024-12-16 09:30:00                             │   ║
║  └────────────────────────────────────────────────────┘   ║
║                                                            ║
║  ┌────────────────────────────────────────────────────┐   ║
║  │ Shopping List                                [Edit]│   ║
║  │ ─────────────────────────────────────────  [Delete]│   ║
║  │ - Milk                                             │   ║
║  │ - Bread                                            │   ║
║  │ - Cat treats                                       │   ║
║  │ 🐾 2024-12-16 08:15:00                             │   ║
║  └────────────────────────────────────────────────────┘   ║
║                                                            ║
║  ┌────────────────────────────────────────────────────┐   ║
║  │ Project Ideas                                [Edit]│   ║
║  │ ─────────────────────────────────────────  [Delete]│   ║
║  │ 1. Build a cat-themed todo app                     │   ║
║  │ 2. Create pixel art cats                           │   ║
║  │ 3. Learn Python GUI development                    │   ║
║  │ 🐾 2024-12-16 07:45:00                             │   ║
║  └────────────────────────────────────────────────────┘   ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝
```

**Colors:**
- Background: Warm cream (#F6F1E7)
- Cards: White (#FFFFFF) with rounded corners
- Accent: Pink (#F6B1C3)
- Text: Dark gray (#2C2C2C)

### 2. Home Screen (Dark Theme)

Click the 🌙 button to toggle to dark mode for comfortable night-time use.

```
╔════════════════════════════════════════════════════════════╗
║  🐱 WhiskerNotes                      ☀️  [+ New Note]     ║
╠════════════════════════════════════════════════════════════╣
║                                                            ║
║  ┌────────────────────────────────────────────────────┐   ║
║  │ Meeting Notes                                [Edit]│   ║
║  │ ─────────────────────────────────────────  [Delete]│   ║
║  │ Discussed project timeline and deliverables...     │   ║
║  │ 🐾 2024-12-16 14:20:00                             │   ║
║  └────────────────────────────────────────────────────┘   ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝
```

**Colors:**
- Background: Deep black (#0F0F0F)
- Cards: Dark gray (#1A1A1A) with rounded corners
- Accent: Pink (#F6B1C3)
- Text: Light gray (#E8E8E8)

### 3. Empty State

When you have no notes yet, WhiskerNotes shows a friendly message.

```
╔════════════════════════════════════════════════════════════╗
║  🐱 WhiskerNotes                      🌙  [+ New Note]     ║
╠════════════════════════════════════════════════════════════╣
║                                                            ║
║                                                            ║
║                                                            ║
║                  No notes yet...                           ║
║                  your cat is waiting 🐱                    ║
║                                                            ║
║                                                            ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝
```

### 4. Editor Screen

The editor provides a distraction-free writing experience with auto-save.

```
╔════════════════════════════════════════════════════════════╗
║  [← Back]                                    [💾 Save]     ║
╠════════════════════════════════════════════════════════════╣
║  ┌────────────────────────────────────────────────────┐   ║
║  │ 🐱 My Awesome Note                                 │   ║
║  └────────────────────────────────────────────────────┘   ║
║  ┌────────────────────────────────────────────────────┐   ║
║  │                                                    │   ║
║  │  This is where I write my thoughts and ideas...   │   ║
║  │                                                    │   ║
║  │  The editor supports multiple lines and           │   ║
║  │  automatically saves your work after 2 seconds    │   ║
║  │  of inactivity.                                   │   ║
║  │                                                    │   ║
║  │  You can write as much as you want, and the       │   ║
║  │  text will wrap nicely within the editor.         │   ║
║  │                                                    │   ║
║  │                                                    │   ║
║  │                                                    │   ║
║  │                                                    │   ║
║  └────────────────────────────────────────────────────┘   ║
║  Auto-saved 🐾                                             ║
╚════════════════════════════════════════════════════════════╝
```

## User Workflows

### Creating a New Note

```
[Home Screen] 
     │
     │ Click "+ New Note"
     ↓
[Editor Screen - Empty]
     │
     │ Type title and content
     ↓
[Auto-save after 2s]
     │
     │ "Auto-saved 🐾"
     ↓
[Click "← Back"]
     │
     ↓
[Home Screen - New note visible]
```

### Editing an Existing Note

```
[Home Screen with notes]
     │
     │ Click "Edit" on a note card
     ↓
[Editor Screen - Loaded with note]
     │
     │ Modify content
     ↓
[Auto-save after 2s]
     │
     │ "Auto-saved 🐾"
     ↓
[Click "← Back"]
     │
     ↓
[Home Screen - Updated note visible]
```

### Deleting a Note

```
[Home Screen with notes]
     │
     │ Click "Delete" on a note card
     ↓
[Note removed from database]
     │
     │ "Note deleted... your cat is sad 😿"
     ↓
[Home Screen - Note removed]
```

## Cat-Themed Feedback Messages

Throughout the application, you'll encounter friendly cat-themed messages:

| Action | Message | Emoji |
|--------|---------|-------|
| Note saved | "Meow! Your note is safe" | 🐾 |
| Auto-saved | "Auto-saved" | 🐾 |
| Note created | "Purr! New note created" | 🐱 |
| Note deleted | "Note deleted... your cat is sad" | 😿 |
| No notes | "No notes yet... your cat is waiting" | 🐱 |
| Welcome | "Welcome to WhiskerNotes!" | 🐾 |

## Color Palette

### Light Theme
- **Background**: #F6F1E7 (Warm cream)
- **Foreground**: #2C2C2C (Dark gray)
- **Accent**: #F6B1C3 (Pink)
- **Card Background**: #FFFFFF (White)
- **Card Hover**: #FFE5EC (Light pink)
- **Border**: #E8D5D5 (Light border)

### Dark Theme
- **Background**: #0F0F0F (Deep black)
- **Foreground**: #E8E8E8 (Light gray)
- **Accent**: #F6B1C3 (Pink)
- **Card Background**: #1A1A1A (Dark gray)
- **Card Hover**: #2A2A2A (Lighter dark)
- **Border**: #2A2A2A (Dark border)

## UI Elements

### Buttons
- Rounded corners (20px border radius)
- Pink accent color (#F6B1C3)
- Hover effects with lighter colors
- Unicode emoji for icons

### Cards
- Rounded corners (15px border radius)
- Subtle border (1px)
- Shadow effect on hover
- Responsive padding

### Input Fields
- Large, comfortable text areas
- Placeholder text with cat emoji
- Clear focus indicators
- Rounded corners

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| Tab | Navigate between fields |
| Ctrl+A | Select all text |
| Escape | (Future: Close editor) |

## Technical Details

### Auto-Save Behavior
- Triggers 2 seconds after typing stops
- Only saves if content is not empty
- Shows brief "Auto-saved 🐾" message
- Silently fails if note is new (creates on first save)

### Theme Toggle
- Persists during application session
- Affects all UI elements simultaneously
- Smooth transitions between themes
- Icon changes (🌙 ↔ ☀️)

### Database
- SQLite for persistence
- Automatic timestamps (created_at, updated_at)
- Transaction safety
- Efficient queries with indexing

---

*WhiskerNotes - Making note-taking cozy, one paw print at a time 🐾*
