#! usr/bin/env python3
import math

import Attachment


class RegionAttachment(Attachment.Attachment):
    __slots__ = [
        "x",
        "y",
        "scaleX",
        "scaleY",
        "rotation",
        "width",
        "height",
        "offset",
    ]

    def __init__(self):
        super(RegionAttachment, self).__init__()

        self.x: float = 0.0
        self.y: float = 0.0
        self.scaleX: float = 1.0
        self.scaleY: float = 1.0
        self.rotation: float = 0.0
        self.width: float = 0.0
        self.height: float = 0.0
        self.offset: list[float] = [
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
        ]

    def updateOffset(self) -> None:
        localX2: float = self.width * 0.5
        localY2: float = self.height * 0.5
        localX = -localX2
        localY = -localY2
        localX *= self.scaleX
        localY *= self.scaleY

        radians: float = math.radians(self.rotation)
        cos: float = math.cos(radians)
        sin: float = math.sin(radians)

        localXCos: float = (localX * cos) + self.x
        localXSin: float = localX * sin
        localYCos: float = (localY * cos) + self.y
        localYSin: float = localY * sin
        localX2Cos: float = (localX2 * cos) + self.x
        localX2Sin: float = localX2 * sin
        localY2Cos: float = (localY2 * cos) + self.y
        localY2Sin: float = localY2 * sin

        self.offset[0] = localXCos - localYSin
        self.offset[1] = localYCos + localXSin
        self.offset[2] = localXCos - localY2Sin
        self.offset[3] = localY2Cos + localXSin
        self.offset[4] = localX2Cos - localY2Sin
        self.offset[5] = localY2Cos + localX2Sin
        self.offset[6] = localX2Cos - localYSin
        self.offset[7] = localYCos + localX2Sin

    def updateWorldVerticies(self, bone):
        pass
