# Framex Studio - Roadmap
### *Of how I am gonna be building this project*

## Features

### What you see right away

1. **Scene View (LEFT ~75%)**
    - Double-click a scene file in File System to load it
    - **Edit Mode (Paused)**
        - Click object → select (highlight in viewport)
        - Drag object → move (updates Transform.position)
        - Drag prefab from File System → create new object in scene
        - Right-click → delete, duplicate
        - Properties Tab updates with selected object
        - Grid displayed (like pygame-ce, top-left origin)
        - Rendering done with **PySide6 QPainter**
    - **Play Mode (Playtest)**
        - Game runs in **new pygame-ce window**
        - All scripts execute (_ready, _process, etc.)
        - Game receives keyboard/mouse input
        - Close window or press ESC → return to Edit Mode
        - Generated `.py` file runs standalone

2. **File System (BOTTOM, Full Width, Resizable)**
    - Auto-reads project structure
    - Folders: assets/, prefabs/, scenes/, scripts/
    - Drag & drop prefabs into Scene View to create objects
    - Drag & drop scripts onto objects to attach them
    - Right-click files → Open, Delete, Rename, Create New
    
    **File Types:**
    - assets/ → PNG/JPG images
    - prefabs/ → .prefab (JSON format)
    - scenes/ → .scene (JSON format)
    - scripts/ → .py (Python files)

3. **Properties Tab (RIGHT, ~20%)**
    - Shows selected object or file properties
    - **For GameObjects:**
        - Object ID
        - Transform
            - Position [x, y]
            - Rotation (degrees)
            - Scale [sx, sy]
        - Sprite
            - Image Path (drag & drop to change)
            - Frame Width / Height (if spritesheet)
        - Components
            - [Currently attached components list]
            - [+ Add Component] button
        - Script
            - Script Path (drag & drop to attach)
    - **For Files:**
        - File name, path, size, last modified

---

## Details

### 1. Scene View

#### Editing
- **Canvas Rendering:** Use `QWidget` with `paintEvent()` override
- **Coordinates:** Top-left origin (0, 0) like pygame-ce
- **Grid Display:** Draw grid lines for snapping (optional snapping)
- **Selection:** Click objects to select, draw selection box around selected
- **Dragging:** Mouse move while selected updates `Transform.position`
- **Drag & Drop:** Accept prefab files from File System, create objects
- **Zoom/Pan:** Mouse wheel to zoom, middle-click drag to pan (optional)
- **Event Handling:**
  - `mousePressEvent()` → select object at position
  - `mouseMoveEvent()` → drag selected object
  - `wheelEvent()` → zoom
  - `dragEnterEvent()` / `dropEvent()` → accept prefab drops

#### Runtime / Play Testing
- **Separate Process:** Use `subprocess.Popen()` to launch generated `.py` file
- **Pygame-ce Window:** Game runs in new window, independent from editor
- **Generated Code:** Exporter creates runnable `.py` with scene data + user scripts
- **No Communication:** Editor and runtime don't communicate (clean separation)

---

### 2. File System

- **Tree Widget:** Use `QTreeWidget` or custom `QAbstractItemModel`
- **Auto-Scan:** On project load, scan folders and populate tree
- **Icons:** Show folder icon, `.scene` icon, `.prefab` icon, `.py` icon
- **Drag & Drop:**
  - Drag prefabs → drop in Scene View (create object)
  - Drag scripts → drop on object in Properties (attach script)
- **Context Menu:** Right-click → New File, Delete, Rename, Properties
- **Double-Click:** 
  - `.scene` file → load in Scene View
  - `.py` file → open in external editor (optional)

---

### 3. Properties Tab

- **Scroll Area:** `QScrollArea` with form layout for editing
- **Dynamic Fields:** Show different fields based on selected object type
- **For GameObjects:**
  - Object ID: `QLineEdit` (read-only or editable?)
  - Transform Position X/Y: `QSpinBox` or `QDoubleSpinBox`
  - Transform Rotation: `QDoubleSpinBox`
  - Transform Scale X/Y: `QDoubleSpinBox`
  - Sprite Image Path: `QLineEdit` + drag & drop
  - Sprite Frame Size: `QSpinBox`
  - Components List: `QListWidget` with component names
  - Add Component Button: `QPushButton` + dialog to select component type
  - Script Path: `QLineEdit` + drag & drop
- **Live Updates:** Changes in Properties immediately update object and redraw Scene View
- **For Files:** Show read-only info (name, path, size, modified date)

---

## What I will need

### Temporary File Structure

```
framex_studio/
├── main.py                          # Entry point
├── src/
│   ├── editor/
│   │   ├── __init__.py
│   │   ├── main_window.py              # Main PySide6 window (layout)
│   │   ├── panels/
│   │   │   ├── __init__.py
│   │   │   ├── scene_view.py           # QWidget: QPainter rendering + input
│   │   │   ├── file_system_panel.py    # QTreeWidget: folder tree
│   │   │   └── properties_panel.py     # QWidget: object properties form
│   │   ├── exporter.py                 # Generate .py files for runtime
│   │   └── scene_editor.py             # Manages current open scene
│   ├── runtime/                         # (Separate from editor, used in exported .py)
│   │   ├── __init__.py
│   │   ├── game.py                     # pygame-ce Game class
│   │   ├── scene.py                    # RuntimeScene base class
│   │   ├── game_object.py              # GameObject class
│   │   ├── components/
│   │   │   ├── __init__.py
│   │   │   ├── transform.py            # Transform component
│   │   │   ├── sprite.py               # Sprite component
│   │   │   └── script.py               # Script component
│   │   └── behavior.py                 # Behavior base class (user scripts inherit)
│   ├── serialization/
│   │   ├── __init__.py
│   │   ├── scene_serializer.py         # Save/load .scene JSON
│   │   └── prefab_serializer.py        # Save/load .prefab JSON
│   ├── _framex_build/                  # (Generated, ignore)
│   │   └── run_*.py
│   └── resources/
│       └── icons/                      # UI icons (optional)
```

