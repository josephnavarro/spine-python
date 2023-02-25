#! usr/bin/env python3
import pygame
import spine


class AtlasPage(spine.AtlasPage):
    __slots__ = [
        "texture",
    ]

    def __init__(self):
        super(AtlasPage, self).__init__()
        self.texture: (pygame.Surface | None) = None
