import cocos, cocos.collision_model as cm, cocos.euclid as eu, pyglet
from cocos.actions import *
from glvars import *


class Paddle(cocos.sprite.Sprite):
    def __init__(self, img, side):
        super().__init__(pyglet.resource.image(img))
        self.velocity = (0, 0)
        self.invert = False
        self.stop = False
        self.scale_y = 1.8 * (windowY / 900)
        self.scale_x = 0.7 * (windowX / 1440)
        if side == 'left':
            self.position = 80 * (windowX / 1440), (windowY / 2)
        if side == 'right':
            self.position = windowX - 80 * (windowX / 1440), (windowY / 2)
        self.cshape = cm.AARectShape(eu.Vector2(*self.position), self.width/2, self.height/2)


class GhostBall(cocos.sprite.Sprite):
    def __init__(self, img):
        super().__init__(pyglet.resource.image(img))
        self.velocity = (0, 0)
        self.scale_x = self.scale_y = 0.6 * (windowX/1440)
        self.color = (100, 255, 0)
        self.dx = (14.4 * (windowX/1440)) / (displayfrequency/60)
        self.dy = (14.4 * (windowY/900)) / (displayfrequency/60)
        self.position = (windowX - 500 * (windowX/1440)), (windowY/2)
        self.cshape = cm.CircleShape(eu.Vector2(*self.position), self.width/2)
        self.do(Repeat(RotateBy(15, 0.05) + RotateBy(-30, 0.1) + RotateBy(15, 0.05)))


class PacBall(cocos.sprite.Sprite):
    def __init__(self, img, color, side):
        super().__init__(img)
        self.velocity = (0, 0)
        self.scale_x = self.scale_y = 0.5 * (windowX/1440)
        self.color = color
        self.invert = False
        self.stop = False
        if side is 'left':
            self.image = pyglet.resource.image(img)
            self.position = (windowX/4), (windowY/2)
        if side is 'right':
            self.image = pyglet.resource.image(img, flip_x=True)
            self.position = ((windowX/4)*3, windowY/2)
        self.cshape = cm.CircleShape(eu.Vector2(*self.position), abs(self.width)/2)
        self.do(Repeat(RotateBy(15, 0.1) + RotateBy(-30, 0.2) + RotateBy(15, 0.1)))


class FireBall(cocos.sprite.Sprite):
    def __init__(self, pointto=None):
        super().__init__(pyglet.resource.animation('fireball.gif'), position=(-100, -100), rotation=90)
        if pointto is not None:
            self.rotation = 270
        self.scale_x = self.scale_y = 0.5 * (windowX/1440)


class Healing(cocos.sprite.Sprite):
    def __init__(self):
        super().__init__(pyglet.resource.image('healing2.png'), position=(-100, -100))
        self.scale_x = self.scale_y = 0.4 * (windowX/1440)
        self.opacity = 170


class SpeedUp(cocos.sprite.Sprite):
    def __init__(self):
        super().__init__(pyglet.resource.animation('spiral.gif'), position=(-1000, -1000))
        self.scale_x = self.scale_y = ((windowX/2-100*((windowX+windowY)/(1440+900)))/self.width)
        self.color = (255, 0, 255)
        self.opacity = 70
