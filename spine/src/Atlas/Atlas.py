#! usr/bin/env python3
import os
from .AtlasPage import AtlasPage
from .AtlasRegion import AtlasRegion
from .TextureWrap import TextureWrap


class Atlas:
    __slots__ = [
        "pages",
        "regions",
    ]

    def __init__(self):
        self.pages: list[AtlasPage] = []
        self.regions: list[AtlasRegion] = []

    def loadWithFile(self, file: (str | None)):
        if not file:
            raise Exception('input cannot be null.')

        with open(os.path.realpath(file), 'r') as fh:
            text: list[str] = fh.readlines()
        self.load(text)

    def load(self, text: list[str]):
        page = None
        # region = None
        _page: (dict | None) = None
        _region: dict = {}

        for line in text:
            value: str = line.strip().rstrip()
            if _page is None:
                _page = {}
            if not value:
                _page: dict = {}
                page = None

            if not page:
                if not ':' in value:
                    value: str = value.strip().rstrip()
                    _page['name'] = value
                else:
                    key, value = value.split(':')
                    key: str = key.strip().rstrip()
                    value: str = value.strip().rstrip()
                    if ',' in value:
                        value: list[str] = value.split(',')
                        _page[key] = [x.strip().rstrip() for x in value]
                    else:
                        if value == 'false':
                            value: bool = False
                        elif value == 'true':
                            value: bool = True
                        _page[key] = value
                    if key == 'repeat':
                        page = self.newAtlasPage(_page['name'])
                        page.format = _page['format']
                        page.minFilter = _page['filter'][0]
                        page.magFilter = _page['filter'][1]
                        if _page['repeat'] == 'x':
                            page.uWrap = TextureWrap.repeat
                            page.vWrap = TextureWrap.clampToEdge
                        elif _page['repeat'] == 'y':
                            page.uWrap = TextureWrap.clampToEdge
                            page.vWrap = TextureWrap.repeat
                        elif _page['repeat'] == 'xy':
                            page.uWrap = TextureWrap.repeat
                            page.vWrap = TextureWrap.repeat
                        self.pages.append(page)
            else:
                if not ':' in value:
                    value: str = value.strip().rstrip()
                    _region['name'] = value
                else:
                    key, value = value.split(':')
                    key: str = key.strip().rstrip()
                    value: str = value.strip().rstrip()
                    if ',' in value:
                        value: list = value.split(',')
                        _region[key] = [int(x.strip().rstrip()) for x in value]
                    else:
                        if value == 'false':
                            value: bool = False
                        elif value == 'true':
                            value: bool = True
                        _region[key] = value

                    if key == 'index':
                        region = self.newAtlasRegion(page)
                        region.name = _region['name']
                        region.x = _region['xy'][0]
                        region.y = _region['xy'][1]
                        region.width = _region['size'][0]
                        region.height = _region['size'][1]
                        if 'split' in _region:
                            region.splits.append(_region['split'][0])
                            region.splits.append(_region['split'][1])
                            region.splits.append(_region['split'][2])
                            region.splits.append(_region['split'][3])
                            if 'pad' in _region:
                                region.pads.append(_region['pad'][0])
                                region.pads.append(_region['pad'][1])
                                region.pads.append(_region['pad'][2])
                                region.pads.append(_region['pad'][3])
                        region.originalWidth = _region['orig'][0]
                        region.originalHeight = _region['orig'][1]
                        region.offsetX = _region['offset'][0]
                        region.offsetY = _region['offset'][1]
                        region.index = int(_region['index'])
                        self.regions.append(region)
                        _region = {}
                        continue

    def findRegion(self, name: str):
        for region in self.regions:
            if region.name == name:
                return region
        return None

    def newAtlasPage(self, name: str) -> AtlasPage:
        pass

    def newAtlasRegion(self, page) -> AtlasRegion:
        pass
