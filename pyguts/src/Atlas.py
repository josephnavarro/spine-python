#! usr/bin/env python3
import os
import pygame
import spine
from .AtlasPage import AtlasPage
from .AtlasRegion import AtlasRegion


class Atlas(spine.Atlas):
    __slots__ = []

    def __init__(self, file):
        super(Atlas, self).__init__()
        super(Atlas, self).loadWithFile(file)

    def newAtlasPage(self, name: str) -> AtlasPage:
        page = AtlasPage()
        page.texture = pygame.image.load(os.path.realpath(name)).convert_alpha()
        return page

    def newAtlasRegion(self, page: AtlasPage) -> AtlasRegion:
        region = AtlasRegion()
        region.page = page
        return region

    def findRegion(self, name: str) -> AtlasRegion:
        return super(Atlas, self).findRegion(name)
