import random
from cocos import director
from cocos.menu import *
from cocos.scene import Scene
from cocos.scenes import *
from pyglet.window import key
from progressBar import *
from sprites import *


class GameScene(cocos.layer.ColorLayer):
    is_event_handler = True

    def __init__(self):
        super(GameScene, self).__init__(70, 100, 175, 255)
        self.pointsl = cocos.text.Label('POINTS: ' + str(left_points), ((120*(windowX/1440)), 50*(windowY/900)),
                                        font_size=16*((windowX+windowY) / (1440+900)), font_name=FN,
                                        color=(0, 0, 0, 255), anchor_x='center', anchor_y='center')
        self.add(self.pointsl)
        self.pointsr = cocos.text.Label('POINTS: ' + str(right_points), ((windowX-120*(windowX/1440)),
                                                                         50*(windowY/900)),
                                        font_size=16*((windowX+windowY) / (1440+900)), font_name=FN,
                                        color=(0, 0, 0, 255), anchor_x='center', anchor_y='center')
        self.pointsr.do((RotateBy(10, 0.04) + RotateBy(-20, 0.08) +
                        RotateBy(10, 0.04)) * 11)
        self.pointsr.do(ScaleBy(1.7, 1.1) + ScaleTo(1, 0.5))
        self.pointsr.do(MoveBy((-135 * (windowX / 1440), 0), 0.63) +
                        MoveBy((0, 70 * (windowY / 900)), 0.63) +
                        MoveBy((0, -70 * (windowY / 900)), 0.3) +
                        MoveBy((135 * (windowX / 1440), 0), 0.3))
        self.add(self.pointsr)

        # Paddles
        self.paddleLeft = Paddle("paddle.png", 'left')
        self.add(self.paddleLeft, z=1)
        self.paddleRight = Paddle("paddle.png", 'right')
        self.add(self.paddleRight, z=1)

        # Ghost Ball
        self.GhostBall = GhostBall("ghost.png")
        self.add(self.GhostBall)
        # Pac ball
        self.pacleft = PacBall("pacball.png", (255, 0, 0), 'left')
        self.add(self.pacleft)
        self.pacright = PacBall("pacball.png", (200, 200, 200), 'right')
        self.add(self.pacright)

        self.coll_manager = cm.CollisionManagerBruteForce()
        self.fireball = FireBall()
        self.add(self.fireball)
        self.fireball2 = FireBall('s')
        self.add(self.fireball2)
        self.heal = Healing()
        self.add(self.heal)
        self.heal2 = Healing()
        self.add(self.heal2)
        self.speed = SpeedUp()
        self.add(self.speed)
        self.speed2 = SpeedUp()
        self.add(self.speed2)
        self.healthbar = HealthBar()
        self.add(self.healthbar)
        self.power = PowerBar()
        self.add(self.power)

        self.pointsl.do(PointslAction())
        self.pointsr.do(PointsrAction())
        self.paddleLeft.do(MovePaddleLeft())
        self.paddleRight.do(MovePaddleRight())
        self.pacleft.do(MovePacl())
        self.GhostBall.do(MoveBall())
        self.pacright.do(MovePacr())

    def updateobj(self, dt):
        global ballCollidingL, ballCollidingR, paccollisionl, paccollisionr, powerright, powerleft
        self.GhostBall.position = ballpos
        self.paddleLeft.position = pl
        self.paddleRight.position = pr
        self.pacright.position = pacr
        self.pacleft.position = pacl

        self.GhostBall.cshape.center = eu.Vector2(*self.GhostBall.position)
        self.paddleLeft.cshape.center = eu.Vector2(*self.paddleLeft.position)
        self.paddleRight.cshape.center = eu.Vector2(*self.paddleRight.position)
        self.pacleft.cshape.center = eu.Vector2(*self.pacleft.position)
        self.pacright.cshape.center = eu.Vector2(*self.pacright.position)

        if self.coll_manager.they_collide(self.GhostBall, self.paddleRight):
            ballCollidingR = True
            powerright += 10
        if self.coll_manager.they_collide(self.GhostBall, self.paddleLeft):
            ballCollidingL = True
            powerleft += 10
        if self.coll_manager.they_collide(self.pacleft, self.GhostBall):
            paccollisionl = True
        if self.coll_manager.they_collide(self.pacright, self.GhostBall):
            paccollisionr = True

    def on_key_press(self, symbol, mod):
        global powerright, powerleft, paclhp, pacrhp
        if powerleft > 20 and symbol == key.C:
            powerleft -= 20
            pacrhp -= 5
            self.fireball2.position = pacl
            self.fireball2.do(MoveBy((abs(pacl[0]+self.pacleft.width/2-pacr[0]), pacr[1]-pacl[1]), 0.4) +
                              MoveTo((-100, -100), 0))
            self.pacright.do(NoMove())
            self.pacright.do(Delay(0.3)+MoveNormal())
        if powerright > 20 and symbol == key.M:
            powerright -= 20
            paclhp -= 5
            self.fireball.position = pacr
            self.fireball.do(MoveBy(((pacl[0] + self.pacleft.width/2)-pacr[0], pacl[1]-pacr[1]), 0.4) +
                             MoveTo((-100, -100), 0))
            self.pacleft.do(NoMove())
            self.pacleft.do(Delay(0.3)+MoveNormal())
        if powerleft > 0 and symbol == key.V:
            paclhp += 20
            powerleft -= 0
            self.heal.do(MoveTo(pacl, 0)+ScaleTo(1.7, 0.2)+ScaleTo(1.2, 0.2)+ScaleTo(1.7, 0.2)
                         + ScaleTo(1.2, 0.2)+MoveTo((-100, 100), 0))
            self.pacleft.do(NoMove())
            self.pacleft.do(Delay(0.8) + MoveNormal())
        if powerright > 0 and symbol == key.N:
            pacrhp += 20
            powerright -= 0
            self.heal2.do(MoveTo(pacr, 0)+ScaleTo(1.7, 0.2)+ScaleTo(1.2, 0.2)+ScaleTo(1.7, 0.2)
                          + ScaleTo(1.2, 0.2)+MoveTo((-100, 100), 0))
            self.pacright.do(NoMove())
            self.pacright.do(Delay(0.8) + MoveNormal())
        if powerleft > 70 and symbol == key.F:
            self.speed.do(MoveTo((self.width/2+self.speed.width/2, self.speed.height/2), 0) + Delay(5) +
                          MoveTo((-1000, -1000), 0))
            self.pacright.do(MoveFaster())
            self.pacright.do(Delay(5) + MoveNormal())
            powerleft -= 70
        if powerright > 70 and symbol == key.H:
            self.speed2.do(MoveTo((self.width/2-self.speed2.width/2, self.speed.height/2), 0) + Delay(5) +
                           MoveTo((-1000, -1000), 0))
            self.pacleft.do(MoveFaster())
            self.pacleft.do(Delay(5) + MoveNormal())
            powerright -= 70


