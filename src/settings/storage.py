import json
from pathlib import Path

__all__ = ["Storage"]

class Storage:
    def __init__(self) -> None:
        self._head_path: Path = Path(__file__)
