# Background and Layout Fixes

## Overview
Fixed the search/filter collision issue and added background image support using assets from the `assets/backgrounds/` directory.

---

## 🔧 Layout Fixes

### Problem
The search frame and category filter frame were both using `row=1`, causing them to overlap and collide.

### Solution
Reorganized the grid layout to properly separate elements:

| Element | Row | Spacing |
|---------|-----|---------|
| Header | 0 | Standard padding |
| Search Frame | 1 | Bottom: 8px (sm) |
| Category Filter | 2 | Top: 16px (md), Bottom: 8px (sm) |
| Scrollable Frame | 3 | Standard padding |
| Status Message | 4 | Bottom: 16px (md) |

### Changes Made

1. **Search Frame** (Row 1)
   - Moved to row 1
   - Bottom padding: `spacing["sm"]` (8px)
   - Contains: Search bar + Sort dropdown

2. **Category Filter Frame** (Row 2)
   - Moved to row 2 (was row 1)
   - Top padding: `spacing["md"]` (16px) - **Proper separation from search**
   - Bottom padding: `spacing["sm"]` (8px)
   - Contains: Category filter buttons (All, Personal, Study, Ideas, Work, Other)

3. **Scrollable Frame** (Row 3)
   - Updated from row 2 to row 3
   - Contains: Note cards

4. **Status Message** (Row 4)
   - Updated from row 3 to row 4
   - Contains: Status notifications

5. **Grid Configuration**
   - Updated `grid_rowconfigure(3, weight=1)` to account for new row structure

---

## 🎨 Background Image Support

### Implementation
Added background image support using a Canvas-based approach that works with CustomTkinter.

### Background Selection
The application automatically selects background images based on theme:

- **Light Theme**: `bg_pink_gradient.jpg`
- **Dark Theme**: `bg_star_pattern.png`

### Features

1. **Automatic Resizing**
   - Background image resizes with window
   - Uses high-quality LANCZOS resampling
   - Maintains aspect ratio

2. **Canvas-Based Approach**
   - Uses Tkinter Canvas placed behind all widgets
   - Automatically updates on window resize
   - Non-intrusive implementation

3. **Theme-Aware**
   - Different backgrounds for light/dark themes
   - Seamlessly switches when theme changes

### Code Structure

```python
# In main.py
def _setup_background(self):
    """Setup background image using canvas"""
    - Loads image from Theme.get_background_image()
    - Creates canvas behind all widgets
    - Handles resize events
    - Updates background dynamically
```

```python
# In themes.py
@classmethod
def get_background_image(cls):
    """Get background image based on current theme"""
    - Returns appropriate background path
    - Light theme: pink gradient
    - Dark theme: star pattern
```

---

## 📐 Spacing Improvements

### Search and Filter Separation
- **Before**: Both on row 1, overlapping
- **After**: 
  - Search on row 1 with 8px bottom padding
  - Filter on row 2 with 16px top padding
  - **Total separation: 24px** (proper visual breathing room)

### Visual Hierarchy
1. Header (row 0) - App title and buttons
2. Search (row 1) - Search and sort controls
3. Filters (row 2) - Category selection
4. Content (row 3) - Note cards
5. Status (row 4) - Feedback messages

---

## ✅ Benefits

1. **No More Collision**: Search and filter are properly separated
2. **Better UX**: Clear visual hierarchy and spacing
3. **Beautiful Backgrounds**: Asset backgrounds enhance visual appeal
4. **Theme Integration**: Backgrounds match theme automatically
5. **Responsive**: Background resizes with window
6. **Performance**: Efficient canvas-based rendering

---

## 🎯 Available Background Assets

The application uses these background assets:

- `bg_pink_gradient.jpg` - Used for light theme
- `bg_star_pattern.png` - Used for dark theme
- `bg_lavender_gradient.jpg` - Available for future use
- `bg_pink_grid.png` - Available for future use

---

## 🔄 Theme Switching

When the theme is toggled:
1. Background image automatically changes
2. Canvas updates with new image
3. All widgets maintain proper spacing
4. No layout shifts or collisions

---

## 📝 Technical Details

### Grid Layout Structure
```
Row 0: Header Frame
  ├─ Title
  └─ Buttons (Theme, New Note)

Row 1: Search Frame
  ├─ Search Entry
  └─ Sort Dropdown

Row 2: Category Filter Frame
  └─ Category Buttons (All, Personal, Study, Ideas, Work, Other)

Row 3: Scrollable Frame (weight=1)
  └─ Note Cards

Row 4: Status Label
  └─ Status Messages
```

### Background Canvas
- Placed at z-index 0 (behind all widgets)
- Uses `place()` with `relwidth=1, relheight=1`
- Updates on `<Configure>` event
- Maintains image reference to prevent garbage collection

---

*Last Updated: Background and layout fixes completed*