class HealthBar(cocos.layer.ColorLayer):
    def __init__(self):
        w, h = director.director.get_window_size()
        super(HealthBar, self).__init__(100, 100, 200, 0, width=w-6, height=40)
        self.position = (3, h - 43)
        self.progressbar = ProgressBar(int(self.width/2), 40)
        self.progressbar.position = 0, 0
        self.progressbar2 = ProgressBar(int(self.width/2), 40)
        self.progressbar2.position = self.width-self.progressbar2.width, 0

        label = cocos.text.Label("HEALTH", position=(self.progressbar.position[0] +
                                                     self.progressbar.width-20*(windowX/1440),
                                                     self.progressbar.position[1]+self.progressbar.height/2),
                                 color=(0, 0, 0, 255), font_size=10*((windowX+windowY)/(1440+900)), font_name=FN,
                                 anchor_x='right', anchor_y='center')
        label2 = cocos.text.Label("HEALTH", position=(self.progressbar.position[0] +
                                                      self.progressbar2.width+20*(windowX/1440),
                                                      self.progressbar2.position[1]+self.progressbar2.height/2),
                                  color=(0, 0, 0, 255), font_size=10*((windowX+windowY)/(1440+900)), font_name=FN,
                                  anchor_x='left', anchor_y='center')
        health = cocos.text.Label("100 | 100", position=(self.progressbar.position[0]+20*(windowX/1440),
                                                         self.progressbar.position[1]+self.progressbar.height/2),
                                  color=(0, 0, 0, 255), font_size=10*((windowX+windowY)/(1440+900)), font_name=FN,
                                  anchor_x='left', anchor_y='center')
        health2 = cocos.text.Label("100 | 100", position=(self.progressbar2.position[0]+self.progressbar2.width -
                                                          20*(windowX/1440),
                                                          self.progressbar2.position[1]+self.progressbar2.height/2),
                                   color=(0, 0, 0, 255), font_size=10*((windowX+windowY)/(1440+900)), font_name=FN,
                                   anchor_x='right', anchor_y='center')

        self.add(self.progressbar)
        self.add(self.progressbar2)
        self.progressbar2.do(UpdateBarRight())
        self.progressbar.do(UpdateBarLeft())
        health.do(UpdateHealthLeft())
        health2.do(UpdateHealthRight())
        self.add(health)
        self.add(health2)
        self.add(label)
        self.add(label2)


