#! usr/bin/env python3
from .Attachment import Attachment
from .Bone import Bone
from .Slot import Slot
from .SkeletonData import SkeletonData
from .Skin import Skin


class Skeleton:
    __slots__ = [
        "data",
        "skin",
        "r",
        "g",
        "b",
        "a",
        "time",
        "bones",
        "slots",
        "drawOrder",
        "flipX",
        "flipY",
    ]

    def __init__(self, skeletonData: (SkeletonData | None)):
        if skeletonData is None:
            raise Exception("skeletonData cannot be null")

        self.data: SkeletonData = skeletonData
        self.skin: (Skin | None) = None
        self.r: float = 1.0
        self.g: float = 1.0
        self.b: float = 1.0
        self.a: float = 1.0
        self.time: float = 0.0
        self.bones: list[Bone | None] = []
        self.slots: list = []
        self.drawOrder: list[Slot] = []
        self.flipX: bool = False
        self.flipY: bool = False

        boneCount: int = len(self.data.bones)
        self.bones: list[Bone | None] = [None] * boneCount
        for i in range(boneCount):
            boneData = self.data.bones[i]
            bone = Bone(boneData)
            if boneData.parent:
                for ii in range(boneCount):
                    if self.data.bones[ii] == boneData.parent:
                        bone.parent = self.bones[ii]
                        break
            self.bones[i] = bone

        slotCount = len(self.data.slots)
        self.slots: list = [None] * slotCount
        for i in range(slotCount):
            slotData = self.data.slots[i]
            bone = None
            for ii in range(boneCount):
                if self.data.bones[ii] == slotData.boneData:
                    bone = self.bones[ii]
                    break
            slot = Slot(slotData=slotData, skeleton=self, bone=bone)
            self.slots[i] = slot
            self.drawOrder.append(slot)

    def updateWorldTransform(self) -> None:
        """
        Once all of the local transforms are set up, we need the world transform
        of each bone (for rendering, physics, etc.)

        This calculation starts at the root bone, then recursively calculates all
        child bone world transforms.

        Calculated results are stored on each bone.

        :return:
        """
        for bone in self.bones:
            bone.updateWorldTransform(self.flipX, self.flipY)

    def setToBindPose(self) -> None:
        self.setBonesToBindPose()
        self.setSlotsToBindPose()

    def setBonesToBindPose(self) -> None:
        for bone in self.bones:  # type: Bone
            bone.setToBindPose()

    def setSlotsToBindPose(self) -> None:
        for i, bone in enumerate(self.slots):
            self.slots[i].setToBindPoseWithIndex(i)

    def getRootBone(self) -> (Bone | None):
        try:
            return self.bones[0]
        except IndexError:
            return None

    def setRootBone(self, bone: Bone) -> None:
        try:
            self.bones[0] = bone
        except IndexError:
            pass

    def findBone(self, boneName) -> (Bone | None):
        for i, bone in enumerate(self.bones):
            if self.data.bones[i].name == boneName:
                return self.bones[i]
        return None

    def findBoneIndex(self, boneName) -> int:
        for i, bone in enumerate(self.bones):
            if self.data.bones[i].name == boneName:
                return i
        return -1

    def findSlot(self, slotName) -> (Slot | None):
        for i, slot in enumerate(self.slots):
            if self.data.slots[i].name == slotName:
                return self.slots[i]
        return None

    def findSlotIndex(self, slotName) -> int:
        for i, slot in enumerate(self.slots):
            if self.data.slots[i].name == slotName:
                return i
        return -1

    def setSkin(self, skinName: str) -> None:
        skin = self.data.findSkin(skinName)
        if skin is None:
            raise Exception(f"Skin not found: {skinName}")
        self.setSkinToSkin(skin)

    def setSkinToSkin(self, newSkin) -> None:
        if self.skin and newSkin:
            newSkin.attachAll(self, self.skin)
        self.skin = newSkin

    def getAttachmentByName(self, slotName, attachmentName) -> (Attachment | None):
        return self.getAttachmentByIndex(
            self.data.findSlotIndex(slotName),
            attachmentName
        )

    def getAttachmentByIndex(self, slotIndex, attachmentName) -> (Attachment | None):
        if self.data.defaultSkin:
            attachment = self.data.defaultSkin.getAttachment(slotIndex, attachmentName)
            if attachment is not None:
                return attachment
        if self.skin is not None:
            return self.skin.getAttachment(slotIndex, attachmentName)
        return None

    def setAttachment(self, slotName: str, attachmentName: str) -> None:
        for i in range(len(self.slots)):
            _slot: Slot = self.slots[i]
            if _slot.data.name == slotName:
                _slot.setAttachment(self.getAttachmentByIndex(i, attachmentName))
                return
        raise Exception(f"Slot not found: {slotName}")

    def update(self, delta: float) -> None:
        self.time += delta
