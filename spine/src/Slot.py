#! usr/bin/env python3
from .Attachment import Attachment
from .Skeleton import Skeleton
from .SlotData import SlotData


class Slot:
    __slots__ = [
        "data",
        "skeleton",
        "bone",
        "r",
        "g",
        "b",
        "a",
        "attachment",
        "attachmentTime",
    ]
    def __init__(self, slotData: SlotData, skeleton: Skeleton, bone):
        if not slotData:
            raise Exception('slotData cannot be None.')
        if not skeleton:
            raise Exception('skeleton cannot be None.')
        if not bone:
            raise Exception('bone cannot be None.')

        self.data: SlotData = slotData
        self.skeleton: Skeleton = skeleton
        self.bone = bone
        self.r: int = 255
        self.g: int = 255
        self.b: int = 255
        self.a: int = 255
        self.attachment: (Attachment | None) = None
        self.attachmentTime: float = 0.0

        self.setToBindPose()

    def setColor(self, r: int, g: int, b: int, a: int) -> None:
        self.r = r
        self.g = g
        self.b = b
        self.a = a

    def setAttachment(self, attachment: Attachment) -> None:
        self.attachment = attachment
        self.attachmentTime = self.skeleton.time

    def setAttachmentTime(self, time: float) -> None:
        self.attachmentTime = self.skeleton.time - time

    def getAttachmentTime(self) -> float:
        return self.skeleton.time - self.attachmentTime

    def setToBindPose(self) -> None:
        for i, slot in enumerate(self.skeleton.data.slots):
            if self.data == slot:
                self.setToBindPoseWithIndex(i)

    def setToBindPoseWithIndex(self, slotIndex: int) -> None:
        self.setColor(self.data.r, self.data.g, self.data.b, self.data.a)
        self.setAttachment(
            self.skeleton.getAttachmentByIndex(
                slotIndex,
                self.data.attachmentName
            )
            if self.data.attachmentName
            else None
        )