class PowerBar(cocos.layer.ColorLayer):
    is_event_handler = True

    def __init__(self):
        w, h = director.director.get_window_size()
        super(PowerBar, self).__init__(100, 100, 200, 0, width=w-6, height=40)
        self.position = (3, h - 83)
        self.progressbar = ProgressPowerBar(int(self.width/2), 40)
        self.progressbar.position = 0, 0
        self.add(self.progressbar)
        self.progressbar2 = ProgressPowerBar(int(self.width/2), 40)
        self.progressbar2.position = self.width-self.progressbar2.width, 0
        self.add(self.progressbar2)
        label = cocos.text.Label("POWER", position=(self.progressbar.position[0] +
                                                    self.progressbar.width-20*(windowX/1440),
                                                    self.progressbar.position[1]+self.progressbar.height/2),
                                 color=(0, 0, 0, 255), font_size=10*((windowX+windowY)/(1440+900)), font_name=FN,
                                 anchor_x='right', anchor_y='center')
        label2 = cocos.text.Label("POWER", position=(self.progressbar.position[0]+
                                                     self.progressbar2.width+20*(windowX/1440),
                                                     self.progressbar2.position[1]+self.progressbar2.height/2),
                                  color=(0, 0, 0, 255), font_size=10*((windowX+windowY)/(1440+900)), font_name=FN,
                                  anchor_x='left', anchor_y='center')
        power = cocos.text.Label("%d | 100" % powerleft,
                                 position=(self.progressbar.position[0]+20*(windowX/1440),
                                           self.progressbar.position[1]+self.progressbar.height/2),
                                 color=(0, 0, 0, 255), font_size=10*((windowX+windowY)/(1440+900)), font_name=FN,
                                 anchor_x='left', anchor_y='center')
        power2 = cocos.text.Label("%d | 100" % powerright,
                                  position=(self.progressbar2.position[0]+self.progressbar2.width-20*(windowX/1440),
                                            self.progressbar2.position[1]+self.progressbar2.height/2),
                                  color=(0, 0, 0, 255), font_size=10*((windowX+windowY)/(1440+900)), font_name=FN,
                                  anchor_x='right', anchor_y='center')
        self.progressbar.set_progress(powerleft)
        self.progressbar2.set_progress(powerright)
        self.progressbar.do(UpdatePowerLeft())
        self.progressbar2.do(UpdatePowerRight())
        power.do(UpdatePowerTL())
        power2.do(UpdatePowerTR())
        self.add(power)
        self.add(power2)
        self.add(label)
        self.add(label2)

    def update_bar(self, dt):
        global powerright, powerleft
        if powerright < 100:
            powerright += 0.05
        elif powerright >= 100:
            powerright = 100
        if powerleft < 100:
            powerleft += 0.05
        elif powerleft >= 100:
            powerleft = 100


