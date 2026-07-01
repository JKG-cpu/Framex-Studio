from dataclasses import dataclass

__all__ = ["File", "Folder", "Image", "Scene", "Script", "Prefab"]


# Files
@dataclass
class File:
    name: str
    extension: str


# Folders
@dataclass
class Folder:
    name: str
    item_count: int


# Images
@dataclass
class Image(File):
    width: int
    height: int
    type: str


# Scenes
@dataclass
class Scene(File):
    pass


# Scripts
@dataclass
class Script(File):
    language: str = ".py"
    # Get the description by optionally setting the first line of code in the script
    # To be a docstring ("""What this code does""")
    # description: str


# Prefabs
@dataclass
class Prefab(File):
    pass
