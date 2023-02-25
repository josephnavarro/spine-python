#! usr/bin/env python3
from ..Enum import enum

Format = enum(
    alpha=0,
    intensity=1,
    luminanceAlpha=2,
    rgb565=3,
    rgba4444=4,
    rgb888=5,
    rgba8888=6,
)
