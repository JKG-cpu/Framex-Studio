from dataclasses import dataclass

__all__ = [
    "File", "Folder",
    "Image"
]

@dataclass
class File:
    name: str
    size: str

@dataclass
class Folder:
    name: str
    item_count: int
    total_size: str

@dataclass
class Image(File):
    width: int
    height: int
    format: str
