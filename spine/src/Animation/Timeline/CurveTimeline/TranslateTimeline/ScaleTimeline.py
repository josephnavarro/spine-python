#! usr/bin/env python3
from .TranslateTimeline import TranslateTimeline, binarySearch


class ScaleTimeline(TranslateTimeline):
    __slots__ = [
        "LAST_FRAME_TIME",
        "FRAME_SPACING",
        "FRAME_X",
        "FRAME_Y",
    ]

    def __init__(self, keyframeCount: int):
        super(ScaleTimeline, self).__init__(keyframeCount)
        self.LAST_FRAME_TIME = -3
        self.FRAME_SPACING = -self.LAST_FRAME_TIME
        self.FRAME_X = 1
        self.FRAME_Y = 2

    def apply(self, skeleton, time, alpha) -> bool:
        if time < self.frames[0]:
            return False
        else:

            bone = skeleton.bones[self.boneIndex]
            if time >= self.frames[self.LAST_FRAME_TIME]:
                # Time is after last frame
                bone.scaleX += (bone.data.scaleX - 1 + self.frames[len(self.frames) - 2] - bone.scaleX) * alpha
                bone.scaleY += (bone.data.scaleY - 1 + self.frames[len(self.frames) - 1] - bone.scaleY) * alpha
                return True
            else:
                # Interpolate between the last frame and the current frame
                frameIndex: int = binarySearch(self.frames, time, self.FRAME_SPACING)
                lastFrameX: float = self.frames[frameIndex - 2]
                lastFrameY: float = self.frames[frameIndex - 1]
                frameTime: float = self.frames[frameIndex]

                percent: float = 1.0 - (time - frameTime) / (self.frames[frameIndex + self.LAST_FRAME_TIME] - frameTime)
                if percent < 0.0:
                    percent = 0.0
                elif percent > 1.0:
                    percent = 1.0
                percent: float = self.getCurvePercent(frameIndex // self.FRAME_SPACING - 1, percent)

                bone.scaleX += (bone.data.scaleX - 1 + lastFrameX + (self.frames[frameIndex + self.FRAME_X] - lastFrameX) * percent - bone.scaleX) * alpha
                bone.scaleY += (bone.data.scaleY - 1 + lastFrameY + (self.frames[frameIndex + self.FRAME_Y] - lastFrameY) * percent - bone.scaleY) * alpha
                return True