# ACTIONS #
class NoMove(cocos.actions.Action):
    def step(self, dt):
        super().step(dt)
        self.target.dx = 0


class MoveNormal(cocos.actions.Action):
    def step(self, dt):
        super().step(dt)
        self.target.dx = 1


class MoveFaster(cocos.actions.Action):
    def step(self, dt):
        super().step(dt)
        self.target.dx = 2


class UpdatePowerTR(cocos.actions.Action):
    def step(self, dt):
        super().step(dt)
        self.target.element.text = '%d | 100' % powerright


class UpdatePowerTL(cocos.actions.Action):
    def step(self, dt):
        super().step(dt)
        self.target.element.text = '%d | 100' % powerleft


class UpdateHealthRight(cocos.actions.Action):
    def step(self, dt):
        super().step(dt)
        self.target.element.text = '%d | 100' % pacrhp


class UpdateHealthLeft(cocos.actions.Action):
    def step(self, dt):
        super().step(dt)
        self.target.element.text = '%d | 100' % paclhp


class UpdatePowerRight(cocos.actions.Action):
    def step(self, dt):
        super().step(dt)
        self.target.set_progress(powerright*0.01)


class UpdatePowerLeft(cocos.actions.Action):
    def step(self, dt):
        super().step(dt)
        self.target.set_progress(powerleft*0.01)


class UpdateBarRight(cocos.actions.Action):
    def step(self, dt):
        super().step(dt)
        if pacrhp <= 0.0:
            game_over()
        else:
            self.target.set_progress(pacrhp*0.01)


class UpdateBarLeft(cocos.actions.Action):
    def step(self, dt):
        if paclhp <= 0.0:
            game_over()
        else:
            self.target.set_progress(paclhp*0.01)


class PointslAction(cocos.actions.Action):
    def step(self, dt):
        super().step(dt)
        global addedpointL
        self.target.element.text = 'POINTS: %d' % left_points
        if addedpointL:
            addedpointL = False
            self.target.do((RotateBy(10, 0.04) + RotateBy(-20, 0.08) +
                            RotateBy(10, 0.04))*7)
            self.target.do(ScaleBy(1.7, 0.5) + ScaleTo(1, 0.5))
            self.target.do(MoveBy((135 * (windowX/1440), 0), 0.3) +
                           MoveBy((0, 70 * (windowY / 900)), 0.3) +
                           MoveBy((0, -70 * (windowY / 900)), 0.3) +
                           MoveBy((-135 * (windowX / 1440), 0), 0.3))


class PointsrAction(cocos.actions.Action):
    def step(self, dt):
        super().step(dt)
        global addedpointR
        self.target.element.text = 'POINTS: %d' % right_points
        if addedpointR:
            addedpointR = False
            self.target.do((RotateBy(10, 0.04) + RotateBy(-20, 0.08) +
                            RotateBy(10, 0.04)) * 7)
            self.target.do(ScaleBy(1.7, 0.5) + ScaleTo(1, 0.5))
            self.target.do(MoveBy((-135 * (windowX/1440), 0), 0.3) +
                           MoveBy((0, 70 * (windowY / 900)), 0.3) +
                           MoveBy((0, -70 * (windowY / 900)), 0.3) +
                           MoveBy((135 * (windowX / 1440), 0), 0.3))


