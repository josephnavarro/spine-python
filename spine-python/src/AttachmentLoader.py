#! usr/bin/env python3
import Enum

AttachmentType = Enum.enum(
    region=0,
    regionSequence=1,
)


class AttachmentLoader:
    __slots__ = []

    def newAttachment(self, type, name):
        pass
