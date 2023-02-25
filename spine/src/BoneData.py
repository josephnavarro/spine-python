#! usr/bin/env python3

class BoneData:
    __slots__ = [
        "name",
        "parent",
        "length",
        "x",
        "y",
        "rotation",
        "scaleX",
        "scaleY",
        "flipY",
    ]

    def __init__(self, name: str):
        self.name: str = name
        self.parent = None
        self.length: float = 0.0
        self.x: float = 0.0
        self.y: float = 0.0
        self.rotation: float = 0.0
        self.scaleX: float = 1.0
        self.scaleY: float = 1.0
        self.flipY: bool = False