class MoveBall(cocos.actions.Move):
    def step(self, dt):
        super().step(dt)
        global ballpos, ballCollidingR, ballCollidingL, left_points, \
            right_points, addedpointR, addedpointL, paccollisionr, paccollisionl, paclhp, pacrhp
        self.target.y = (self.target.y + self.target.dy)
        self.target.x = (self.target.x + self.target.dx)
        ballpos = self.target.position

        if self.target.y > windowY - (self.target.height/2 + 110 * (windowY / 900)):
            self.target.y = windowY - (self.target.height/2 + 105 * (windowY / 900))
            self.target.dy *= -1
        if self.target.y < (self.target.height/2 + 110 * (windowY / 900)):
            self.target.y = (self.target.height/2 + 105 * (windowY / 900))
            self.target.dy *= -1

        if -self.target.width > self.target.x > (-abs(self.target.dx))-self.target.width:
            right_points += 1
            addedpointR = True
        if windowX+self.target.width < self.target.x < abs(self.target.dx)+windowX+self.target.width:
            left_points += 1
            addedpointL = True

        if self.target.x > windowX+self.target.width+calculate_seconds(self.target.dx, 3):
            self.target.position = (windowX/2, windowY/2)
            self.target.dx *= -1
            self.target.dy *= random.randrange(-1, 2, 2)
        if self.target.x < -self.target.width-calculate_seconds(self.target.dx, 3):
            self.target.position = (windowX/2, windowY/2)
            self.target.dx *= -1
            self.target.dy *= random.randrange(-1, 2, 2)

        if ballCollidingL:
            ballCollidingL = False
            self.target.dx *= -1
            self.target.x += 40 * (windowX/1440)
        if ballCollidingR:
            ballCollidingR = False
            self.target.dx *= -1
            self.target.x -= 40 * (windowX/1440)
        if paccollisionl:
            paclhp -= 25
            if self.target.dx < 0:
                self.target.x -= 40 * (windowX/1440)
            if self.target.dx > 0:
                self.target.x += 40 * (windowX/1440)
            if self.target.dy < 0:
                self.target.y -= 40 * (windowY / 900)
            if self.target.dy > 0:
                self.target.y += 40 * (windowY / 900)
            paccollisionl = False
        if paccollisionr:
            pacrhp -= 25
            if self.target.dx < 0:
                self.target.x -= 40 * (windowX / 1440)
            if self.target.dx > 0:
                self.target.x += 40 * (windowX / 1440)
            if self.target.dy < 0:
                self.target.y -= 40 * (windowY / 900)
            if self.target.dy > 0:
                self.target.y += 40 * (windowY / 900)
            paccollisionr = False


class MovePaddleLeft(cocos.actions.Move):
    def step(self, dt):
        super().step(dt)
        if keyboard[key.Q] and not keyboard[key.Z]:
            if self.target.y > windowY - (self.target.height/2 + 110 * (windowY / 900)):
                self.target.y = windowY - (self.target.height/2 + 105 * (windowY / 900))
            else:
                self.target.do(MoveBy((0, (15 * (windowY / 900)) / (displayfrequency/60)),
                                      0.01 / (displayfrequency/60)))
        if keyboard[key.Z] and not keyboard[key.Q]:
            if self.target.y < (self.target.height/2 + 90 * (windowY / 900)):
                self.target.y = self.target.height/2 + 85 * (windowY / 900)
            else:
                self.target.do(MoveBy((0, (-15 * (windowY / 900)) / (displayfrequency/60)),
                                      0.01 / (displayfrequency/60)))
        global pl
        pl = self.target.position


class MovePaddleRight(cocos.actions.Move):
    def step(self, dt):
        super().step(dt)
        if keyboard[key.O] and not keyboard[key.PERIOD]:
            if self.target.y > windowY - (self.target.height/2 + 110 * (windowY / 900)):
                self.target.y = windowY - (self.target.height/2 + 105 * (windowY / 900))
            else:
                self.target.do(MoveBy((0, (15 * (windowY / 900)) / (displayfrequency/60)),
                                      0.01 / (displayfrequency/60)))
        if keyboard[key.PERIOD] and not keyboard[key.O]:
            if self.target.y < (self.target.height/2 + 90 * (windowY / 900)):
                self.target.y = self.target.height/2 + 85 * (windowY / 900)
            else:
                self.target.do(MoveBy((0, (-15 * (windowY / 900)) / (displayfrequency/60)),
                                      0.01 / (displayfrequency/60)))
        global pr
        pr = self.target.position


