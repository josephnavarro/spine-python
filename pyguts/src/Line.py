#! usr/bin/env python3
import pygame


class Line:
    __slots__ = [
        "x",
        "y",
        "x1",
        "x2",
        "length",
        "rotation",
        "color",
        "texture",
        # TODO: Init?
        "xScale",
        "yScale",
        "y1",
        "y2",
    ]

    def __init__(self, length):
        self.x = 0.0
        self.y = 0.0
        self.x1 = 0.0
        self.x2 = 0.0
        self.length = length
        self.rotation = 0.0
        self.color = (255, 0, 0, 255)
        self.texture = pygame.Surface((640, 480), pygame.SRCALPHA, 32)
        pygame.draw.rect(self.texture, (255, 255, 0, 64), (0, 0, self.texture.get_width(), self.texture.get_height()), 1)

    def rotate(self, *, _rotozoom=pygame.transform.rotozoom) -> pygame.Surface:
        return _rotozoom(self.texture, self.rotation, self.xScale)
