
## Overall
I created a **Theme Manager** that will handle loading in color settings.

---
## Options Panel
Nothing for the options panel was planned yet...

---
## Hierarchy Panel
Nothing for the hierarchy panel was planned yet...

---
## Scene View
### Grid
I created a grid like structure with X and Y bars. Defaulted to having (0, 0) appear in the "top-left" of the grid (you can scroll to go into the negative X and Y values).

I implemented panning, but decided not to allow zooming at the moment, problems arose with the zooming moving to fast + the numbers weren't always "good looking" (decimal values almost everywhere).

Gave color values for each X and Y line. I added a bold color for marking where (0, 0) is. I set the default zoom value to 50 units (meaning each "section" in between lines are 50 units by 50 units).
### Bars
I have 3 different bars set inside the scene view.
1. Top Bar
	1. Currently just holds "Scene View"
2. Edit Bar
	1. This is where you can run the game
	2. Was thinking about, when the game is being run, I create a separate thread for compiling / running the game. While the thread is active, I change the play button to a stop button. If clicked => I stop the thread.
3. Bottom Bar
	1. Current just the function "Return to (0, 0)" is there

## Game Objects / Scene Loading + Saving
I added a few methods for loading scenes + objects. Currently, to load a new scene, you just pass in the scene data *(dict)*.
```python
def select_scene(self, scene: dict) -> None:
	if scene is self.scene:
		# Prevent reloading the same scene quickly
		self.update()
		return
	
	# Sets the scene data
	self.scene = scene
	
	# Resets the objects
	self.objects = self._load_scene_objects()
	
	# Update widget
	self.update()
```

`self._load_scene_objects()` just returns a list of game objects (from the data) which is already parsed from the **Scene Serializer**.  Current fallback is just a blank list.
```python
def _load_scene_objects(self) -> None:
	return self.scene.get("objects", []) if self.scene else []
```

The current way I am handling scene saving is (when the user presses Ctrl + S) I send out a signal that is received in the **Main Window** class, then sent over to the **Scene Editor** which is then saved (after being serialized).

## Ideas to Implement?
I was thinking of adding a handful of helpful methods (like returning to (0, 0)) to the scene view bottom bar.
- Return to (0, 0)

---
## Properties Panel
Nothing for the properties panel was planned yet

---
## File System Panel
The file system panel is separated *(currently)* into two widgets.
### File Explorer
 I used PySide6's QTreeWidget to build the files / folders layout. Then I just plugged in the folders I had via a file path ***(WILL BE AUTO SCANNED AND AUTO DECIDED LATER)*** and used the pathlib module to iterate through all the directories + files.
 ```python
 def _load_entries(self, path: Path = None) -> list:
	path = path or self.file_path
	folders = []
	files = []

	for entry in sorted(path.iterdir()):
		if entry.is_dir():
			folders.append(
				(entry.stem, self._load_entries(entry), "Folder", entry)
			)
	
		else:
		files.append(
			(entry.stem, str(entry.suffix) if entry.suffix else "None", entry)
		)
	
	# Return folders and files
	return folders + files
 ```

Each item in `files` is a tuple of (file name, file extension, path). Each item in `folders` is a tuple of (file name, children, path).

In order to load it, it is pretty simple. I just needed to iterate over each entry from `_load_entries(...)`
```python
def _build_tree(
	self, 
	parent, 
	entries: list[tuple[str, str, str] | tuple[str, str]]
	) -> None:
	
	for entry in entries:
		name, content, path = entry
	
		if isinstance(content, list):
			item = QTreeWidgetItem(parent, [name])
			item.setChildIndicatorPolicy(
				QTreeWidgetItem.ChildIndicatorPolicy.ShowIndicator
			)
			item.setForeground(0, QColor(self.theme["folder"]))
			if content: item.setExpanded(True)
			item.setData(0, Qt.UserRole, path)
			self._build_tree(item, content)
	
		else:
			item = QTreeWidgetItem(parent, [name])
			item.setData(0, Qt.UserRole, path)
			item.setForeground(0, QColor(self.theme["file"]))
```
### File / Folder Preview
For the folder preview, I decided to try to replicate what some game engines are currently using. Where if a folder is clicked, you would see all the children (files) inside of that folder.

Currently, I created some pixel art for some file icons (very rough, will definitely redraw) and just added them to a widget registry, which (currently) uses the file extension to determine which icon to use.

Ideas for current images (some not drawn)
-  Basic File, Text Files, Markdown Files, Image Files
-  Script File (.py)
-  Scene File (.scene, but really .json)
-  Prefab (.prefab, but really .json)

The whole file preview isn't that great. I will most definitely refactor a lot of it in the future.

---
## What's Next?
### Creating Game Objects

---