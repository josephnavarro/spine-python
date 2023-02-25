#! usr/bin/env python3
from BoneData import BoneData


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
        self.slots = []
        self.skins = []
        self.animations = []
        self.defaultSkin = None

    def findBone(self, boneName) -> (BoneData | None):
        for i, bone in enumerate(self.bones):
            if bone.name == boneName:
                return bone
        return None

    def findBoneIndex(self, boneName) -> int:
        for i, bone in enumerate(self.bones):
            if bone.name == boneName:
                return i
        return -1

    def findSlot(self, slotName):
        for i, slot in enumerate(self.slots):
            if slot.name == slotName:
                return slot
        return None

    def findSlotIndex(self, slotName):
        for i, slot in enumerate(self.slots):
            if slot.name == slotName:
                return i
        return -1

    def findSkin(self, skinName):
        for i, skin in enumerate(self.skins):
            if skin.name == skinName:
                return skin
        return None

    def findAnimation(self, animationName):
        for i, animation in enumerate(self.animations):
            if animation.name == animationName:
                return animation
        return None
