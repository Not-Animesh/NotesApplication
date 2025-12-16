# 🐱 WhiskerNotes - A Cozy Cat-Themed Notes Application

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![CustomTkinter](https://img.shields.io/badge/CustomTkinter-5.2.2-green.svg)](https://github.com/TomSchimansky/CustomTkinter)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A feature-rich, cat-themed desktop notes application built with Python and CustomTkinter. WhiskerNotes provides an advanced yet intuitive environment for creating, organizing, and managing your notes with delightful cat-inspired feedback messages, rich formatting options, and a cozy aesthetic.

---

## 📋 Table of Contents

- [Problem Statement](#-problem-statement)
- [Features](#-features)
- [System Architecture](#-system-architecture)
- [Installation](#-installation)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [Technologies Used](#-technologies-used)
- [Screenshots](#-screenshots)
- [Contributing](#-contributing)
- [Conclusion](#-conclusion)

---

## 🎯 Problem Statement

In today's digital world, note-taking applications are often cluttered with unnecessary features, overwhelming interfaces, and distracting elements. Users need a simple, calm, and focused environment to capture their thoughts without complexity.

**WhiskerNotes** addresses this need by providing:
- A minimalist yet powerful interface that reduces cognitive load
- Cat-themed visual elements that add personality without distraction
- Advanced organization features (tags, categories, pinning)
- Rich text formatting for expressive notes
- Auto-save functionality to prevent data loss
- Powerful search and filtering capabilities
- Light and dark themes for different lighting conditions
- Persistent storage with SQLite for reliability

**Target Users:**
- Students organizing study materials by subject
- Writers brainstorming and categorizing ideas
- Professionals managing work notes and meeting minutes
- Anyone seeking a delightful, powerful note-taking experience

---

## ✨ Features

### Core Functionality
- ✅ **Create Notes** - Start writing instantly with the "+ New Note" button
- ✅ **Edit Notes** - Click any note card to edit its content
- ✅ **Delete Notes** - Remove unwanted notes with a single click
- ✅ **Pin Notes** - Pin important notes to the top of your list
- ✅ **Auto-Save** - Notes automatically save after 2 seconds of inactivity with cute messages

### Organization & Search
- 🔍 **Instant Search** - Search by title, content, or tags in real-time
- 🏷️ **Tags System** - Add multiple comma-separated tags to notes
- 📁 **Categories** - Organize notes into Personal, Study, Ideas, Work, or Other
- 🎯 **Smart Filtering** - Filter notes by category or search by tag
- 📊 **Sorting Options** - Sort by last edited, alphabetical, or pinned first

### Rich Text Editor
- ✨ **Formatting Toolbar** - Bold, italic, underline text
- 📐 **Font Sizes** - Choose from 5 different font sizes (12-20px)
- 📝 **Structure Tools** - Add headings and bullet lists
- 📊 **Word Counter** - Live word count display below editor
- 🎨 **Markdown Support** - Format text with markdown-style syntax

### User Experience
- 🌙 **Theme Toggle** - Switch between Light and Dark modes
- 🎨 **Accent Colors** - Choose from pink, mint, yellow, or lavender accents
- 🐾 **Cat-Themed Feedback** - Delightful messages like "Meow! Your note is safe 🐾"
- 📱 **Responsive Design** - Cards and layout adapt to window size
- ✨ **Hover Effects** - Soft pastel shading on note cards
- 🖼️ **Cat Images** - Adorable cat illustrations for empty states and icons

### Note Cards Enhancement
- 📌 **Pin Indicators** - Visual paw star icon for pinned notes
- 🏷️ **Tag Bubbles** - Tags displayed as colorful pastel bubbles
- 📁 **Category Display** - See the category of each note at a glance
- 📝 **Word Count** - Word count visible on each card
- 🕐 **Timestamps** - Last edit time displayed with paw print emoji
- 📄 **Content Preview** - See truncated content (150 characters)

### Technical Features
- 💾 **SQLite Database** - Reliable local data persistence with migration support
- 🔄 **Real-time Updates** - Notes list refreshes automatically
- 🎯 **Keyboard Support** - Efficient navigation and editing
- 🖼️ **Asset Management** - Custom icons and backgrounds
- 📊 **Data Integrity** - Automatic word count tracking and timestamps

---

## 🏗️ System Architecture

WhiskerNotes follows a clean, modular architecture separating concerns:

```
┌─────────────────────────────────────────┐
│           User Interface Layer          │
│  (CustomTkinter - home.py, editor.py)  │
└──────────────────┬──────────────────────┘
                   │
┌──────────────────▼──────────────────────┐
│         Application Layer               │
│        (main.py - Controller)           │
└──────────────────┬──────────────────────┘
                   │
┌──────────────────▼──────────────────────┐
│          Data Layer                     │
│    (database.py - SQLite Operations)    │
└──────────────────┬──────────────────────┘
                   │
┌──────────────────▼──────────────────────┐
│         Storage Layer                   │
│      (whiskernotes.db - SQLite DB)      │
└─────────────────────────────────────────┘
```

### Component Breakdown

#### 1. **main.py** - Application Controller
- Initializes the application window
- Manages screen navigation (Home ↔ Editor)
- Coordinates between UI and database
- Handles theme switching
- Acts as the central controller

#### 2. **database.py** - Data Persistence
- SQLite database initialization
- CRUD operations (Create, Read, Update, Delete)
- Note search functionality
- Transaction management
- Data validation

#### 3. **themes.py** - Visual Configuration
- Color scheme definitions (Light/Dark)
- Theme state management
- Cat-themed message strings
- Consistent styling constants

#### 4. **ui/home.py** - Home Screen
- Note cards display in scrollable grid
- Create new note button
- Theme toggle button
- Edit/Delete actions per note
- Empty state handling

#### 5. **ui/editor.py** - Editor Screen
- Title and content input fields
- Manual save button
- Auto-save mechanism (2s delay)
- Back navigation
- Status messages

### Data Flow

```
User Action → UI Component → Main Controller → Database → SQLite
                                    ↓
                          UI Update ← Data Retrieved
```

**Example Flow - Creating a Note:**
1. User clicks "+ New Note" button in `home.py`
2. `main.py` controller shows `editor.py`
3. User types title and content
4. After 2s inactivity, auto-save triggers
5. `main.py` calls `database.create_note()`
6. SQLite stores the note
7. Success message displayed: "Meow! Your note is safe 🐾"

---

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git (for cloning)

### Step 1: Clone the Repository
```bash
git clone https://github.com/Not-Animesh/NotesApplication.git
cd NotesApplication
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

This will install:
- `customtkinter==5.2.1` - Modern UI framework

### Step 3: Run the Application
```bash
python main.py
```

The application will launch, and a SQLite database file (`whiskernotes.db`) will be created automatically in the application directory.

---

## 📖 Usage

### Creating Your First Note
1. Launch WhiskerNotes
2. Click the **"+ New Note"** button
3. Enter a title (optional - defaults to "Untitled Note")
4. Type your content
5. Notes auto-save after 2 seconds of inactivity
6. Click **"← Back"** to return to the home screen

### Editing an Existing Note
1. From the home screen, click the **"Edit"** button on any note card
2. Modify the title or content
3. Changes auto-save automatically
4. Click **"← Back"** when finished

### Deleting a Note
1. Click the **"Delete"** button on any note card
2. The note is permanently removed
3. A confirmation message appears: "Note deleted... your cat is sad 😿"

### Switching Themes
- Click the **🌙/☀️** button in the top-right corner
- Toggle between Light and Dark modes
- Theme preference persists during the session

### Keyboard Navigation
- **Tab** - Move between title and content fields
- **Ctrl+A** - Select all text
- Standard text editing shortcuts work in all fields

---

## 📂 Project Structure

```
WhiskerNotes/
├── main.py              # Application entry point and controller
├── database.py          # SQLite database operations
├── themes.py            # Theme colors and cat messages
├── requirements.txt     # Python dependencies
├── README.md            # This file
│
├── ui/                  # User interface components
│   ├── home.py          # Home screen with note cards
│   └── editor.py        # Note editor screen
│
├── assets/              # Visual assets
│   ├── cats/            # Pixel cat images (placeholders)
│   │   └── README.md    # Cat asset documentation
│   └── icons/           # UI icons (placeholders)
│       └── README.md    # Icon documentation
│
└── whiskernotes.db      # SQLite database (created at runtime)
```

### File Descriptions

| File | Purpose | Lines of Code |
|------|---------|---------------|
| `main.py` | Main application controller | ~140 |
| `database.py` | Database operations | ~150 |
| `themes.py` | Theme configuration | ~60 |
| `ui/home.py` | Home screen UI | ~260 |
| `ui/editor.py` | Editor screen UI | ~200 |
| **Total** | **Complete application** | **~810** |

---

## 🛠️ Technologies Used

### Core Technologies
- **Python 3.8+** - Primary programming language
- **CustomTkinter 5.2.1** - Modern, customizable UI framework
- **SQLite3** - Lightweight database (built into Python)

### Why These Technologies?

#### CustomTkinter
- Modern, native-looking widgets
- Built-in dark mode support
- Rounded corners and smooth animations
- Cross-platform (Windows, macOS, Linux)
- No web browser required

#### SQLite
- Zero configuration
- Serverless architecture
- Reliable and fast
- Built into Python standard library
- Perfect for desktop applications

#### Python
- Simple, readable syntax
- Excellent for rapid development
- Rich standard library
- Cross-platform compatibility
- Large ecosystem of packages

---

## 📸 Screenshots

### Light Theme - Home Screen
*Features note cards with rounded corners, pink accents, and the warm cream background*

```
┌─────────────────────────────────────────────┐
│  🐱 WhiskerNotes         🌙  [+ New Note]   │
├─────────────────────────────────────────────┤
│  ┌─────────────────────────────────────┐   │
│  │ Meeting Notes                 [Edit]│   │
│  │ Discussed project timeline... [Delete]  │
│  │ 🐾 2024-12-16 09:30:00              │   │
│  └─────────────────────────────────────┘   │
│  ┌─────────────────────────────────────┐   │
│  │ Shopping List                [Edit]│   │
│  │ Milk, bread, cat treats...   [Delete]  │
│  │ 🐾 2024-12-16 08:15:00              │   │
│  └─────────────────────────────────────┘   │
└─────────────────────────────────────────────┘
```

### Dark Theme - Editor Screen
*Distraction-free writing with auto-save feedback*

```
┌─────────────────────────────────────────────┐
│  [← Back]                     [💾 Save]     │
├─────────────────────────────────────────────┤
│  🐱 My Awesome Note                         │
├─────────────────────────────────────────────┤
│  This is where I write my thoughts...       │
│  The editor supports multiple lines         │
│  and auto-saves after 2 seconds.            │
│                                             │
│                                             │
├─────────────────────────────────────────────┤
│  Auto-saved 🐾                              │
└─────────────────────────────────────────────┘
```

### Empty State
*Friendly message when no notes exist*

```
┌─────────────────────────────────────────────┐
│  🐱 WhiskerNotes         🌙  [+ New Note]   │
├─────────────────────────────────────────────┤
│                                             │
│           No notes yet...                   │
│           your cat is waiting 🐱            │
│                                             │
└─────────────────────────────────────────────┘
```

---

## 🤝 Contributing

Contributions are welcome! Here are some ways you can contribute:

### Ideas for Enhancement
- 🎨 Add pixel cat images to assets/cats/
- 🔍 Implement note search functionality
- 🏷️ Add tags or categories
- 📤 Export notes to text/markdown
- ☁️ Cloud sync capabilities
- 🔒 Note encryption
- 📎 Attachment support

### How to Contribute
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Code Style
- Follow PEP 8 guidelines
- Add docstrings to functions
- Keep functions focused and small
- Write descriptive commit messages
- Test your changes thoroughly

---

## 🎓 Conclusion

**WhiskerNotes** successfully demonstrates how a simple, focused application can provide an excellent user experience through:

### Key Achievements
✅ **Minimalist Design** - Clean interface without unnecessary clutter  
✅ **Cat-Themed Personality** - Delightful feedback without being overwhelming  
✅ **Reliable Persistence** - SQLite ensures notes are never lost  
✅ **Auto-Save** - Prevents accidental data loss  
✅ **Theme Support** - Comfortable viewing in any lighting condition  
✅ **Pure Python** - No JavaScript or web dependencies  

### Learning Outcomes
This project showcases:
- **MVC Architecture** - Separation of concerns between UI, logic, and data
- **Database Design** - Proper CRUD operations with SQLite
- **UI/UX Principles** - User-friendly interface with feedback
- **Event Handling** - Keyboard events, auto-save timers, button callbacks
- **Theme Management** - Dynamic color switching

### Future Vision
WhiskerNotes is designed to be:
- **Extensible** - Easy to add new features
- **Maintainable** - Clean, documented code
- **Educational** - Great for learning Python GUI development
- **Practical** - Actually useful for daily note-taking

### Perfect For
- 📚 **Students** learning Python GUI development
- 🎯 **Developers** needing a simple notes app
- 🎨 **Designers** appreciating minimalist aesthetics
- 🐱 **Cat lovers** who enjoy delightful interfaces

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 👤 Author

**Not-Animesh**
- GitHub: [@Not-Animesh](https://github.com/Not-Animesh)
- Repository: [NotesApplication](https://github.com/Not-Animesh/NotesApplication)

---

## 🙏 Acknowledgments

- CustomTkinter framework by Tom Schimansky
- Python Software Foundation
- The wonderful cat emoji designers 🐱🐾
- Everyone who loves cozy, minimal applications

---

<div align="center">

### Made with 💖 and 🐾

**Start writing your notes with WhiskerNotes today!**

*"A note a day keeps the chaos away"* - WhiskerNotes Philosophy

</div>