#! usr/bin/env python3
import json
import os
from .Animation import Animation
from .SkeletonData import SkeletonData
from .BoneData import BoneData
from .SlotData import SlotData
from .Skin import Skin
from .Attachment import Attachment
from .AttachmentLoader import AttachmentType, AttachmentLoader
from .Animation.Timeline import Timeline, AttachmentTimeline, CurveTimeline, ScaleTimeline, TranslateTimeline, ColorTimeline, RotateTimeline


def readCurve(timeline: CurveTimeline, keyframeIndex: int, valueMap: dict) -> Timeline:
    try:
        curve = valueMap['curve']
    except KeyError:
        return timeline

    if curve == 'stepped':
        timeline.setStepped(keyframeIndex)
    else:
        timeline.setCurve(
            keyframeIndex,
            float(curve[0]),
            float(curve[1]),
            float(curve[2]),
            float(curve[3]),
        )
    return timeline


class SkeletonJson:
    __slots__ = [
        "attachmentLoader",
        "scale",
        "flipY",
    ]

    def __init__(self, attachmentLoader: AttachmentLoader):
        self.attachmentLoader: AttachmentLoader = attachmentLoader
        self.scale: float = 1.0
        self.flipY: bool = False

    def readSkeletonDataFile(self, filename: str, path: (str | None) = None):
        if path:
            filename: str = '{path}/{file}'.format(path=path, file=filename)

        filename = os.path.realpath(filename)
        with open(filename, 'r') as jsonFile:
            jsonPayload: str = ''.join(jsonFile.readlines())

        return self.readSkeletonData(jsonPayload=jsonPayload)

    def createNewBoneData(self, boneMap: dict, skeletonData: SkeletonData) -> BoneData:
        boneName: str = boneMap["name"]

        boneData: BoneData = BoneData(name=boneName)

        # "parent" (optional)
        try:
            boneParent: str = boneMap["parent"]
            boneData.parent = skeletonData.findBone(boneParent)
            if boneData.parent is None:
                raise Exception(f"Parent bone not found: {boneName}")
        except KeyError:
            pass

        # "length"
        try:
            boneLength: float = float(boneMap["length"]) * self.scale
        except KeyError:
            boneLength = 0.0
        boneData.length = boneLength

        # "x"
        try:
            boneX: float = float(boneMap["x"]) * self.scale
        except KeyError:
            boneX = 0.0
        boneData.x = boneX

        # "y"
        try:
            boneY: float = float(boneMap["y"]) * self.scale
        except KeyError:
            boneY = 0.0
        boneData.y = boneY

        # "rotation"
        try:
            boneRotation: float = float(boneMap["rotation"])
        except KeyError:
            boneRotation = 0.0
        boneData.rotation = boneRotation

        # "scaleX"
        try:
            boneScaleX: float = float(boneMap["scaleX"])
        except KeyError:
            boneScaleX = 1.0
        boneData.scaleX = boneScaleX

        # "scaleY"
        try:
            boneScaleY: float = float(boneMap["scaleY"])
        except KeyError:
            boneScaleY = 1.0
        boneData.scaleY = boneScaleY

        return boneData

    @staticmethod
    def createSlotData(slotMap: dict, skeletonData: SkeletonData) -> SlotData:
        slotName: str = slotMap["name"]

        # "bone"
        boneName: str = slotMap["bone"]
        boneData: (BoneData | None) = skeletonData.findBone(boneName)
        if BoneData is None:
            raise Exception(f"Slot bone not found: {boneName}")

        slotData: SlotData = SlotData(name=slotName, boneData=boneData)

        # "color"
        try:
            slotColor = slotMap["color"]
            slotData.r = int(slotColor[0:2], 16)
            slotData.g = int(slotColor[2:4], 16)
            slotData.b = int(slotColor[4:6], 16)
            slotData.a = int(slotColor[6:8], 16)
        except KeyError:
            pass

        # "attachment"
        try:
            slotData.attachmentName = slotMap['attachment']
        except KeyError:
            pass

        return slotData

    def readSkeletonData(self, jsonPayload: str):
        try:
            root: dict = json.loads(jsonPayload)
        except ValueError:
            if os.path.isfile(jsonPayload):
                print('The API has changed.  You need to load skeleton data with readSkeletonDataFile(), not readSkeletonData()')
            raise SystemExit

        skeletonData: SkeletonData = SkeletonData()

        # "bones"
        try:
            skeletonData.bones.extend([self.createNewBoneData(boneMap, skeletonData) for boneMap in root["bones"]])
        except KeyError:
            pass

        # "slots"
        try:
            skeletonData.slots.extend([self.createSlotData(slotMap, skeletonData) for slotMap in root["slots"]])
        except KeyError:
            pass

        # skinsMap: dict = root.get('skins', {})

        skinsList: list[dict] = root.get("skins", [])
        for skinData in skinsList:
            skinName: str = skinData["name"]
            skin: Skin = Skin(skinName)

            skeletonData.skins.append(skin)
            if skinName == 'default':
                skeletonData.defaultSkin = skin

            attachmentsMap: dict = skinData["attachments"]
            for attachmentName in attachmentsMap.keys():
                attachmentMap: dict = attachmentsMap[attachmentName]
                attachmentData: dict = attachmentMap[attachmentName]

                try:
                    typeString: str = attachmentData["type"]
                except KeyError:
                    typeString = "region"

                if typeString == 'region':
                    type_ = AttachmentType.region
                elif typeString == 'regionSequence':
                    type_ = AttachmentType.regionSequence
                else:
                    raise Exception(f"Unknown attachment type: {typeString} ({attachmentName})")
                attachment: Attachment = self.attachmentLoader.newAttachment(type_, attachmentName)
                # TODO: We're transcribing a list of skinMaps now

        skinsMap = {}
        print(skinsMap)
        for skinName in skinsMap.keys():
            skin: Skin = Skin(skinName)
            skeletonData.skins.append(skin)
            if skinName == 'default':
                skeletonData.defaultSkin = skin

            slotMap: dict = skinsMap[skinName]
            for slotName in slotMap.keys():
                slotIndex: int = skeletonData.findSlotIndex(slotName)
                attachmentsMap: dict = slotMap[slotName]
                for attachmentName in attachmentsMap.keys():
                    attachmentMap: dict = attachmentsMap[attachmentName]
                    typeString: str = attachmentMap.get('type', 'region')
                    if typeString == 'region':
                        type_ = AttachmentType.region
                    elif typeString == 'regionSequence':
                        type_ = AttachmentType.regionSequence
                    else:
                        raise Exception(f"Unknown attachment type: {typeString} ({attachmentName})")

                    attachment: Attachment = self.attachmentLoader.newAttachment(
                        type_,
                        attachmentMap.get('name', attachmentName)
                    )

                    if type_ == AttachmentType.region or type_ == AttachmentType.regionSequence:
                        regionAttachment: Attachment = attachment
                        regionAttachment.name = attachmentName

                        # "x"
                        try:
                            regionAttachmentX: float = float(attachmentMap["x"]) * self.scale
                        except KeyError:
                            regionAttachmentX = 0.0
                        regionAttachment.x = regionAttachmentX

                        # "y"
                        try:
                            regionAttachmentY: float = float(attachmentMap["y"]) * self.scale
                        except KeyError:
                            regionAttachmentY = 0.0
                        regionAttachment.y = regionAttachmentY

                        regionAttachment.scaleX = float(attachmentMap.get('scaleX', 1.0))
                        regionAttachment.scaleY = float(attachmentMap.get('scaleY', 1.0))
                        regionAttachment.rotation = float(attachmentMap.get('rotation', 0.0))
                        regionAttachment.width = float(attachmentMap.get('width', 32)) * self.scale
                        regionAttachment.height = float(attachmentMap.get('height', 32)) * self.scale

                    skin.addAttachment(slotIndex, attachmentName, attachment)

        animations: dict = root.get('animations', {})
        for animationName in animations:
            animationMap: dict = animations.get(animationName, {})
            animationData = self.readAnimation(
                name=animationName,
                root=animationMap,
                skeletonData=skeletonData,
            )
            skeletonData.animations.append(animationData)

        return skeletonData

    @staticmethod
    def readAnimation(name: str, root: dict, skeletonData: (SkeletonData | None)) -> Animation:
        if skeletonData is None:
            raise Exception('skeletonData cannot be null.')
        else:
            timelines: list[Timeline] = []
            duration: float = 0.0
            bones: dict = root.get('bones', {})

            for boneName in bones.keys():
                boneIndex: int = skeletonData.findBoneIndex(boneName)
                if boneIndex == -1:
                    raise Exception('Bone not found: %s' % boneName)
                else:
                    timelineMap: dict = bones[boneName]
                    for timelineName in timelineMap.keys():
                        values = timelineMap[timelineName]

                        if timelineName == 'rotate':
                            timeline: RotateTimeline = RotateTimeline(len(values))
                            timeline.boneIndex = boneIndex

                            keyframeIndex: int = 0
                            for valueMap in values:
                                time: float = valueMap['time']
                                timeline.setKeyframe(keyframeIndex, time, valueMap['angle'])
                                timeline: (RotateTimeline | Timeline) = readCurve(timeline, keyframeIndex, valueMap)
                                keyframeIndex += 1

                            timelines.append(timeline)
                            if timeline.getDuration() > duration:
                                duration = timeline.getDuration()

                        elif timelineName == 'translate' or timelineName == 'scale':
                            if timelineName == 'scale':
                                timeline: (ScaleTimeline | Timeline) = ScaleTimeline(len(values))
                            else:
                                timeline: (TranslateTimeline | Timeline) = TranslateTimeline(len(values))
                            timeline.boneIndex = boneIndex

                            keyframeIndex: int = 0
                            for valueMap in values:
                                timeline.setKeyframe(
                                    keyframeIndex,
                                    valueMap['time'],
                                    valueMap.get('x', 0.0),
                                    valueMap.get('y', 0.0),
                                )
                                timeline: Timeline = readCurve(timeline, keyframeIndex, valueMap)
                                keyframeIndex += 1

                            timelines.append(timeline)
                            if timeline.getDuration() > duration:
                                duration = timeline.getDuration()
                        else:
                            raise Exception(f"Invalid timeline type for a bone: {timelineName} ({boneName})")

            slots: dict = root.get('slots', {})
            for slotName in slots.keys():
                slotIndex: int = skeletonData.findSlotIndex(slotName)
                if slotIndex == -1:
                    raise Exception(f"Slot not found: {slotName}")
                else:
                    timelineMap: dict = slots[slotName]
                    for timelineName in timelineMap.keys():
                        values = timelineMap[timelineName]
                        if timelineName == 'color':
                            timeline: ColorTimeline = ColorTimeline(len(values))
                            timeline.slotIndex = slotIndex

                            keyframeIndex: int = 0
                            for valueMap in values:
                                timeline.setKeyframe(
                                    keyframeIndex,
                                    valueMap['time'],
                                    int(valueMap['color'][0:2], 16),
                                    int(valueMap['color'][2:4], 16),
                                    int(valueMap['color'][4:6], 16),
                                    int(valueMap['color'][6:8], 16),
                                )
                                timeline: (ColorTimeline | Timeline) = readCurve(timeline, keyframeIndex, valueMap)
                                keyframeIndex += 1

                            timelines.append(timeline)
                            timelineDuration: float = timeline.getDuration()
                            if timelineDuration > duration:
                                duration = timelineDuration

                        elif timelineName == 'attachment':
                            timeline: AttachmentTimeline = AttachmentTimeline(len(values))
                            timeline.slotIndex = slotIndex

                            keyframeIndex: int = 0
                            for valueMap in values:
                                valueName: str = valueMap['name']
                                timeline.setKeyframe(keyframeIndex, valueMap['time'], '' if not valueName else valueName)
                                keyframeIndex += 1

                            timelines.append(timeline)
                            timelineDuration: float = timeline.getDuration()
                            if timelineDuration > duration:
                                duration = timelineDuration
                        else:
                            raise Exception(f"Invalid timeline type for a slot: {timelineName} ({slotName})")

            animation: Animation = Animation(name, timelines, duration)
            return animation
