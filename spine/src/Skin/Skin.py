#! usr/bin/env python3
from .Key import Key
from .. import Attachment, Slot


class Skin:
    __slots__ = [
        "name",
        "attachments",
    ]

    def __init__(self, name: str):
        if not name:
            raise Exception('Name cannot be None.')
        self.name: str = name
        self.attachments: dict = {}

    def addAttachment(self, slotIndex: int, name: str, attachment: Attachment) -> None:
        if not name:
            raise Exception('Name cannot be None.')
        key = Key(slotIndex=slotIndex, name=name)
        self.attachments[key] = attachment

    def getAttachment(self, slotIndex: int, name: str) -> (Attachment | None):
        key = Key(slotIndex=slotIndex, name=name)
        if key in self.attachments:
            return self.attachments[key]
        return None

    def attachAll(self, skeleton, oldSkin):
        for key, attachment in self.attachments.items():
            slot: Slot = skeleton.slots[key.slotIndex]
            if slot.attachment == attachment:
                newAttachment: (Attachment | None) = self.getAttachment(key.slotIndex, key.name)
                if newAttachment is not None:
                    slot.setAttachment(newAttachment)
