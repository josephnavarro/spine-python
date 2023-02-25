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
        "myfont",
    ]

    def __init__(self, skeletonData: spine.SkeletonData):
        super(Skeleton, self).__init__(skeletonData=skeletonData)
        # Draw the FPS in the bottom right corner.
        pygame.font.init()
        self.myfont = pygame.font.SysFont(None, 24, bold=True)
        self.x = 0
        self.y = 0
        self.texture = None
        self.debug: bool = True
        self.images: list = []
        self.clock = None

    def draw(
            self, screen, states,
            *,
            _flip=pygame.transform.flip,
            _rotozoom=pygame.transform.rotozoom,
            _smoothscale=pygame.transform.smoothscale,
            _int=int,
            _blend=pygame.BLEND_RGBA_MULT,
    ):
        for slot in self.drawOrder:
            attachment: (RegionAttachment | None) = slot.attachment
            if attachment is not None:
                texture: (pygame.Surface | None) = attachment.texture.copy()
                if texture is not None:
                    attachX = attachment.x
                    attachY = attachment.y
                    attachScaleX = attachment.scaleX
                    attachScaleY = attachment.scaleY
                    attachRotation = attachment.rotation
                    bone = slot.bone
                    worldX = bone.worldX
                    worldY = bone.worldY
                    m00 = bone.m00
                    m01 = bone.m01
                    m10 = bone.m10
                    m11 = bone.m11
                    worldRotation = bone.worldRotation
                    worldScaleX = bone.worldScaleX
                    worldScaleY = bone.worldScaleY

                    rotation: float = -(worldRotation + attachRotation)
                    xScale: float = worldScaleX + attachScaleX - 1
                    if self.flipX:
                        xScale = -xScale
                        rotation = -rotation

                    yScale: float = worldScaleY + attachScaleY - 1
                    if self.flipY:
                        yScale = -yScale
                        rotation = -rotation

                    flipX: bool = False
                    if xScale < 0:
                        flipX = True
                        xScale = math.fabs(xScale)

                    flipY: bool = False
                    if yScale < 0:
                        flipY = True
                        yScale = math.fabs(yScale)

                    texture.fill((slot.r, slot.g, slot.b, slot.a), None, _blend)

                    # center = texture.get_rect().center
                    texture = _flip(texture, flipX, flipY)
                    texture = _smoothscale(texture, (_int(texture.get_width() * xScale), _int(texture.get_height() * yScale)))
                    texture = _rotozoom(texture, -rotation, 1)

                    # Center image
                    x: float = worldX + (attachX * m00) + (attachY * m01) + self.x - texture.get_width() * 0.5
                    y: float = -(worldY + (attachX * m10) + (attachY * m11)) + self.y - texture.get_height() * 0.5
                    screen.blit(texture, (x, y))

        if self.debug:
            if not self.clock:
                self.clock = pygame.time.Clock()
            self.clock.tick()

            mytext = self.myfont.render('FPS: %.2f' % self.clock.get_fps(), True, (255, 255, 255))
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
