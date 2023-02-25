#! usr/bin/env python3
from .Utility import *


class Animation:
    __slots__ = [
        "name",
        "timelines",
        "duration",
    ]

    def __init__(self, name, timelines, duration):
        if not timelines:
            raise Exception('Timelines cannot be None.')
        self.name = name
        self.timelines = timelines
        self.duration = duration

    def mix(self, skeleton, time, loop, alpha):
        if not skeleton:
            raise Exception('Skeleton cannot be None.')

        if loop and self.duration:
            time = time % self.duration
        # if loop and self.duration:
        #     time = time % self.duration

        for timeline in self.timelines:
            timeline.apply(skeleton, time, alpha)

    def apply(self, skeleton, time, loop):
        if not skeleton:
            raise Exception('Skeleton cannot be None.')

        if loop and self.duration:
            time = time % self.duration

        for timeline in self.timelines:
            timeline.apply(skeleton, time, 1)
