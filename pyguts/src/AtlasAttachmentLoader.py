#! usr/bin/env python3
import spine
from .RegionAttachment import RegionAttachment


class AtlasAttachmentLoader(spine.AttachmentLoader):
    __slots__ = [
        "atlas"
    ]
    def __init__(self, atlas):
        self.atlas = atlas

    def newAttachment(self, type_, name: str) -> RegionAttachment:
        if type_ == spine.AttachmentType.region:
            region = self.atlas.findRegion(name)
            if region is None:
                raise Exception(f"Atlas region not found: {name}")
            return RegionAttachment(region)
        else:
            raise Exception(f"Unknown attachment type: {type_}")
