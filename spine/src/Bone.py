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

        # TODO (?)
        # "shearX",
        # "shearY",
        # "flipX",
        # "flipY",

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
        self.parent: (Bone | None) = None
        self.x: float = data.x
        self.y: float = data.y
        self.rotation: float = data.rotation
        self.scaleX: float = data.scaleX
        self.scaleY: float = data.scaleY

        # 2x2 column-major matrix to encode rotation, scale, and shear
        self.m00: float = 0.0
        self.m01: float = 0.0
        self.m10: float = 0.0
        self.m11: float = 0.0

        # World position of this bone
        self.worldX: float = 0.0
        self.worldY: float = 0.0

        # TODO: Reconcile with matrix spec
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

    def updateWorldTransform(self, flipX: bool, flipY: bool,
                             *, _rad=math.radians, _cos=math.cos, _sin=math.sin) -> None:
        """
        Called by a skeleton when calculating its world transform.

        :param flipX:
        :param flipY:

        :param _rad:
        :param _cos:
        :param _sin:

        :return:
        """
        if self.parent is not None:
            # Offset relative to parent's specs
            parentWorldX: float = self.parent.worldX
            parentWorldScaleX: float = self.parent.worldScaleX
            parentWorldScaleY: float = self.parent.worldScaleY
            parentWorldRotation: float = self.parent.worldRotation
            parentWorldY: float = self.parent.worldY
            parentM00: float = self.parent.m00
            parentM01: float = self.parent.m01
            parentM10: float = self.parent.m10
            parentM11: float = self.parent.m11

            self.worldX = (self.x * parentM00) + (self.y * parentM01) + parentWorldX
            self.worldY = (self.x * parentM10) + (self.y * parentM11) + parentWorldY
            self.worldScaleX = parentWorldScaleX * self.scaleX
            self.worldScaleY = parentWorldScaleY * self.scaleY
            self.worldRotation = parentWorldRotation + self.rotation

        else:
            # Use own specs as source of truth
            self.worldX = self.x
            self.worldY = self.y
            self.worldScaleX = self.scaleX
            self.worldScaleY = self.scaleY
            self.worldRotation = self.rotation

        # Update 2x2 matrix
        # TODO: Encode shear
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
