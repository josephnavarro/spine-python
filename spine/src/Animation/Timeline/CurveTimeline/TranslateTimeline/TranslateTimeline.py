#! usr/bin/env python3
from ..CurveTimeline import CurveTimeline, binarySearch


class TranslateTimeline(CurveTimeline):
    __slots__ = [
        "LAST_FRAME_TIME",
        "FRAME_X",
        "FRAME_Y",
        "frames",
        "boneIndex",
    ]

    def __init__(self, keyframeCount: int):
        super(TranslateTimeline, self).__init__(keyframeCount)
        self.LAST_FRAME_TIME: int = -3
        self.FRAME_SPACING: int = -self.LAST_FRAME_TIME
        self.FRAME_X: int = 1
        self.FRAME_Y: int = 2
        self.frames: list[float] = [0.0] * (keyframeCount * self.FRAME_SPACING)
        self.boneIndex: int = 0

    def getDuration(self) -> float:
        return self.frames[self.LAST_FRAME_TIME]

    def getKeyframeCount(self) -> int:
        return len(self.frames) // self.FRAME_SPACING

    def setKeyframe(self, keyframeIndex: int, time, x, y) -> None:
        keyframeIndex = keyframeIndex * self.FRAME_SPACING
        self.frames[keyframeIndex] = time
        self.frames[keyframeIndex + 1] = x
        self.frames[keyframeIndex + 2] = y

    def apply(self, skeleton, time, alpha) -> bool:
        if time < self.frames[0]:
            # Time is before the first frame
            return False
        else:
            bone = skeleton.bones[self.boneIndex]

            if time >= self.frames[self.LAST_FRAME_TIME]:
                # Time is after the last frame.
                bone.x += (bone.data.x + self.frames[self.LAST_FRAME_TIME + 1] - bone.x) * alpha
                bone.y += (bone.data.y + self.frames[self.LAST_FRAME_TIME + 2] - bone.y) * alpha
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
                if percent > 1.0:
                    percent = 1.0
                percent: float = self.getCurvePercent(frameIndex // self.FRAME_SPACING - 1, percent)

                bone.x += (bone.data.x + lastFrameX + (self.frames[frameIndex + self.FRAME_X] - lastFrameX) * percent - bone.x) * alpha
                bone.y += (bone.data.y + lastFrameY + (self.frames[frameIndex + self.FRAME_Y] - lastFrameY) * percent - bone.y) * alpha
                return True
