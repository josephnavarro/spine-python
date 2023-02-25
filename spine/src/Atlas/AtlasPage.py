#! usr/bin/env python3

class AtlasPage:
    __slots__ = [
        "name",
        "format",
        "minFilter",
        "magFilter",
        "uWrap",
        "vWrap",
    ]

    def __init__(self):
        self.name = None
        self.format = None
        self.minFilter = None
        self.magFilter = None
        self.uWrap = None
        self.vWrap = None
