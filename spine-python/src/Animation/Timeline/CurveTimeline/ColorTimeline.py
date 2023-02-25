#! usr/bin/env python3
from .CurveTimeline import CurveTimeline
from .. import binarySearch


class ColorTimeline(CurveTimeline):
    __slots__ = [
        "LAST_FRAME_TIME",
        "FRAME_R",
        "FRAME_G",
        "FRAME_B",
        "FRAME_A",
        "frames",
        "slotIndex",
    ]

    def __init__(self, keyframeCount: int):
        super(ColorTimeline, self).__init__(keyframeCount)
        self.LAST_FRAME_TIME = -5
        self.FRAME_SPACING = -self.LAST_FRAME_TIME
        self.FRAME_R = 1
        self.FRAME_G = 2
        self.FRAME_B = 3
        self.FRAME_A = 4
        self.frames: list[float] = [0] * (keyframeCount * self.FRAME_SPACING)
        self.slotIndex = 0

    def getDuration(self) -> float:
        return self.frames[self.LAST_FRAME_TIME]

    def getKeyframeCount(self) -> int:
        return len(self.frames) // self.FRAME_SPACING

    def setKeyframe(self, keyframeIndex, time, r, g, b, a):
        keyframeIndex *= self.FRAME_SPACING
        self.frames[keyframeIndex] = time
        self.frames[keyframeIndex + 1] = r
        self.frames[keyframeIndex + 2] = g
        self.frames[keyframeIndex + 3] = b
        self.frames[keyframeIndex + 4] = a

    def apply(self, skeleton, time, alpha):
        if time < self.frames[0]:  # Time is before first frame.
            return

        slot = skeleton.slots[self.slotIndex]

        if time >= self.frames[self.LAST_FRAME_TIME]:  # -5
            i = len(self.frames) - 1
            slot.r = self.frames[i - 3]  # -4
            slot.g = self.frames[i - 2]  # -3
            slot.b = self.frames[i - 1]  # -2
            slot.a = self.frames[i]  # -1
            return

            # Interpolate between the last frame and the current frame.
        frameIndex = binarySearch(self.frames, time, self.FRAME_SPACING)
        lastFrameR = self.frames[frameIndex - 4]
        lastFrameG = self.frames[frameIndex - 3]
        lastFrameB = self.frames[frameIndex - 2]
        lastFrameA = self.frames[frameIndex - 1]
        frameTime = self.frames[frameIndex]
        percent = 1 - (time - frameTime) / (self.frames[frameIndex + self.LAST_FRAME_TIME] - frameTime)
        if percent < 0.0:
            percent = 0.0
        if percent > 255:
            percent = 255
        percent = self.getCurvePercent(frameIndex / self.FRAME_SPACING - 1, percent)

        r = lastFrameR + (self.frames[frameIndex + self.FRAME_R] - lastFrameR) * percent
        g = lastFrameG + (self.frames[frameIndex + self.FRAME_G] - lastFrameG) * percent
        b = lastFrameB + (self.frames[frameIndex + self.FRAME_B] - lastFrameB) * percent
        a = lastFrameA + (self.frames[frameIndex + self.FRAME_A] - lastFrameA) * percent
        if alpha < 1:
            slot.r += (r - slot.r) * alpha
            slot.g += (g - slot.g) * alpha
            slot.b += (b - slot.b) * alpha
            slot.a += (a - slot.a) * alpha
        else:
            slot.r = r
            slot.g = g
            slot.b = b
            slot.a = a
        return
