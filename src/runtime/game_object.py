# ================
# GameObject Class
# ================
from PySide6.QtCore import QPointF
from PySide6.QtGui import QColor
from os.path import join, isfile

from .components import *

__all__ = ["BaseObject"]

class BaseObject:
    def __init__(self) -> None:
        self.transform = Transform()
        self._name: str = "Object"
        self._tags: set[str] = set()
        self._active: bool = True
        self._selected: bool = False
        self._layer: int = 0
        self._color: str = "#FFFFFF"
        self._image_path: str | None = None
        self._script_path: str | None = None
    
    # Data
    #region
    def to_dict(self) -> dict:
        return {
            "name": self._name,
            "tags": list(self._tags),
            "active": self._active,
            "layer": self._layer,
            "color": self._color,
            "image_path": self._image_path,
            "script_path": self._script_path,
            "transform": self.transform.to_dict()
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "BaseObject":
        b = cls()
        b._name = data["name"]
        b._tags = data["tags"]
        b._active = data["active"]
        b._selected = False
        b._layer = data["layer"]
        b._color = data["color"]
        b._image_path = data["image_path"]
        b._script_path = data["script_path"]
        b.transform = Transform.from_dict(data["transform"])
        return b
    #endregion

    # Properties
    #region
    @property
    def name(self) -> str: return self._name

    @property
    def tag(self) -> frozenset[str]: return frozenset(self._tags)
    
    @property
    def active(self) -> bool: return self._active

    @property
    def selected(self) -> bool: return self._selected

    @property
    def layer(self) -> int: return self._layer
    
    @property
    def color(self) -> str: return self._color

    # Transform
    @property
    def position(self) -> QPointF: return self.transform.position

    @property
    def rotation(self) -> float: return self.transform.rotation

    @property
    def scale(self) -> QPointF: return self.transform.scale

    @property
    def size(self) -> QPointF: return self.transform.size

    # Paths
    @property
    def image(self) -> str: return self._image_path

    @property 
    def script(self) -> str: return self._script_path
    #endregion

    # Setter
    #region
    @name.setter
    def name(self, value: str) -> None:
        if isinstance(value, str):
            self._name = value
        
        else:
            raise TypeError(f"Name must be a str, got {type(value)}")

    @tag.setter
    def tag(self, value: str | list[str] | set[str]) -> None:
        if isinstance(value, str):
            self._tags = {value.strip().lower()}
        
        elif isinstance(value, (list, set)):
            self._tags = {v.strip().lower() for v in value}

        else:
            raise TypeError(f"Tag must be str, list, or set, got {type(value)}")

    @selected.setter
    def selected(self, selected: bool) -> None:
        if isinstance(selected, bool):
            self._selected = selected
        
        else:
            raise TypeError(f"Selected must be a bool, got {type(selected)}")

    @layer.setter
    def layer(self, value: int) -> None:
        if isinstance(value, int):
            self._layer = value
        
        else:
            raise TypeError(f"Layer must be an int, got {type(value)}")
    
    @color.setter
    def color(self, value: str) -> None:
        if isinstance(value, str) and value.startswith("#") and len(value) == 7:
            self._color = value

        else:
            raise TypeError(f"Value must be a hex color (str), got {type(value)}, value: {value}")
    
    @image.setter
    def image(self, *path: str) -> None:
        self._image_path = join(*path)

        if not isfile(self._image_path):
            raise FileNotFoundError(f"File path: {self._image_path} not found.")
        
    @script.setter
    def script(self, *path: str) -> None:
        self._script_path = join(*path)

        if not isfile(self._script_path):
            raise FileNotFoundError(f"File path: {self._script_path} not found.")
    #endregion

    # Other Methods
    #region
    def toggle_active(self) -> None: self._active = not self._active
    def toggle_selected(self) -> None: self._selected = not self._selected

    def move_to(self, x: int | float, y: int | float) -> None: 
        if isinstance(x, (int, float)) and isinstance(y, (int, float)):
            self.transform.position = QPointF(x, y)

        else:
            raise TypeError(f"X and Y must be ints or floats, got x: {type(x)} and y: {type(y)}")

    def rotate(self, rotation: int | float) -> None:
        if isinstance(rotation, (int, float)):
            self.transform.rotation = rotation

        else:
            raise TypeError(f"Rotation must be an int or float, got {type(rotation)}")

    def scale_to(self, w: int | float, h: int | float) -> None:
        if isinstance(w, (int, float)) and isinstance(h, (int, float)):
            self.transform.scale = QPointF(w, h)
        
        else:
            raise TypeError(f"W and H must be ints or floats, got w: {type(w)} and h: {type(h)}")
    
    def resize(self, w: int | float, h: int | float) -> None:
        if isinstance(w, (int, float)) and isinstance(h, (int, float)):
            self.transform.size = QPointF(w, h)
        
        else:
            raise TypeError(f"W and H must be ints or floats, got w: {type(w)} and h: {type(h)}")
    #endregion
