#! usr/bin/env python3
from ..Enum import enum

TextureFilter = enum(
    nearest=0,
    linear=1,
    mipMap=2,
    mipMapNearestNearest=3,
    mipMapLinearNearest=4,
    mipMapNearestLinear=5,
    mipMapLinearLinear=6,
)