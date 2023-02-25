#! usr/bin/env python3
from .Timeline import Timeline, binarySearch


class AttachmentTimeline(Timeline):
    __slots__ = [
        "LAST_FRAME_TIME",
        "FRAME_SPACING",
        "frames",
        "attachmentNames",
        "slotIndex",
    ]

    def __init__(self, keyframeCount: int):
        super(AttachmentTimeline, self).__init__(keyframeCount)
        self.LAST_FRAME_TIME = -1
        self.FRAME_SPACING = -self.LAST_FRAME_TIME
        self.frames: list[float] = [0.0] * keyframeCount
        self.attachmentNames = [None] * keyframeCount
        self.slotIndex = 0

    def getDuration(self) -> float:
        return self.frames[self.LAST_FRAME_TIME]

    def getKeyframeCount(self) -> int:
        return len(self.frames)

    def setKeyframe(self, keyframeIndex: int, time: float, attachmentName) -> None:
        self.frames[keyframeIndex] = time
        self.attachmentNames[keyframeIndex] = attachmentName

    def apply(self, skeleton, time, alpha) -> bool:
        if time < self.frames[0]:
            # Time is before first frame
            return False
        else:
            if time >= self.frames[self.LAST_FRAME_TIME]:
                # Time is after last frame.
                frameIndex: int = self.LAST_FRAME_TIME
            else:
                frameIndex: int = binarySearch(self.frames, time, self.FRAME_SPACING) - 1

            attachmentName = self.attachmentNames[frameIndex]
            skeleton.slots[self.slotIndex].setAttachment(
                skeleton.getAttachmentByIndex(self.slotIndex, attachmentName)
            )
            return True
