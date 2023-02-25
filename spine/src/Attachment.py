#! usr/bin/env python3

class Attachment:
    __slots__ = [
        "name",
        # TODO: Subclass? The following are only for 'regionAttachment'
        "x",
        "y",
        "scaleX",
        "scaleY",
        "rotation",
        "width",
        "height"
    ]

    def __init__(self):
        self.name: (str | None) = None

    def draw(self, slot):
        pass
