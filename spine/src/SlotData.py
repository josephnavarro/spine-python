#! usr/bin/env python3
from .BoneData import BoneData


class SlotData:
    __slots__ = [
        "name",
        "boneData",
        "r",
        "g",
        "b",
        "a",
        "attachmentName",
    ]

    def __init__(self, name: str, boneData: BoneData):
        if not name:
            raise Exception('Name cannot be None.')

        if not boneData:
            raise Exception('boneData cannot be None.')

        self.name: str = name
        self.boneData: BoneData = boneData
        self.r: int = 255
        self.g: int = 255
        self.b: int = 255
        self.a: int = 255
        self.attachmentName: (str | None) = None

    def setColor(self, r: int, g: int, b: int, a: int) -> None:
        self.r = r
        self.g = g
        self.b = b
        self.a = a
