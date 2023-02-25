#! usr/bin/env python3
from ..Timeline import Timeline, binarySearch


class CurveTimeline(Timeline):
    __slots__ = [
        "FRAME_SPACING",
        "LINEAR",
        "STEPPED",
        "BEZIER_SEGMENTS",
        "curves",
    ]

    def __init__(self, keyframeCount: int):
        super(CurveTimeline, self).__init__()
        self.FRAME_SPACING: int = 6
        self.LINEAR: int = 0
        self.STEPPED: int = -1
        self.BEZIER_SEGMENTS: float = 10.0
        self.curves: list[float] = [0] * ((keyframeCount - 1) * 6)

    def setLinear(self, keyframeIndex: int) -> None:
        self.curves[keyframeIndex * self.FRAME_SPACING] = self.LINEAR
        self.curves[keyframeIndex * 6] = self.LINEAR

    def setStepped(self, keyframeIndex: int) -> None:
        self.curves[keyframeIndex * self.FRAME_SPACING] = self.STEPPED
        self.curves[keyframeIndex * 6] = self.STEPPED

    def setCurve(self, keyframeIndex: int, cx1, cy1, cx2, cy2) -> None:
        subdiv_step1: float = 1.0 / self.BEZIER_SEGMENTS
        subdiv_step2: float = subdiv_step1 * subdiv_step1
        subdiv_step3: float = subdiv_step2 * subdiv_step1
        pre1: float = 3 * subdiv_step1
        pre2: float = 3 * subdiv_step2
        pre4: float = 6 * subdiv_step2
        pre5: float = 6 * subdiv_step3
        tmp1x = -cx1 * 2 + cx2
        tmp1y = -cy1 * 2 + cy2
        tmp2x = (cx1 - cx2) * 3 + 1
        tmp2y = (cy1 - cy2) * 3 + 1
        i: int = keyframeIndex * 6
        self.curves[i + 0] = (cx1 * pre1) + (tmp1x * pre2) + (tmp2x * subdiv_step3)
        self.curves[i + 1] = (cy1 * pre1) + (tmp1y * pre2) + (tmp2y * subdiv_step3)
        self.curves[i + 2] = (tmp1x * pre4) + (tmp2x * pre5)
        self.curves[i + 3] = (tmp1y * pre4) + (tmp2y * pre5)
        self.curves[i + 4] = (tmp2x * pre5)
        self.curves[i + 5] = (tmp2y * pre5)

    def getCurvePercent(self, keyframeIndex: int, percent) -> float:
        curveIndex: int = keyframeIndex * self.FRAME_SPACING
        # TODO: Inheritors overriding this to anything other than 6 cause it to break!
        curveIndex: int = keyframeIndex * 6

        dfx: float = self.curves[curveIndex]
        if dfx == self.LINEAR:
            return percent
        elif dfx == self.STEPPED:
            return 0.0
        else:
            dfy: float = self.curves[curveIndex + 1]
            ddfx: float = self.curves[curveIndex + 2]
            ddfy: float = self.curves[curveIndex + 3]
            dddfx: float = self.curves[curveIndex + 4]
            dddfy: float = self.curves[curveIndex + 5]
            x: float = dfx
            y: float = dfy
            i: float = self.BEZIER_SEGMENTS - 2

            while i != 0:
                if x >= percent:
                    lastX: float = x - dfx
                    lastY: float = y - dfy
                    return lastY + (y - lastY) * (percent - lastX) / (x - lastX)
                else:
                    i -= 1
                    dfx += ddfx
                    dfy += ddfy
                    ddfx += dddfx
                    ddfy += dddfy
                    x += dfx
                    y += dfy

            return y + (1 - y) * (percent - x) / (1 - x)  # Last point is 1,1
