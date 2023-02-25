#! usr/bin/env python3

class BaseAtlasRegion:
    __slots__ = [
        "name",
        "x",
        "y",
        "width",
        "height",
        "width",
        "offsetX",
        "offsetY",
        "originalWidth",
        "originalHeight",
        "index",
        "rotate",
        "flip",
        "splits",
        "pads",
    ]

    def __init__(self):
        self.name = None
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0
        self.offsetX = 0.0
        self.offsetY = 0.0
        self.originalWidth = 0
        self.originalHeight = 0
        self.index = 0
        self.rotate = False
        self.flip = False
        self.splits = []
        self.pads = []
