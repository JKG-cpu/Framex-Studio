# Framex Studio - Roadmap
### *Of how I am gonna be building this project*

## Features

### What you see right away
1. **Scene View (LEFT ~75%)**
    - Select a scene ***(from a panel of scenes)***
    - Scene paused **(Edit Mode)**
        - Move things around ***(i.e objects)***
        - Drag and Drop Objects
        - Property Tab Updates ***(via clicked object)***
    - Scene unpaused **(Play Testing Mode)**
        - Game is playing 
        - Scripts execute
        - Block keyboard input to UI ***(leave certain keybinds???)***

2. **File System (BOTTOM FULL)**
    - Automatically read files
    - assets/
        - This will contain images provided by the user ***(like character.png)***
    - prefabs/
        - This will contain prefabs ***(like player.prefab)***
    - scenes/
        - This will contain scenes ***(like main_scene.json)***
    - scripts/
        - This will contain scripts tied to prefabs or scenes ***(like movement.py)***
        - Users can either create custom scripts or use premade scripts
            - In an external editor
            - Use a base class ***(like godot)***
    - Files / objects ***(like scenes and prefabs)*** will be json

3. **Properties Tab (RIGHT)**
    - Select a file or item to see its properties
    - What shows up
        - Object Name / ID
        - Transform 
            - Position: [x, y]
            - Rotation: 0
            - Scale: [1, 1]
        - Sprite
            - Image Path
            - ***DRAG AND DROPPABLE***
        - Attributes
            - Attributes in selected image
            - [+ Add Attribute]
        - Script Path
            - ***DRAG AND DROPPABLE***

### Details

1. Attributes
    - List of attributes *(still brainstorming)*
