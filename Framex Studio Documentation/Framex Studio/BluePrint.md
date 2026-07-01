This will be a game engine built in python using PySide6 for the GUI and my own module, framex, that will be used for runtime.

***Canvas Blueprint***
![[BluePrint.canvas]]

## KeyBinds
### Global
-  Ctrl + S => Save everything that is flagged

---
## Logic
### Scene View
#### Scene selection
Whenever a scene is selected from the file explorer, the scene data in the **Scene View** is reset. All the objects are extracted from the data like this
```python
def _load_new_scene(self, new_scene: dict) -> None:
	self.current_scene = new_scene
	self.prefabs = self.current_scene.get("prefabs")
	
	# Update the widget
	self.update()
```

#### Moving / Adding items
Whenever a object from a loaded scene is changed (any values / properties) a signal is emitted to the **Main Window Manager** and a flag is set in **Scene Editor**. Whenever a new scene is selected, the program closes, or some other change happens, the **Scene Editor** saves the data, and unchecked the flag.

Adding items to a scene will be done by right clicking the **Scene View**, then a menu pops up with
- Add new game object
- Save scene

---
### Properties Panel
Whenever an item *(ALREADY IN THE SCENE)* is selected, a signal from **Scene View** is sent to the properties panel. The item is then displayed (all the attributes for the item).

---
### Hierarchy Panel
This will be sort of like a QTreeWidget for the objects in the **Scene View**.

---
### File Explorer
This is just a QTreeWidget that shows all the files / folders in the current project directory. 

Clicking a script or an image will open it. Click a prefab or scene selects it.

---
### File Preview
Whenever a folder is selected, the file preview gets the path and displays all the files. If a file is selected, the file preview shows the contents of the file's parent folder.

---
### File Actions
This will just contain buttons / actions that can be used to add files, scenes, objects, etc *(RIGHT CLICK)*.

---