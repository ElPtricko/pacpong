import random

import cocos, cocos.collision_model as cm, cocos.euclid as eu, pyglet
from cocos.actions import *
from glvars import *


class Paddle(cocos.sprite.Sprite):
    def __init__(self, side):
        super().__init__(pyglet.resource.image('paddle.png'))
        self.velocity = (0, 0)
        self.invert = False
        self.stop = False
        self.scale_y = 1.7 * (windowY / 900)
        self.scale_x = 0.7 * (windowX / 1440)
        if side == 'left':
            self.position = 80 * (windowX / 1440), (windowY / 2)
        if side == 'right':
            self.position = windowX - 80 * (windowX / 1440), (windowY / 2)
        self.cshape = cm.AARectShape(eu.Vector2(*self.position), (14.3 * (windowX / 1440)) / (displayfrequency / 60),
                                     self.height / 2)


class GhostBall(cocos.sprite.Sprite):
    def __init__(self, practice):
        super().__init__(pyglet.resource.image('ghost.png'))
        self.velocity = (0, 0)
        self.scale_x = self.scale_y = 0.6 * (windowX / 1440)
        self.color = (100, 255, 0)
        if practice is True:
            self.dx = -1 * (14.4 * (windowX / 1440)) / (displayfrequency / 60)
            self.position = (500 * (windowX / 1440)), (windowY / 2)
        else:
            self.dx = (14.4 * (windowX / 1440)) / (displayfrequency / 60)
            self.position = (windowX - 50 * (windowX / 1440)), (windowY / 2)
        self.dy = (14.4 * (windowY / 900)) / (displayfrequency / 60)
        self.cshape = cm.CircleShape(eu.Vector2(*self.position), self.width / 2)
        self.do(Repeat(RotateBy(15, 0.05) + RotateBy(-30, 0.1) + RotateBy(15, 0.05)))


class PacBall(cocos.sprite.Sprite):
    def __init__(self, side, scale=0.2):
        super().__init__('pacballblue.gif')
        self.velocity = (0, 0)
        self.scale_x = self.scale_y = scale * (windowX / 1440)
        self.invert = False
        self.stop = False
        if side is 'left':
            self.image = pyglet.resource.animation('pacballred.gif', flip_x=True)
            self.position = (windowX / 4), (windowY / 2) + self.width / 4
            self.cshape = cm.AARectShape(eu.Vector2(*self.position), (14 * (windowX / 1440)) / (displayfrequency / 60),
                                         abs(self.height * 2 / 3))
            self.anchor = -self.width * 2 / 7, self.height * 3 / 18
        if side is 'right':
            self.image = pyglet.resource.animation('pacballblue.gif')
            self.position = ((windowX / 4) * 3, windowY / 2 + self.width / 4)
            self.cshape = cm.AARectShape(eu.Vector2(*self.position), (14 * (windowX / 1440)) / (displayfrequency / 60),
                                         abs(self.height * 2 / 3))
            self.anchor = self.width * 2 / 7, self.height * 3 / 18


class FireBall(cocos.sprite.Sprite):
    def __init__(self, pointto=None):
        super().__init__(pyglet.resource.animation('fireball.gif'), position=(-100, -100), rotation=90)
        if pointto is not None:
            self.rotation = 270
        self.scale_x = self.scale_y = 0.5 * (windowX / 1440)


class Healing(cocos.sprite.Sprite):
    def __init__(self):
        super().__init__(pyglet.resource.image('healing2.png'), position=(-100, -100))
        self.scale_x = self.scale_y = 0.4 * (windowX / 1440)
        self.opacity = 170


class SpeedUp(cocos.sprite.Sprite):
    def __init__(self):
        super().__init__(pyglet.resource.animation('spiral.gif'), position=(-1000, -1000))
        self.scale_x = self.scale_y = ((windowX / 2 - 100 * ((windowX + windowY) / (1440 + 900))) / self.width)
        self.color = (255, 0, 255)
        self.opacity = 70


class Bg(cocos.sprite.Sprite):
    def __init__(self):
        super().__init__('bgorange.png')
        randnum = random.randrange(1, 3)
        if randnum is 1:
            self.image = pyglet.resource.image('bgorange.png')
        elif randnum is 2:
            self.image = pyglet.resource.image('bgpurple.png')
        self.scale_x = windowX / self.width
        self.scale_y = windowY / self.height
        self.position = windowX / 2, (windowY / 2)


