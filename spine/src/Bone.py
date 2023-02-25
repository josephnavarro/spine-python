#! usr/bin/env python3
import math
from .BoneData import BoneData


class Bone:
    __slots__ = [
        "data",
        "parent",
        "x",
        "y",
        "rotation",
        "scaleX",
        "scaleY",
        "m00",
        "m01",
        "m10",
        "m11",
        "worldX",
        "worldY",
        "worldRotation",
        "worldScaleX",
        "worldScaleY",
        "line",
        "circle",
    ]
    def __init__(self, data: BoneData):
        self.data: BoneData = data
        self.parent = None
        self.x: float = data.x
        self.y: float = data.y
        self.rotation: float = data.rotation
        self.scaleX: float = data.scaleX
        self.scaleY: float = data.scaleY
        self.m00: float = 0.0
        self.m01: float = 0.0
        self.m10: float = 0.0
        self.m11: float = 0.0
        self.worldX: float = 0.0
        self.worldY: float = 0.0
        self.worldRotation : float= 0.0
        self.worldScaleX: float = 0.0
        self.worldScaleY: float = 0.0
        self.line = None
        self.circle = None

    def setToBindPose(self) -> None:
        self.x = self.data.x
        self.y = self.data.y
        self.rotation = self.data.rotation
        self.scaleX = self.data.scaleX
        self.scaleY = self.data.scaleY

    def updateWorldTransform(self, flipX: bool, flipY: bool, *, _rad=math.radians, _cos=math.cos, _sin=math.sin) -> None:
        if self.parent is not None:
            self.worldX = (self.x * self.parent.m00) + (self.y * self.parent.m01) + self.parent.worldX
            self.worldY = (self.x * self.parent.m10) + (self.y * self.parent.m11) + self.parent.worldY
            self.worldScaleX = self.parent.worldScaleX * self.scaleX
            self.worldScaleY = self.parent.worldScaleY * self.scaleY
            self.worldRotation = self.parent.worldRotation + self.rotation
        else:
            self.worldX = self.x
            self.worldY = self.y
            self.worldScaleX = self.scaleX
            self.worldScaleY = self.scaleY
            self.worldRotation = self.rotation

        radians: float = _rad(self.worldRotation)
        cos: float = _cos(radians)
        sin: float = _sin(radians)
        self.m00 = cos * self.worldScaleX
        self.m10 = sin * self.worldScaleX
        self.m01 = -sin * self.worldScaleY
        self.m11 = cos * self.worldScaleY

        if flipX:
            self.m00 = -self.m00
            self.m01 = -self.m01
        if flipY:
            self.m10 = -self.m10
            self.m11 = -self.m11
            # The C++ runtime has this, but Corona doesn't.
        # if self.data.flipY:
        #    self.m10 = -self.m10 if self.m10 != 0.0 else 0.0
        #    self.m11 = -self.m11 if self.m11 != 0.0 else 0.0