class MovePacl(cocos.actions.Move):
    def step(self, dt):
        super().step(dt)
        if self.target.dx is 1:
            if keyboard[key.W] and not keyboard[key.S]:
                if self.target.y >= windowY - (200 * (windowY / 900)):
                    self.target.y = windowY - (200 * (windowY / 900))
                else:
                    self.target.do(MoveBy((0, (10 * (windowY / 900)) / (displayfrequency/60)), 0))
            if keyboard[key.S] and not keyboard[key.W]:
                if self.target.y <= (200 * (windowY / 900)):
                    self.target.y = 200 * (windowY / 900)
                else:
                    self.target.do(MoveBy((0, (-10 * (windowY / 900)) / (displayfrequency/60)), 0))
            if keyboard[key.D] and not keyboard[key.A]:
                if self.target.x >= windowX/2 - (70*windowX/1440):
                    self.target.x = windowX/2 - (70*windowX/1440)
                else:
                    self.target.do(MoveBy(((10 * (windowX / 1440)) / (displayfrequency/60), 0), 0))
            if keyboard[key.A] and not keyboard[key.D]:
                if self.target.x <= 200 * (windowX / 1440):
                    self.target.x = 200 * (windowX / 1440)
                else:
                    self.target.do(MoveBy(((-10 * (windowX / 1440)) / (displayfrequency / 60), 0), 0))
        if self.target.dx is 2:
            if keyboard[key.W] and not keyboard[key.S]:
                if self.target.y >= windowY - (200 * (windowY / 900)):
                    self.target.y = windowY - (200 * (windowY / 900))
                else:
                    self.target.do(MoveBy((0, (20 * (windowY / 900)) / (displayfrequency/60)), 0))
            if keyboard[key.S] and not keyboard[key.W]:
                if self.target.y <= (200 * (windowY / 900)):
                    self.target.y = 200 * (windowY / 900)
                else:
                    self.target.do(MoveBy((0, (-20 * (windowY / 900)) / (displayfrequency/60)), 0))
            if keyboard[key.D] and not keyboard[key.A]:
                if self.target.x >= windowX/2 - (70*windowX/1440):
                    self.target.x = windowX/2 - (70*windowX/1440)
                else:
                    self.target.do(MoveBy(((20 * (windowX / 1440)) / (displayfrequency/60), 0), 0))
            if keyboard[key.A] and not keyboard[key.D]:
                if self.target.x <= 200 * (windowX / 1440):
                    self.target.x = 200 * (windowX / 1440)
                else:
                    self.target.do(MoveBy(((-20 * (windowX / 1440)) / (displayfrequency / 60), 0), 0))
        else:
            pass
        global pacl
        pacl = self.target.position


