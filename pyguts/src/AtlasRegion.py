#! usr/bin/env python3
import spine
from .AtlasPage import AtlasPage


class AtlasRegion(spine.AtlasRegion):
    __slots__ = [
        "page",
    ]

    def __init__(self):
        super(AtlasRegion, self).__init__()
        self.page: (AtlasPage | None) = None
