# 🚀 WhiskerNotes Quick Start Guide

Get up and running with WhiskerNotes in under 2 minutes!

## Installation

### Option 1: Using pip (Recommended)

```bash
# Clone the repository
git clone https://github.com/Not-Animesh/NotesApplication.git
cd NotesApplication

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

### Option 2: Using Virtual Environment

```bash
# Clone the repository
git clone https://github.com/Not-Animesh/NotesApplication.git
cd NotesApplication

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

## First Steps

### 1. Launch WhiskerNotes
```bash
python main.py
```

### 2. Create Your First Note
1. Click the **"+ New Note"** button
2. Type a title (or leave it for "Untitled Note")
3. Write your content
4. Wait 2 seconds - it auto-saves!
5. Click **"← Back"** to see your note

### 3. Try the Features

**Edit a note:**
- Click **"Edit"** on any note card
- Make your changes
- Auto-saves as you type!

**Delete a note:**
- Click **"Delete"** on any note card
- Note is removed instantly

**Toggle theme:**
- Click the **🌙/☀️** button in the top-right
- Enjoy dark mode for night-time writing

## Troubleshooting

### "No module named 'tkinter'"
**Solution:** Install tkinter for your system:
- **Ubuntu/Debian:** `sudo apt-get install python3-tk`
- **Fedora:** `sudo dnf install python3-tkinter`
- **macOS:** Tkinter comes with Python (use official Python.org installer)
- **Windows:** Tkinter comes with Python (ensure "tcl/tk" is checked during install)

### "No module named 'customtkinter'"
**Solution:** Install CustomTkinter:
```bash
pip install customtkinter
```

### Application won't launch
**Check Python version:**
```bash
python --version  # Should be 3.8 or higher
```

**Verify installation:**
```bash
python -c "import customtkinter; print('OK')"
```

## Usage Tips

### Keyboard Shortcuts
- **Tab** - Move between title and content
- **Ctrl/Cmd + A** - Select all text
- **Ctrl/Cmd + C** - Copy
- **Ctrl/Cmd + V** - Paste
- **Ctrl/Cmd + X** - Cut

### Auto-Save Tips
- Auto-save happens 2 seconds after you stop typing
- Only works for existing notes (not brand new ones)
- Manual save button available anytime
- Look for "Auto-saved 🐾" message at bottom

### Organizing Notes
- Notes appear in reverse chronological order (newest first)
- Recently edited notes move to the top
- Use descriptive titles for easy scanning
- Keep individual notes focused on one topic

## Demo Mode

Want to see it in action without the GUI?

```bash
python demo.py
```

This runs a command-line demo showing:
- Creating notes
- Searching notes
- Updating notes
- Deleting notes
- Theme switching

## What's Next?

Now that you're set up:
1. 📝 Create some notes
2. 🎨 Try both light and dark themes
3. 🔍 Experiment with editing and deleting
4. 😺 Enjoy the cat-themed messages!

## Need Help?

- 📖 Read the full [README.md](README.md)
- 🎨 Check out [VISUAL_GUIDE.md](VISUAL_GUIDE.md)
- 🐛 Report issues on GitHub
- ⭐ Star the repo if you like it!

---

**Happy note-taking with WhiskerNotes! 🐱🐾**
