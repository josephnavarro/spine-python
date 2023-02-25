#! usr/bin/env python3
from .AtlasRegion import AtlasRegion, BaseAtlasRegion
from .Atlas import Atlas
from .AtlasPage import AtlasPage
from .Format import Format
from .TextureFilter import TextureFilter
from .TextureWrap import TextureWrap

formatNames: tuple[str, ...] = (
    'Alpha',
    'Intensity',
    'LuminanceAlpha',
    'RGB565',
    'RGBA4444',
    'RGB888',
    'RGBA8888',
)

textureFiltureNames: tuple[str, ...] = (
    'Nearest',
    'Linear',
    'MipMap',
    'MipMapNearestNearest',
    'MipMapLinearNearest',
    'MipMapNearestLinear',
    'MipMapLinearLinear',
)