class MovePacr(cocos.actions.Move):
    def step(self, dt):
        super().step(dt)
        if self.target.dx is 1:
            if keyboard[key.I] and not keyboard[key.K]:
                if self.target.y >= windowY - (200 * (windowY / 900)):
                    self.target.y = windowY - (200 * (windowY / 900))
                else:
                    self.target.do(MoveBy((0, (10 * (windowY / 900)) / (displayfrequency/60)), 0))
            if keyboard[key.K] and not keyboard[key.I]:
                if self.target.y <= (200 * (windowY / 900)):
                    self.target.y = 200 * (windowY / 900)
                else:
                    self.target.do(MoveBy((0, (-10 * (windowY / 900)) / (displayfrequency/60)), 0))
            if keyboard[key.J] and not keyboard[key.L]:
                if self.target.x <= windowX/2 + (70*windowX/1440):
                    self.target.x = windowX/2 + (70*windowX/1440)
                else:
                    self.target.do(MoveBy(((-10 * (windowX / 1440)) / (displayfrequency/60), 0), 0))
            if keyboard[key.L] and not keyboard[key.J]:
                if self.target.x >= windowX - (200 * (windowX / 1440)):
                    self.target.x = windowX - (200 * (windowX / 1440))
                else:
                    self.target.do(MoveBy(((10 * (windowX / 1440)) / (displayfrequency / 60), 0), 0))
        if self.target.dx is 2:
            if keyboard[key.I] and not keyboard[key.K]:
                if self.target.y >= windowY - (200 * (windowY / 900)):
                    self.target.y = windowY - (200 * (windowY / 900))
                else:
                    self.target.do(MoveBy((0, (20 * (windowY / 900)) / (displayfrequency/60)), 0))
            if keyboard[key.K] and not keyboard[key.I]:
                if self.target.y <= (200 * (windowY / 900)):
                    self.target.y = 200 * (windowY / 900)
                else:
                    self.target.do(MoveBy((0, (-20 * (windowY / 900)) / (displayfrequency/60)), 0))
            if keyboard[key.J] and not keyboard[key.L]:
                if self.target.x <= windowX/2 + (70*windowX/1440):
                    self.target.x = windowX/2 + (70*windowX/1440)
                else:
                    self.target.do(MoveBy(((-20 * (windowX / 1440)) / (displayfrequency/60), 0), 0))
            if keyboard[key.L] and not keyboard[key.J]:
                if self.target.x >= windowX - (200 * (windowX / 1440)):
                    self.target.x = windowX - (200 * (windowX / 1440))
                else:
                    self.target.do(MoveBy(((20 * (windowX / 1440)) / (displayfrequency / 60), 0), 0))
        else:
            pass
        global pacr
        pacr = self.target.position


# End Game Scene
class EndGame(Menu):
    def __init__(self, winner):
        super().__init__(winner + ' HAS WON!')

        self.font_title = {'font_name': FN, 'font_size': 25 * ((windowX + windowY) / (1440 + 900)),
                           'color': (255, 220, 50, 255), 'anchor_y': 'center', 'anchor_x': 'center'}
        self.font_item = {'font_name': FN, 'font_size': 20 * ((windowX + windowY) / (1440 + 900)),
                          'anchor_y': 'center', 'anchor_x': 'center', 'color': (192, 192, 192, 255)}
        self.font_item_selected = {'font_name': FN, 'font_size': 30 * ((windowX + windowY) / (1440 + 900)),
                                   'anchor_y': 'center', 'anchor_x': 'center', 'color': (255, 255, 255, 255)}

        # Menu items incl. functions they trigger
        self.items = []
        self.items.append(MenuItem('PLAY AGAIN', self.start_game))
        self.items[0].y = 80
        self.items.append(MenuItem('OPTIONS', self.options))
        self.items[1].y = 40
        self.items.append(MenuItem('QUIT', self.quit))
        self.selected = 0
        self.create_menu(self.items, shake(), shake_back())

    def start_game(self):
        global paclhp, pacrhp, left_points, right_points, powerleft, powerright
        paclhp = 100
        pacrhp = 100
        left_points = -1
        right_points = 0
        powerleft = 0
        powerright = 0
        director.director.push(JumpZoomTransition(on_game_start(), 1))

    def quit(self):
        pyglet.app.exit()

    def options(self):
        pass

    def on_key_press(self, symbol, modifiers):
        if symbol in (key.ENTER, key.NUM_ENTER):
            self._activate_item()
            return True
        elif symbol in (key.DOWN, key.UP, key.S, key.W):
            if symbol == key.DOWN or symbol == key.S:
                new_idx = self.selected_index + 1
            elif symbol == key.UP or symbol == key.W:
                new_idx = self.selected_index - 1
            if new_idx < 0:
                new_idx = len(self.children) - 1
            elif new_idx > len(self.children) - 1:
                new_idx = 0
            self._select_item(new_idx)
            return True
        elif symbol in (key.Q, key.U, key.E, key.Q):
            return True


class BackgroundEnd(cocos.layer.ColorLayer):
    def __init__(self):
        super().__init__(0, 0, 0, 100)


