#! usr/bin/env python3
from .. import CurveTimeline, binarySearch


class RotateTimeline(CurveTimeline):
    __slots__ = [
        "LAST_FRAME_TIME",
        "FRAME_VALUE",
        "frames",
        "boneIndex",
    ]

    def __init__(self, keyframeCount):
        super(RotateTimeline, self).__init__(keyframeCount)
        self.LAST_FRAME_TIME: int = -2
        self.FRAME_SPACING: int = -self.LAST_FRAME_TIME
        self.FRAME_VALUE: int = 1
        self.frames: list[float] = [0.0] * (keyframeCount * self.FRAME_SPACING)
        self.boneIndex: int = 0

    def getDuration(self) -> float:
        return self.frames[self.LAST_FRAME_TIME]

    def getKeyframeCount(self) -> int:
        return len(self.frames) // self.FRAME_SPACING

    def setKeyframe(self, keyframeIndex: int, time, value) -> None:
        keyframeIndex *= self.FRAME_SPACING
        self.frames[keyframeIndex] = time
        self.frames[keyframeIndex + 1] = value

    def apply(self, skeleton, time, alpha) -> bool:
        if time < self.frames[0]:
            return False
        else:
            bone = skeleton.bones[self.boneIndex]
            if time >= self.frames[self.LAST_FRAME_TIME]:
                # Time is after last frame
                amount = bone.data.rotation + self.frames[-1] - bone.rotation
                while amount > 180:
                    amount -= 360
                while amount < -180:
                    amount += 360
                bone.rotation = bone.rotation + amount * alpha
                return True
            else:
                # Interpolate between the last frame and the current frame
                frameIndex: int = binarySearch(self.frames, time, self.FRAME_SPACING)
                lastFrameValue: float = self.frames[frameIndex - 1]
                frameTime: float = self.frames[frameIndex]

                percent: float = 1.0 - (time - frameTime) / (self.frames[frameIndex + self.LAST_FRAME_TIME] - frameTime)
                if percent < 0.0:
                    percent = 0.0
                elif percent > 1.0:
                    percent = 1.0
                percent = self.getCurvePercent(frameIndex // self.FRAME_SPACING - 1, percent)

                amount: float = self.frames[frameIndex + self.FRAME_VALUE] - lastFrameValue
                while amount > 180:
                    amount -= 360
                while amount < -180:
                    amount += 360

                amount: float = bone.data.rotation + (lastFrameValue + amount * percent) - bone.rotation
                while amount > 180:
                    amount -= 360
                while amount < -180:
                    amount += 360

                bone.rotation = bone.rotation + amount * alpha
                return True