### 1. Scene View (scene_view.py)

**What it needs:**
- `SceneViewport(QWidget)` class
- `paintEvent()` → draw grid, objects, selection box
- `mousePressEvent()` → select object at click position
- `mouseMoveEvent()` → drag selected object
- `wheelEvent()` → zoom in/out
- `dragEnterEvent()` / `dropEvent()` → accept prefab drops
- Methods:
  - `load_scene(scene_path)` → deserialize and display
  - `add_object(prefab_path, position)` → create object in scene
  - `get_object_at(x, y)` → collision detection for clicking
  - `draw_grid(painter)` → draw grid lines
  - `draw_object(painter, game_object)` → render single object
  - `draw_selection(painter)` → highlight selected object

**Emits Signals:**
- `object_selected(game_object)` → tells Properties Tab to update
- `object_moved(game_object)` → tells Properties Tab to update position
- `objects_changed()` → tells File System to refresh (optional)

---

### 2. File System Panel (file_system_panel.py)

**What it needs:**
- `FileSystemPanel(QWidget)` class
- `QTreeWidget` for folder hierarchy
- Auto-populate on init from project folder
- Methods:
  - `load_project(project_path)` → scan and display folders
  - `get_selected_file()` → return selected file path
  - `refresh()` → re-scan folders
  - `setup_context_menu()` → right-click options
- Events:
  - `itemDoubleClicked()` → load `.scene` files or open `.py` files
  - `dragEnter/dragMove` → show drop indicator for Scene View
  - `drop()` → emit signal with dragged file path

**Emits Signals:**
- `scene_selected(scene_path)` → tells Scene View to load
- `file_dragged(file_path)` → for drag & drop
- `context_menu_action(action, file_path)` → for delete, rename, etc.

---

### 3. Properties Panel (properties_panel.py)

**What it needs:**
- `PropertiesPanel(QWidget)` class
- `QScrollArea` + `QFormLayout` for dynamic fields
- Methods:
  - `show_object_properties(game_object)` → build form for object
  - `show_file_properties(file_path)` → build form for file
  - `create_transform_fields()` → Position X/Y/Z spinboxes
  - `create_sprite_fields()` → Image path + frame size
  - `create_script_field()` → Script path + drag & drop
  - `create_components_list()` → List of attached components
- Events:
  - Field changes → emit signals to update object + Scene View

**Emits Signals:**
- `property_changed(game_object, property_name, new_value)` → update object
- `object_needs_redraw()` → tell Scene View to refresh

**Accepts Signals:**
- `object_selected(game_object)` from Scene View

---

## Data Flow Example

**User double-clicks a `.scene` file:**
1. File System emits `scene_selected('scenes/level_1.scene')`
2. Main Window receives signal
3. Calls `scene_editor.load_scene('scenes/level_1.scene')`
4. Scene Editor deserializes JSON, creates GameObjects
5. Scene View receives objects, redraws with `paintEvent()`

**User clicks object in Scene View:**
1. Scene View `mousePressEvent()` detects click
2. Calls `get_object_at(x, y)` to find object
3. Emits `object_selected(game_object)` signal
4. Properties Panel receives signal
5. Creates form fields for object's Transform, Sprite, etc.
6. User edits Position X
7. Properties Panel emits `property_changed(object, 'position.x', 100)`
8. Scene View updates object and redraws

**User drags prefab into Scene View:**
1. File System drag starts, emits `file_dragged('prefabs/player.prefab')`
2. Scene View `dragEnterEvent()` accepts drop
3. User drops on canvas
4. Scene View `dropEvent()` creates new object from prefab
5. Calls `scene_editor.add_object(prefab_path, mouse_pos)`
6. Scene Editor instantiates object
7. Scene View redraws
8. Emits `object_selected(new_object)` for Properties to show

---

## Key Classes to Create

### Scene Editing

```python
# editor/scene_editor.py
class SceneEditor:
    def __init__(self):
        self.current_scene = None
        self.game_objects = []
    
    def load_scene(self, scene_path):
        # Deserialize .scene JSON
        # Create GameObjects
    
    def add_object(self, prefab_path, position):
        # Create object from prefab
        # Add to scene
    
    def remove_object(self, game_object):
        # Delete object from scene
    
    def save_scene(self, scene_path):
        # Serialize to JSON
```

### Runtime Export

```python
# editor/exporter.py
class SceneExporter:
    def export_scene(self, scene_path, output_dir):
        # Read .scene JSON
        # Generate .py file with scene data + imports
        # Save to output_dir/run_*.py
    
    def export_all(self, project_path, output_dir):
        # Export all scenes
```

---

## Next Steps

1. **Create main window layout - DONE** with 3 panels (Scene View, File System, Properties)
2. **Implement Scene View - DONE** with QPainter + basic object rendering
3. **Implement File System - IN PROGRESS** with QTreeWidget auto-scan
4. **Implement Properties Panel** with form fields
5. **Wire up signals/slots** to connect panels
6. **Build serialization** (load/save .scene and .prefab JSON)
7. **Implement exporter** to generate .py files
8. **Test with simple project** (create scene, add objects, play)