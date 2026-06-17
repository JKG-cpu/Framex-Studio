import json
from pathlib import Path

__all__ = ["Storage"]

def load(file_path: str) -> dict:
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    
    except FileNotFoundError:
        raise FileNotFoundError(f"Path {file_path} not found!")

    except Exception as e:
        raise Exception(f"Exception occurred when loading data from {file_path}. Exception: {e}")

def save(file_path: str, data: dict) -> None:
    try:
        with open(file_path, "w") as f:
            json.dump(data, f)

    except FileNotFoundError:
        raise FileNotFoundError(f"Path {file_path} not found!")

    except Exception as e:
        raise Exception(f"Exception occurred when saving data to {file_path}. Exception: {e}")

class Color:
    def __init__(self, head_path: Path) -> None:
        self._file_path: str = head_path.parent / "color.json"
        self.data = load(self._file_path)

        self.dirty = False

    #region
    @property
    def mode(self) -> str:
        return self.data.get("mode")

    @property
    def scene_view(self) -> dict:
        return self.data.get("scene_view").get(self.data.get("mode", "dark"))

    @property
    def file_system(self) -> dict:
        return self.data.get("file_system").get(self.data.get("mode", "dark"))
    #endregion

    #region
    @mode.setter
    def mode(self, value: str) -> None:
        value = value.lower()

        if value == ("dark", "light"):
            self.data["mode"] = value
            self.dirty = True
    #endregion

    #region
    def apply_changes(self) -> None:
        if self.dirty:
            save(self._file_path, self.data)
    #endregion

class Storage:
    def __init__(self) -> None:
        self._head_path: Path = Path(__file__)

        self._color: Color = Color(self._head_path)

    @property
    def color(self) -> Color:
        return self._color

    def update_all(self) -> None:
        self._color.apply_changes()
