#! usr/bin/env python3
from ..Enum import enum


TextureWrap = enum(
    mirroredRepeat=0,
    clampToEdge=1,
    repeat=2,
)
