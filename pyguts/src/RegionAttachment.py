#! usr/bin/env python3
import spine
import pygame
from .Vertex import Vertex


class RegionAttachment(spine.RegionAttachment):
    __slots__ = [
        "verticies",
        "u",
        "u2",
        "v",
        "v2",
        "rect",
        "texture",
    ]

    def __init__(self, region):
        super(RegionAttachment, self).__init__()
        self.verticies: list[Vertex, Vertex, Vertex, Vertex] = [
            Vertex(),
            Vertex(),
            Vertex(),
            Vertex(),
        ]
        self.u = region.x
        self.u2 = self.u + region.width
        self.v = region.y
        self.v2 = self.v + region.height
        self.rect = pygame.Rect((self.u, self.v, region.width, region.height))
        self.texture = region.page.texture.subsurface(self.rect)
        self.offset = pygame.Rect(0, 0, region.width, region.height)
        self.offset.center = (region.width / 2, region.height / 2)
        if region.rotate:
            self.verticies[1].texCoords.x = self.u
            self.verticies[1].texCoords.y = self.v2
            self.verticies[2].texCoords.x = self.u
            self.verticies[2].texCoords.y = self.v
            self.verticies[3].texCoords.x = self.u2
            self.verticies[3].texCoords.y = self.v
            self.verticies[0].texCoords.x = self.u2
            self.verticies[0].texCoords.y = self.v2
        else:
            self.verticies[0].texCoords.x = self.u
            self.verticies[0].texCoords.y = self.v2
            self.verticies[1].texCoords.x = self.u
            self.verticies[1].texCoords.y = self.v
            self.verticies[2].texCoords.x = self.u2
            self.verticies[2].texCoords.y = self.v
            self.verticies[3].texCoords.x = self.u2
            self.verticies[3].texCoords.y = self.v2

    def draw(self, slot):
        skeleton = slot.skeleton

        r = skeleton.r * slot.r * 255.0
        g = skeleton.g * slot.g * 255.0
        b = skeleton.b * slot.b * 255.0
        a = skeleton.a * slot.a * 255.0

        self.verticies[0].color.r = r
        self.verticies[0].color.g = g
        self.verticies[0].color.b = b
        self.verticies[0].color.a = a
        self.verticies[1].color.r = r
        self.verticies[1].color.g = g
        self.verticies[1].color.b = b
        self.verticies[1].color.a = a
        self.verticies[2].color.r = r
        self.verticies[2].color.g = g
        self.verticies[2].color.b = b
        self.verticies[2].color.a = a
        self.verticies[3].color.r = r
        self.verticies[3].color.g = g
        self.verticies[3].color.b = b
        self.verticies[3].color.a = a

        self.updateOffset()
        self.updateWorldVerticies(slot.bone)

        skeleton.texture = self.texture
        skeleton.vertexArray.append(self.verticies[0])
        skeleton.vertexArray.append(self.verticies[1])
        skeleton.vertexArray.append(self.verticies[2])
        skeleton.vertexArray.append(self.verticies[3])

    def updateWorldVertices(self, bone):
        x = bone.worldX
        y = bone.worldY
        m00 = bone.m00
        m01 = bone.m01
        m10 = bone.m10
        m11 = bone.m11
        self.verticies[0].texCoords.x = self.offset[0] * m00 + self.offset[1] * m01 + x
        self.verticies[0].texCoords.y = self.offset[0] * m10 + self.offset[1] * m11 + y
        self.verticies[1].texCoords.x = self.offset[2] * m00 + self.offset[3] * m01 + x
        self.verticies[1].texCoords.y = self.offset[2] * m10 + self.offset[3] * m11 + y
        self.verticies[2].texCoords.x = self.offset[4] * m00 + self.offset[5] * m01 + x
        self.verticies[2].texCoords.y = self.offset[4] * m10 + self.offset[5] * m11 + y
        self.verticies[3].texCoords.x = self.offset[6] * m00 + self.offset[7] * m01 + x
        self.verticies[3].texCoords.y = self.offset[6] * m10 + self.offset[7] * m11 + y
