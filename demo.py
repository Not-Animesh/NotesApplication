#!/usr/bin/env python3
"""
WhiskerNotes Demo Script
Demonstrates the core functionality without GUI
"""

from database import Database
from themes import Theme, CAT_MESSAGES

def main():
    print("=" * 50)
    print("🐱 WhiskerNotes - Demo Script")
    print("=" * 50)
    
    # Initialize database
    print("\n1. Initializing database...")
    db = Database("demo_whiskernotes.db")
    print("   ✓ Database initialized")
    
    # Create sample notes
    print("\n2. Creating sample notes...")
    note1_id = db.create_note(
        "Welcome to WhiskerNotes", 
        "This is your first note! WhiskerNotes is a cozy cat-themed notes app."
    )
    print(f"   ✓ {CAT_MESSAGES['note_created']}")
    
    note2_id = db.create_note(
        "Shopping List",
        "- Milk\n- Bread\n- Cat treats\n- Coffee"
    )
    print(f"   ✓ {CAT_MESSAGES['note_created']}")
    
    note3_id = db.create_note(
        "Project Ideas",
        "1. Build a cat-themed todo app\n2. Create pixel art cats\n3. Learn Python GUI development"
    )
    print(f"   ✓ {CAT_MESSAGES['note_created']}")
    
    # Display all notes
    print("\n3. Displaying all notes...")
    notes = db.get_all_notes()
    print(f"   Found {len(notes)} notes:")
    for note in notes:
        print(f"\n   📝 {note['title']}")
        content_preview = note['content'][:50] + "..." if len(note['content']) > 50 else note['content']
        print(f"      {content_preview}")
        print(f"      🐾 Updated: {note['updated_at']}")
    
    # Update a note
    print("\n4. Updating a note...")
    db.update_note(
        note1_id,
        "Welcome to WhiskerNotes (Updated)",
        "This note has been updated! Auto-save keeps your changes safe."
    )
    print(f"   ✓ {CAT_MESSAGES['note_saved']}")
    
    # Search notes
    print("\n5. Searching notes...")
    results = db.search_notes("cat")
    print(f"   Search for 'cat' found {len(results)} results:")
    for result in results:
        print(f"   - {result['title']}")
    
    # Theme demonstration
    print("\n6. Demonstrating themes...")
    print(f"   Current theme: {Theme.current_theme}")
    colors = Theme.get_colors()
    print(f"   Background: {colors['bg']}")
    print(f"   Accent: {colors['accent']}")
    
    Theme.toggle_theme()
    print(f"\n   Switched to: {Theme.current_theme}")
    colors = Theme.get_colors()
    print(f"   Background: {colors['bg']}")
    print(f"   Accent: {colors['accent']}")
    
    # Delete a note
    print("\n7. Deleting a note...")
    db.delete_note(note2_id)
    print(f"   ✓ {CAT_MESSAGES['note_deleted']}")
    
    # Final count
    remaining = db.get_all_notes()
    print(f"\n8. Final status:")
    print(f"   {len(remaining)} notes remaining")
    
    print("\n" + "=" * 50)
    print("✅ Demo completed successfully!")
    print("Run 'python main.py' to launch the full GUI app")
    print("=" * 50)
    
    # Cleanup demo database
    import os
    os.remove("demo_whiskernotes.db")
    print("\n🧹 Demo database cleaned up")

if __name__ == "__main__":
    main()