class PowersIndicator(cocos.sprite.Sprite):
    def __init__(self):
        super().__init__(pyglet.resource.image('powers.png'))
        self.scale_x = 0.32 * (windowX / 1440)
        self.scale_y = 0.35 * (windowX / 1440)
        self.position = (windowX / 2, self.height / 2 + (20 * (windowY / 900)))


class BackgroundLayer(cocos.layer.Layer):
    def __init__(self, winner=None):
        super().__init__()
        credits1 = cocos.text.Label('Developer   -   Patrick Ravnholt',
                                    (windowX - (50 * windowX / 1440), 80 * (windowY / 900)),
                                    font_name=FN, color=(150, 150, 150, 255),
                                    font_size=21 * ((windowX + windowY) / (1440 + 900)), anchor_x='right',
                                    anchor_y='bottom')
        credits2 = cocos.text.Label('Designer & Animator  -   Adri Evans',
                                    (windowX - (50 * windowX / 1440), 40 * (windowY / 900)),
                                    font_name=FN, color=(150, 150, 150, 255),
                                    font_size=21 * ((windowX + windowY) / (1440 + 900)), anchor_x='right',
                                    anchor_y='bottom')
        credits3 = cocos.text.Label('Bautista Cazeaux  -  Concept & Marketing',
                                    ((50 * windowX / 1440), 40 * (windowY / 900)),
                                    font_name=FN, color=(150, 150, 150, 255),
                                    font_size=21 * ((windowX + windowY) / (1440 + 900)), anchor_x='left',
                                    anchor_y='bottom')
        credits4 = cocos.text.Label('Pablo Pazos  -  Marketing', ((50 * windowX / 1440), 80 * (windowY / 900)),
                                    font_name=FN,
                                    color=(150, 150, 150, 255), font_size=21 * ((windowX + windowY) / (1440 + 900)),
                                    anchor_x='left', anchor_y='bottom')
        self.add(Bg())
        self.add(PacBall('left', 0.3))
        self.add(PacBall('right', 0.3))
        self.add(cocos.layer.ColorLayer(0, 0, 0, 150, windowX, windowY))
        self.add(credits1)
        self.add(credits2)
        self.add(credits3)
        self.add(credits4)
        if winner is None:
            pass
        elif 'LEFT' in winner:
            win = cocos.text.Label('WINNER', (windowX * 1.3 / 8, windowY * 4 / 6), font_name=FN,
                                   color=(0, 200, 30, 255),
                                   font_size=60 * ((windowX + windowY) / (1440 + 900)), anchor_x='center',
                                   anchor_y='center')
            lose = cocos.text.Label('LOSER', (windowX * 6.7 / 8, windowY * 4 / 6), font_name=FN,
                                    color=(200, 0, 10, 255),
                                    font_size=60 * ((windowX + windowY) / (1440 + 900)), anchor_x='center',
                                    anchor_y='center')
            lose.rotation = 20
            win.rotation = -20
            self.add(win)
            self.add(lose)
        elif 'RIGHT' in winner:
            win = cocos.text.Label('WINNER', (windowX * 6.7 / 8, windowY * 4 / 6), font_name=FN,
                                   color=(0, 200, 30, 255),
                                   font_size=50 * ((windowX + windowY) / (1440 + 900)), anchor_x='center',
                                   anchor_y='center')
            lose = cocos.text.Label('LOSER', (windowX * 1.3 / 8, windowY * 4 / 6), font_name=FN,
                                    color=(200, 0, 10, 255),
                                    font_size=50 * ((windowX + windowY) / (1440 + 900)), anchor_x='center',
                                    anchor_y='center')
            lose.rotation = -20
            win.rotation = 20
            self.add(win)
            self.add(lose)
        elif 'TIE' in winner:
            win = cocos.text.Label('TIED', (windowX * 1.3 / 8, windowY * 4 / 6), font_name=FN, color=(200, 200, 0, 255),
                                   font_size=50 * ((windowX + windowY) / (1440 + 900)), anchor_x='center',
                                   anchor_y='center')
            lose = cocos.text.Label('TIED', (windowX * 6.7 / 8, windowY * 4 / 6), font_name=FN,
                                    color=(200, 200, 0, 255),
                                    font_size=50 * ((windowX + windowY) / (1440 + 900)), anchor_x='center',
                                    anchor_y='center')
            lose.rotation = 20
            win.rotation = -20
            self.add(win)
            self.add(lose)
