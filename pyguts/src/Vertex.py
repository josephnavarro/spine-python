#! usr/bin/env python3
from .Color import Color
from .TextureCoordinates import TextureCoordinates


class Vertex:
    __slots__ = [
        "color",
        "texCoords",
    ]
    def __init__(self):
        self.color = Color()
        self.texCoords = TextureCoordinates()