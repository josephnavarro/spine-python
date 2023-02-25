#! usr/bin/env python3

class Circle:
    __slots__ = [
        "x",
        "y",
        "r",
        "color",
    ]

    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r
        self.color = (0, 255, 0, 255)
