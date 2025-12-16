# 🐱 WhiskerNotes - Complete Feature Guide

This document provides a comprehensive guide to all features in WhiskerNotes.

---

## 📋 Table of Contents

1. [Getting Started](#getting-started)
2. [Note Management](#note-management)
3. [Organization Features](#organization-features)
4. [Text Formatting](#text-formatting)
5. [Search & Filter](#search--filter)
6. [Customization](#customization)
7. [Tips & Tricks](#tips--tricks)

---

## Getting Started

### Creating Your First Note

1. **Launch WhiskerNotes** - Run `python main.py`
2. **Click "+ New Note"** - Located in the top-right corner
3. **Enter a Title** - Type your note title (or leave blank for "Untitled Note")
4. **Add Content** - Type your note content in the large text area
5. **Notes Auto-Save** - After 2 seconds of inactivity, you'll see "Meow! Auto-saved 🐾"

### Navigation

- **← Back Button** - Returns to the home screen
- **💾 Save Button** - Manually save your note anytime
- **🐾 Status Messages** - Watch for cute cat feedback at the bottom

---

## Note Management

### Pin Important Notes

**Pinned notes always appear at the top of your list!**

1. Find the note you want to pin on the home screen
2. Click the **"Pin"** button on the note card
3. The note will show a 📌 paw star icon and appear at the top
4. Click **"Unpin"** to remove the pin

**Use Cases:**
- Pin meeting agendas you're currently working on
- Keep important reference notes easily accessible
- Highlight ongoing project notes

### Delete Notes

1. Click the **"Delete"** button on any note card
2. The note is permanently removed
3. You'll see "Note deleted... your cat is sad 😿"

⚠️ **Note:** Deletion is permanent. There's no undo feature (yet!).

---

## Organization Features

### Tags System

**Tags help you categorize notes across multiple dimensions.**

#### Adding Tags

1. Open a note in the editor
2. Find the tags field: `🏷️ Tags (comma-separated, e.g., todo, study, important)`
3. Type your tags separated by commas: `meeting, urgent, q4-planning`
4. Tags are automatically saved with your note

#### Viewing Tags

Tags appear as colorful bubbles on note cards:
- **#meeting** 
- **#urgent**
- **#q4-planning**

#### Searching by Tag

Simply type the tag name in the search bar to find all notes with that tag!

**Examples:**
```
Search: "todo"     → Finds all notes tagged with #todo
Search: "study"    → Finds all notes tagged with #study
Search: "urgent"   → Finds all notes tagged with #urgent
```

### Categories

**Organize notes into predefined categories for better structure.**

#### Available Categories

1. **Personal 🐱** - Personal thoughts, diary entries, shopping lists
2. **Study 📘** - Study notes, course materials, learning resources
3. **Ideas 💡** - Brainstorming, creative thoughts, project ideas
4. **Work 💼** - Professional notes, meeting minutes, tasks
5. **Other 📝** - Everything else!

#### Setting a Category

1. Open a note in the editor
2. Use the **category dropdown** below the title
3. Select from the available categories
4. Category is saved automatically

#### Filtering by Category

On the home screen, click any category button to show only notes in that category:
- **All** - Show all notes
- **Personal 🐱** - Show only Personal notes
- **Study 📘** - Show only Study notes
- And so on...

---

## Text Formatting

### Formatting Toolbar

The toolbar provides quick access to text formatting options:

#### Basic Formatting

| Button | Format | Example |
|--------|--------|---------|
| **B** | Bold | `**text**` becomes **text** |
| **I** | Italic | `*text*` becomes *text* |
| **U** | Underline | `__text__` becomes __text__ |

**How to Use:**
1. Select the text you want to format
2. Click the formatting button
3. The text will be wrapped with formatting markers

#### Structure Tools

| Button | Function | Example |
|--------|----------|---------|
| **H** | Heading | `## Heading` |
| **•** | Bullet List | `- Item` |

#### Font Size

Use the **Size** dropdown to change the font size:
- **12** - Small
- **14** - Normal (default)
- **16** - Large
- **18** - Extra Large
- **20** - Huge

### Markdown Support

WhiskerNotes supports basic markdown formatting:

```markdown
**Bold Text**
*Italic Text*
__Underlined Text__

## Heading 2
### Heading 3

- Bullet point 1
- Bullet point 2

1. Numbered item
2. Numbered item
```

---

## Search & Filter

### Instant Search

The search bar provides real-time filtering as you type!

**Search Scope:**
- Note titles
- Note content
- Tags

**Examples:**
```
Search: "meeting"   → Finds all notes with "meeting" in title/content/tags
Search: "python"    → Finds study notes about Python
Search: "#urgent"   → Finds all notes tagged as urgent
```

### Sorting Options

Use the **sorting dropdown** to organize your notes:

1. **Last Edited** - Most recently edited notes first (default)
2. **Alphabetical** - Sort by title A-Z
3. **Pinned First** - Pinned notes at top, then by last edited

### Combining Filters

You can combine search and category filtering:

1. Select a category (e.g., "Study 📘")
2. Type in the search bar (e.g., "python")
3. Result: Only Study notes containing "python"

---

## Customization

### Theme Toggle

Click the **🌙/☀️ button** to switch themes:
- **Light Mode** (🌙) - Warm cream background, perfect for daytime
- **Dark Mode** (☀️) - Deep black background, easy on the eyes at night

### Accent Colors

WhiskerNotes supports multiple accent colors:
- **Pink** 💗 - Default, soft and cozy
- **Mint** 🍃 - Fresh and calm
- **Yellow** ☀️ - Bright and cheerful
- **Lavender** 💜 - Elegant and soothing

*Note: Accent color switching will be available in the theme menu (future feature)*

---

## Tips & Tricks

### Efficient Workflows

#### Quick Note Capture
1. Press `+ New Note`
2. Start typing immediately (title can be added later)
3. Auto-save handles the rest

#### Tag Strategy
Use a consistent tagging system:
- **Priority:** `urgent`, `important`, `someday`
- **Type:** `todo`, `done`, `reference`
- **Project:** `project-alpha`, `project-beta`

#### Category Organization
Develop a personal system:
- **Personal:** Everything non-work related
- **Study:** Learning and education
- **Ideas:** Brainstorming and creativity
- **Work:** Professional activities
- **Other:** Temporary or miscellaneous

### Keyboard Shortcuts

While in the editor:
- **Tab** - Move between title and content
- **Ctrl+A** - Select all text
- **Ctrl+C/V/X** - Copy/Paste/Cut
- Standard text editing shortcuts

### Word Count Tracking

The word count updates live as you type:
- Shows at the bottom of the editor: `📝 Word count: 42`
- Also displayed on each note card
- Useful for meeting word limits or tracking progress

### Auto-Save Messages

Watch for delightful auto-save messages:
- "Meow! Note saved 🐾"
- "Purr... Everything is safe 🐱"
- "Hooman, don't forget me! 🐱"
- "Your note is purr-fect! 🐾"
- "Meow meow! Saved successfully 🐱"

### Empty State

When you have no notes, you'll see:
- A cute cat reading image 📚🐱
- Message: "No notes yet... your cat is waiting 🐱"
- Perfect opportunity to create your first note!

---

## Feature Comparison

### Before vs After Enhancement

| Feature | Original | Enhanced |
|---------|----------|----------|
| **Organization** | None | Tags + Categories + Pinning |
| **Search** | None | Full-text + Tag search |
| **Formatting** | Plain text | Rich formatting toolbar |
| **Note Cards** | Basic | Tags, category, word count, timestamps |
| **Sorting** | Date only | Date, alphabetical, pinned |
| **Empty State** | Text only | Cat image + message |
| **Assets** | Text emoji | Custom images + icons |
| **Feedback** | Standard | Random cat messages |

---

## Coming Soon

Future features under consideration:
- 🎨 Accent color picker in UI
- 🖼️ Note attachments (images, files)
- 📤 Export to Markdown/PDF
- 🔒 Note encryption
- ☁️ Cloud sync
- 📝 Note linking
- 🎨 Drawing/sketching tool
- 📊 Statistics dashboard

---

**Made with 💖 and 🐾 by the WhiskerNotes team**

*Remember: A note a day keeps the chaos away!*
