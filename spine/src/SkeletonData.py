#! usr/bin/env python3
from .Animation import Animation
from .BoneData import BoneData
from .SlotData import SlotData
from .Skin import Skin


class SkeletonData:
    __slots__ = [
        "bones",
        "slots",
        "skins",
        "animations",
        "defaultSkin",
    ]

    def __init__(self):
        self.bones: list[BoneData] = []
        self.slots: list[SlotData] = []
        self.skins: list[Skin] = []
        self.animations: list[Animation] = []
        self.defaultSkin = None

    def findBone(self, boneName: str) -> (BoneData | None):
        try:
            return tuple(filter(lambda bone: bone.name == boneName, self.bones))[0]
        except IndexError:
            return None

    def findBoneIndex(self, boneName: str) -> int:
        for i, bone in enumerate(self.bones):
            if bone.name == boneName:
                return i
        return -1

    def findSlot(self, slotName: str) -> (SlotData | None):
        try:
            return tuple(filter(lambda slot: slot.name == slotName, self.slots))[0]
        except IndexError:
            return None

    def findSlotIndex(self, slotName: str) -> int:
        for i, slot in enumerate(self.slots):
            if slot.name == slotName:
                return i
        return -1

    def findSkin(self, skinName: str) -> (Skin | None):
        try:
            return tuple(filter(lambda skin: skin.name == skinName, self.skins))[0]
        except IndexError:
            return None

    def findAnimation(self, animationName: str) -> (Animation | None):
        try:
            return tuple(filter(lambda animation: animation.name == animationName, self.animations))[0]
        except IndexError:
            return None
