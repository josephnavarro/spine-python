#! usr/bin/env python3
import math
import pygame
import spine
from .RegionAttachment import RegionAttachment
from .Circle import Circle
from .Line import Line


class Skeleton(spine.Skeleton):
    __slots__ = [
        "x",
        "y",
        "texture",
        "debug",
        "images",
        "clock",
    ]

    def __init__(self, skeletonData: spine.SkeletonData):
        super(Skeleton, self).__init__(skeletonData=skeletonData)
        self.x = 0
        self.y = 0
        self.texture = None
        self.debug: bool = True
        self.images: list = []
        self.clock = None

    def draw(self, screen, states):
        for slot in self.drawOrder:
            attachment: (RegionAttachment | None) = slot.attachment
            if attachment is not None:
                texture: (pygame.Surface | None) = attachment.texture.copy()
                if texture:
                    x = slot.bone.worldX + slot.attachment.x * slot.bone.m00 + slot.attachment.y * slot.bone.m01
                    y = -(slot.bone.worldY + slot.attachment.x * slot.bone.m10 + slot.attachment.y * slot.bone.m11)
                    rotation = -(slot.bone.worldRotation + slot.attachment.rotation)
                    xScale = slot.bone.worldScaleX + slot.attachment.scaleX - 1
                    yScale = slot.bone.worldScaleY + slot.attachment.scaleY - 1

                    x += self.x
                    y += self.y

                    if self.flipX:
                        xScale = -xScale
                        rotation = -rotation
                    if self.flipY:
                        yScale = -yScale
                        rotation = -rotation

                    flipX = False
                    flipY = False

                    if xScale < 0:
                        flipX = True
                        xScale = math.fabs(xScale)
                    if yScale < 0:
                        flipY = True
                        yScale = math.fabs(yScale)

                    texture.fill((slot.r, slot.g, slot.b, slot.a), None, pygame.BLEND_RGBA_MULT)

                    # center = texture.get_rect().center
                    texture = pygame.transform.flip(texture, flipX, flipY)
                    texture = pygame.transform.smoothscale(texture, (int(texture.get_width() * xScale), int(texture.get_height() * yScale)))
                    texture = pygame.transform.rotozoom(texture, -rotation, 1)

                    # Center image
                    x = x - texture.get_width() * 0.5
                    y = y - texture.get_height() * 0.5
                    screen.blit(texture, (x, y))

        if self.debug:
            if not self.clock:
                self.clock = pygame.time.Clock()
            self.clock.tick()
            # Draw the FPS in the bottom right corner.
            pygame.font.init()
            myfont = pygame.font.SysFont(None, 24, bold=True)
            mytext = myfont.render('FPS: %.2f' % self.clock.get_fps(), True, (255, 255, 255))

            screen.blit(mytext, (screen.get_width() - mytext.get_width(), screen.get_height() - mytext.get_height()))

            for bone in self.bones:

                if not bone.line:
                    bone.line = Line(bone.data.length)
                bone.line.x = bone.worldX + self.x
                bone.line.y = -bone.worldY + self.y
                bone.line.rotation = -bone.worldRotation
                bone.line.color = (255, 0, 0)

                if self.flipX:
                    bone.line.xScale = -1
                    bone.line.rotation = -bone.line.rotation
                else:
                    bone.line.xScale = 1
                if self.flipY:
                    bone.line.yScale = -1
                    bone.line.rotation = -bone.line.rotation
                else:
                    bone.line.yScale = 1

                bone.line.x1 = bone.line.x + math.cos(math.radians(bone.line.rotation)) * bone.line.length
                bone.line.y1 = bone.line.y + math.sin(math.radians(bone.line.rotation)) * bone.line.length

                pygame.draw.line(screen, bone.line.color, (bone.line.x, bone.line.y), (bone.line.x1, bone.line.y1))

                if not bone.circle:
                    bone.circle = Circle(0, 0, 3)
                bone.circle.x = int(bone.worldX) + self.x
                bone.circle.y = -int(bone.worldY) + self.y
                bone.circle.color = (0, 255, 0)

                if 'top left' in bone.data.name:
                    bone.circle.color = (255, 0, 0)
                if 'top right' in bone.data.name:
                    bone.circle.color = (255, 140, 0)
                if 'bottom right' in bone.data.name:
                    bone.circle.color = (255, 255, 0)
                if 'bottom left' in bone.data.name:
                    bone.circle.color = (199, 21, 133)

                pygame.draw.circle(
                    screen,
                    bone.circle.color,
                    (bone.circle.x, bone.circle.y),
                    bone.circle.r,
                    0,
                )