# Used for starting the game
def on_game_start():
    thisgamescene = Scene()
    thisgamescene.add(GameScene(), z=-1, name="Game")
    thisgamescene.schedule_interval(GameScene().updateobj, (1/60)/(displayfrequency/144) * 1.1)
    thisgamescene.schedule_interval(PowerBar().update_bar, 1/20)
    return thisgamescene


def game_over():
    if paclhp > pacrhp:
        director.director.push(FadeTransition(on_game_end('THE LEFT PLAYER'), 3))
    else:
        director.director.push(FadeTransition(on_game_end('THE RIGHT PLAYER'), 3))


def on_game_end(winner):
    endscene = Scene()
    endscene.add(EndGame(winner), z=-1, name="MENU")
    endscene.add(BackgroundEnd(), z=-2, name="BG")
    return endscene


def calculate_seconds(balldx, seconds):
    ballsmth = 60 * balldx * seconds
    return abs(ballsmth)


# MAIN MENU #

class MainMenu(Menu):
    def __init__(self):
        super().__init__("PACPONG")

    # Style of menu items
        self.font_title = {'font_name': FN, 'font_size': 30 * ((windowX+windowY) / (1440+900)),
                           'color': (192, 192, 192, 255), 'anchor_y': 'center', 'anchor_x': 'center'}
        self.font_item = {'font_name': FN, 'font_size': 20 * ((windowX+windowY) / (1440+900)),
                          'anchor_y': 'center', 'anchor_x': 'center', 'color': (192, 192, 192, 255)}
        self.font_item_selected = {'font_name': FN, 'font_size': 30 * ((windowX+windowY) / (1440+900)),
                                   'anchor_y': 'center', 'anchor_x': 'center', 'color': (255, 255, 255, 255)}

    # Menu items incl. functions they trigger
        self.items = []
        self.items.append(MenuItem('PLAY', self.start_game))
        self.items[0].y = 80
        self.items.append(MenuItem('OPTIONS', self.options))
        self.items[1].y = 40
        self.items.append(MenuItem('QUIT', self.quit))
        self.selected = 0
        self.create_menu(self.items, shake(), shake_back())

    def start_game(self):
        director.director.push(FadeTransition(on_game_start(), 1))

    def quit(self):
        pyglet.app.exit()

    def options(self):
        pass

    def on_key_press(self, symbol, modifiers):
        if symbol in (key.ENTER, key.NUM_ENTER):
            self._activate_item()
            return True
        elif symbol in (key.DOWN, key.UP, key.S, key.W):
            if symbol == key.DOWN or symbol == key.S:
                new_idx = self.selected_index + 1
            elif symbol == key.UP or symbol == key.W:
                new_idx = self.selected_index - 1
            if new_idx < 0:
                new_idx = len(self.children) - 1
            elif new_idx > len(self.children) - 1:
                new_idx = 0
            self._select_item(new_idx)
            return True
        elif symbol in (key.Q, key.PERIOD, key.Z, key.Q):
            return True


# Centered background capable of handling animations #
class BackgroundLayer(cocos.layer.Layer):
    def __init__(self):
        super().__init__()
        bg = cocos.sprite.Sprite(pyglet.resource.animation('bg.gif'))
        bg.scale = 1.2 * ((windowX+windowY) / (1440+900))
        bg.position = ((windowX / 2) - (100 * (windowX/1440)), windowY/2)
        self.add(bg)


# MAIN DIRECTOR #
class Handlers(object):
    def on_key_press(symbol, modifiers):
        if symbol is key.ESCAPE:
            return True


if __name__ == '__main__':

    director.director.init(width=windowX, height=windowY, caption="PacPong",
                           fullscreen=True
                           )
    director.director.window.pop_handlers()
    keyboard = key.KeyStateHandler()
    director.director.window.push_handlers(keyboard)
    director.director.window.push_handlers(Handlers)
    scene = Scene()
    scene.add(MainMenu(), z=1)
    scene.add(BackgroundLayer(), z=0)
    director.director.run(scene)
