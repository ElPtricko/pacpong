import random
from cocos import director
from cocos.menu import *
from cocos.scene import Scene
from cocos.scenes import *
from progressBar import *
from sprites import *


class GameScene(cocos.layer.ColorLayer):
    is_event_handler = True

    def __init__(self, practice=False, timer=False):
        super(GameScene, self).__init__(0, 100, 175, 255)
        global paclhp, pacrhp, powerleft, powerright, left_points, right_points
        paclhp = 100.0
        pacrhp = 100.0
        background = Bg('bg1.png')
        self.pointsl = cocos.text.Label('POINTS: 0', ((120*(windowX/1440)), 50*(windowY/900)),
                                        font_size=16*((windowX+windowY)/(1440+900)), font_name=FN,
                                        color=(0, 0, 0, 255), anchor_x='center', anchor_y='center')
        self.pointsr = cocos.text.Label('POINTS: 0', ((windowX-120*(windowX/1440)),
                                                      50*(windowY/900)),
                                        font_size=16*((windowX+windowY)/(1440+900)), font_name=FN,
                                        color=(0, 0, 0, 255), anchor_x='center', anchor_y='center')
        if practice:
            left_points = 0
            right_points = -1
            powerleft = 5.0
            powerright = -10.0
            self.pointsl.do((RotateBy(10, 0.04)+RotateBy(-20, 0.08)+
                             RotateBy(10, 0.04))*11)
            self.pointsl.do(ScaleBy(1.7, 1.1)+ScaleTo(1, 0.5))
            self.pointsl.do(MoveBy((135*(windowX/1440), 0), 0.63)+
                            MoveBy((0, 70*(windowY/900)), 0.63)+
                            MoveBy((0, -70*(windowY/900)), 0.3)+
                            MoveBy((-135*(windowX/1440), 0), 0.3))
        else:
            left_points = -1
            right_points = 0
            powerleft = -10.0
            powerright = 5.0
            self.pointsr.do((RotateBy(10, 0.04)+RotateBy(-20, 0.08)+
                             RotateBy(10, 0.04))*11)
            self.pointsr.do(ScaleBy(1.7, 1.1)+ScaleTo(1, 0.5))
            self.pointsr.do(MoveBy((-135*(windowX/1440), 0), 0.63)+
                            MoveBy((0, 70*(windowY/900)), 0.63)+
                            MoveBy((0, -70*(windowY/900)), 0.3)+
                            MoveBy((135*(windowX/1440), 0), 0.3))
        self.paddleLeft = Paddle('left')
        self.paddleRight = Paddle('right')
        self.GhostBall = GhostBall(practice)
        self.pacleft = PacBall((255, 0, 0), 'left')
        self.pacright = PacBall((200, 200, 200), 'right')
        self.coll_manager = cm.CollisionManagerBruteForce()
        self.fireball = FireBall()
        self.fireball2 = FireBall('flip')
        self.heal = Healing()
        self.heal2 = Healing()
        self.speed = SpeedUp()
        self.speed2 = SpeedUp()
        self.healthbar = HealthBar()
        self.power = PowerBar()
        self.add(background)
        self.add(self.paddleLeft)
        self.add(self.paddleRight)
        self.add(PowersIndicator())
        self.add(self.GhostBall)
        self.add(self.pointsl)
        self.add(self.pointsr)
        self.add(self.pacright)
        self.add(self.pacleft)
        self.add(self.fireball)
        self.add(self.fireball2)
        self.add(self.heal)
        self.add(self.heal2)
        self.add(self.speed)
        self.add(self.speed2)
        self.add(self.healthbar)
        self.add(self.power)
        self.pointsl.do(PointslAction())
        self.pointsr.do(PointsrAction())
        self.paddleLeft.do(MovePaddleLeft())
        self.paddleRight.do(MovePaddleRight())
        self.pacleft.do(MovePacl())
        self.GhostBall.do(MoveBall())
        self.pacright.do(MovePacr())
        if timer is True:
            self.countdownlabel = cocos.text.Label('%d S'%4, (windowX/2, windowY*9.5/11),
                                                   font_size=16*((windowX+windowY)/(1440+900)), font_name=FN,
                                                   color=(0, 0, 0, 255), anchor_x='center')
            self.countdownlabel.do(UpdateCountdown())
            self.add(self.countdownlabel)
        else:
            pass

    def updateobj(self, dt):
        global ballCollidingL, ballCollidingR, paccollisionl, paccollisionr, powerright, powerleft, paclhp, pacrhp, time
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
        if -50 < paclhp <= 0 < pacrhp:
            paclhp = -60
            director.director.push(FadeTransition(on_game_end('RIGHT'), 2))
        elif -50 < pacrhp <= 0 < paclhp:
            pacrhp = -60
            director.director.push(FadeTransition(on_game_end('LEFT'), 2))
        if -5 < time <= 0:
            if paclhp*left_points == pacrhp*right_points:
                director.director.push(FadeTransition(on_game_end('TIE'), 2))
            elif paclhp*left_points < pacrhp*right_points:
                director.director.push(FadeTransition(on_game_end('RIGHT'), 2))
            else:
                director.director.push(FadeTransition(on_game_end('LEFT'), 2))
            time = -6

    def on_key_press(self, symbol, mod):
        global powerright, powerleft, paclhp, pacrhp
        if powerleft > 20 and symbol == key.C:
            powerleft -= 20
            pacrhp -= 10
            self.fireball2.position = pacl
            self.fireball2.do(MoveBy((abs(pacl[0]+self.pacleft.width/2-pacr[0]), pacr[1]-pacl[1]), 0.4)+
                              MoveTo((-100, -100), 0))
            self.pacright.do(NoMove())
            self.pacright.do(Delay(0.3)+MoveNormal())
        if powerright > 20 and symbol == key.M:
            powerright -= 20
            paclhp -= 10
            self.fireball.position = pacr
            self.fireball.do(MoveBy(((pacl[0]+self.pacleft.width/2)-pacr[0], pacl[1]-pacr[1]), 0.4)+
                             MoveTo((-100, -100), 0))
            self.pacleft.do(NoMove())
            self.pacleft.do(Delay(0.3)+MoveNormal())
        if powerleft > 35 and symbol == key.V:
            paclhp += 20
            powerleft -= 35
            self.heal.do(MoveTo(pacl, 0)+ScaleTo(1.7, 0.2)+ScaleTo(1.2, 0.2)+ScaleTo(1.7, 0.2)
                         +ScaleTo(1.2, 0.2)+MoveTo((-100, -100), 0))
            self.pacleft.do(NoMove())
            self.pacleft.do(Delay(0.8)+MoveNormal())
        if powerright > 35 and symbol == key.N:
            pacrhp += 20
            powerright -= 35
            self.heal2.do(MoveTo(pacr, 0)+ScaleTo(1.7, 0.2)+ScaleTo(1.2, 0.2)+ScaleTo(1.7, 0.2)
                          +ScaleTo(1.2, 0.2)+MoveTo((-100, -100), 0))
            self.pacright.do(NoMove())
            self.pacright.do(Delay(0.8)+MoveNormal())
        if powerleft > 50 and symbol == key.F:
            self.speed.do(MoveTo((windowX/2+self.speed.width/2+50*((windowX+windowY)/(1440+900)), windowY/2), 0)
                          +Delay(4)+MoveTo((-1000, -1000), 0))
            self.pacright.do(InvertControls())
            self.pacright.do(Delay(4)+NoInvert())
            self.paddleRight.do(InvertControls())
            self.paddleRight.do(Delay(4)+NoInvert())
            powerleft -= 50
        if powerright > 50 and symbol == key.H:
            self.speed2.do(MoveTo((windowX/2-self.speed2.width/2-50*((windowX+windowY)/(1440+900)), windowY/2), 0)
                           +Delay(4)+MoveTo((-1000, -1000), 0))
            self.pacleft.do(InvertControls())
            self.pacleft.do(Delay(4)+NoInvert())
            self.paddleLeft.do(InvertControls())
            self.paddleLeft.do(Delay(4)+NoInvert())
            powerright -= 50

        if symbol is key.ESCAPE:
            director.director.push(FadeTransition(on_game_end(), 1))


class HealthBar(cocos.layer.ColorLayer):
    def __init__(self):
        w, h = director.director.get_window_size()
        super(HealthBar, self).__init__(100, 100, 200, 0, width=w-int(6*(w/1440)), height=int(40*(h/900)))
        self.position = (3*(w/1440), h-int(43*(h/900)))
        self.progressbar = ProgressBar(self.width//2-2, int(40*(h/900)))
        self.progressbar.position = 0, 0
        self.progressbar2 = ProgressBar(self.width//2-2, int(40*(h/900)))
        self.progressbar2.position = self.width-self.progressbar2.width, 0
        label = cocos.text.Label("HEALTH", position=(self.progressbar.position[0]+
                                                     self.progressbar.width-20*(w/1440),
                                                     self.progressbar.position[1]+self.progressbar.height/2),
                                 color=(0, 0, 0, 255), font_size=10*((w+h)/(1440+900)), font_name=FN,
                                 anchor_x='right', anchor_y='center')
        label2 = cocos.text.Label("HEALTH", position=(self.progressbar.position[0]+
                                                      self.progressbar2.width+20*(w/1440),
                                                      self.progressbar2.position[1]+self.progressbar2.height/2),
                                  color=(0, 0, 0, 255), font_size=10*((w+h)/(1440+900)), font_name=FN,
                                  anchor_x='left', anchor_y='center')
        health = cocos.text.Label("100 | 100", position=(self.progressbar.position[0]+20*(w/1440),
                                                         self.progressbar.position[1]+self.progressbar.height/2),
                                  color=(0, 0, 0, 255), font_size=10*((w+h)/(1440+900)), font_name=FN,
                                  anchor_x='left', anchor_y='center')
        health2 = cocos.text.Label("100 | 100", position=(self.progressbar2.position[0]+self.progressbar2.width-
                                                          20*(w/1440),
                                                          self.progressbar2.position[1]+self.progressbar2.height/2),
                                   color=(0, 0, 0, 255), font_size=10*((w+h)/(1440+900)), font_name=FN,
                                   anchor_x='right', anchor_y='center')

        self.add(self.progressbar)
        self.add(self.progressbar2)
        self.add(health)
        self.add(health2)
        self.add(label)
        self.add(label2)
        self.progressbar.do(UpdateHealthLeft())
        self.progressbar2.do(UpdateHealthRight())
        health.do(UpdateHealthTL())
        health2.do(UpdateHealthTR())


class PowerBar(cocos.layer.ColorLayer):
    def __init__(self):
        w, h = director.director.get_window_size()
        super(PowerBar, self).__init__(100, 100, 200, 0, width=w-int(6*(w/1440)), height=int(40*(h/900)))
        self.position = (3*(w/1440), h-int(86*(h/900)))
        self.progressbar = ProgressPowerBar(self.width//2-2, int(40*(h/900)))
        self.progressbar.position = 0, 0
        self.progressbar2 = ProgressPowerBar(self.width//2-2, int(40*(h/900)))
        self.progressbar2.position = self.width-self.progressbar2.width, 0
        label = cocos.text.Label("POWER", position=(self.progressbar.position[0]+
                                                    self.progressbar.width-20*(w/1440),
                                                    self.progressbar.position[1]+self.progressbar.height/2),
                                 color=(0, 0, 0, 255), font_size=10*((w+h)/(1440+900)), font_name=FN,
                                 anchor_x='right', anchor_y='center')
        label2 = cocos.text.Label("POWER", position=(self.progressbar.position[0]+
                                                     self.progressbar2.width+20*(w/1440),
                                                     self.progressbar2.position[1]+self.progressbar2.height/2),
                                  color=(0, 0, 0, 255), font_size=10*((w+h)/(1440+900)), font_name=FN,
                                  anchor_x='left', anchor_y='center')
        power = cocos.text.Label("0 | 100", position=(self.progressbar.position[0]+20*(w/1440),
                                                      self.progressbar.position[1]+self.progressbar.height/2),
                                 color=(0, 0, 0, 255), font_size=10*((w+h)/(1440+900)), font_name=FN,
                                 anchor_x='left', anchor_y='center')
        power2 = cocos.text.Label("0 | 100", position=(self.progressbar2.position[0]+self.progressbar2.width-
                                                       20*(w/1440),
                                                       self.progressbar2.position[1]+self.progressbar2.height/2),
                                  color=(0, 0, 0, 255), font_size=10*((w+h)/(1440+900)), font_name=FN,
                                  anchor_x='right', anchor_y='center')
        self.add(self.progressbar)
        self.add(self.progressbar2)
        self.add(power)
        self.add(power2)
        self.add(label)
        self.add(label2)
        self.progressbar.do(UpdatePowerLeft())
        self.progressbar2.do(UpdatePowerRight())
        power.do(UpdatePowerTL())
        power2.do(UpdatePowerTR())


# ACTIONS #
class NoMove(cocos.actions.Action):
    def step(self, dt):
        super().step(dt)
        self.target.stop = True


class MoveNormal(cocos.actions.Action):
    def step(self, dt):
        super().step(dt)
        self.target.stop = False


class NoInvert(cocos.actions.Action):
    def step(self, dt):
        super().step(dt)
        self.target.invert = False


class InvertControls(cocos.actions.Action):
    def step(self, dt):
        super().step(dt)
        self.target.invert = True


class UpdatePowerTR(cocos.actions.Action):
    def step(self, dt):
        super().step(dt)
        self.target.element.text = '%d | 100'%powerright


class UpdatePowerTL(cocos.actions.Action):
    def step(self, dt):
        super().step(dt)
        self.target.element.text = '%d | 100'%powerleft


class UpdateHealthTR(cocos.actions.Action):
    def step(self, dt):
        super().step(dt)
        if pacrhp < 0:
            self.target.element.text = '0 | 100'
        else:
            self.target.element.text = '%d | 100'%pacrhp


class UpdateHealthTL(cocos.actions.Action):
    def step(self, dt):
        super().step(dt)
        if paclhp < 0:
            self.target.element.text = '0 | 100'
        else:
            self.target.element.text = '%d | 100'%paclhp


class UpdatePowerRight(cocos.actions.Action):
    def step(self, dt):
        super().step(dt)
        self.target.set_progress(powerright*0.01)


class UpdatePowerLeft(cocos.actions.Action):
    def step(self, dt):
        super().step(dt)
        self.target.set_progress(powerleft*0.01)


class UpdateHealthRight(cocos.actions.Action):
    def step(self, dt):
        super().step(dt)
        if pacrhp <= 0.0:
            self.target.set_progress(0)
        else:
            self.target.set_progress(pacrhp*0.01)


class UpdateHealthLeft(cocos.actions.Action):
    def step(self, dt):
        super().step(dt)
        if paclhp <= 0.0:
            self.target.set_progress(0)
        else:
            self.target.set_progress(paclhp*0.01)


class UpdateCountdown(cocos.actions.Action):
    def step(self, dt):
        super().step(dt)
        if time < 0:
            pass
        else:
            self.target.element.text = '%.1f S'%(time*0.1)


class PointslAction(cocos.actions.Action):
    def step(self, dt):
        super().step(dt)
        global addedpointL
        self.target.element.text = 'POINTS: %d'%left_points
        if addedpointL:
            addedpointL = False
            self.target.do((RotateBy(10, 0.04)+RotateBy(-20, 0.08)+
                            RotateBy(10, 0.04))*7)
            self.target.do(ScaleBy(1.7, 0.5)+ScaleTo(1, 0.5))
            self.target.do(MoveBy((135*(windowX/1440), 0), 0.3)+
                           MoveBy((0, 70*(windowY/900)), 0.3)+
                           MoveBy((0, -70*(windowY/900)), 0.3)+
                           MoveBy((-135*(windowX/1440), 0), 0.3))


class PointsrAction(cocos.actions.Action):
    def step(self, dt):
        super().step(dt)
        global addedpointR
        self.target.element.text = 'POINTS: %d'%right_points
        if addedpointR:
            addedpointR = False
            self.target.do((RotateBy(10, 0.04)+RotateBy(-20, 0.08)+
                            RotateBy(10, 0.04))*7)
            self.target.do(ScaleBy(1.7, 0.5)+ScaleTo(1, 0.5))
            self.target.do(MoveBy((-135*(windowX/1440), 0), 0.3)+
                           MoveBy((0, 70*(windowY/900)), 0.3)+
                           MoveBy((0, -70*(windowY/900)), 0.3)+
                           MoveBy((135*(windowX/1440), 0), 0.3))


class MoveBall(cocos.actions.Move):
    def step(self, dt):
        super().step(dt)
        global ballpos, ballCollidingR, ballCollidingL, left_points, \
            right_points, addedpointR, addedpointL, paccollisionr, paccollisionl, paclhp, pacrhp, powerright, powerleft
        self.target.y = (self.target.y+self.target.dy)
        self.target.x = (self.target.x+self.target.dx)
        ballpos = self.target.position

        if self.target.y > windowY-(self.target.height/2+84*(windowY/900)):
            self.target.y = windowY-(self.target.height/2+83*(windowY/900))
            self.target.dy *= -1

        if self.target.y < (self.target.height/2+84*(windowY/900)):
            self.target.y = (self.target.height/2+83*(windowY/900))
            self.target.dy *= -1

        if -self.target.width > self.target.x > (-abs(self.target.dx))-self.target.width:
            right_points += 1
            addedpointR = True
            if powerright < 100:
                powerright += 10
            if powerleft < 10:
                powerleft = 0
            else:
                powerleft -= 10
        if windowX+self.target.width < self.target.x < abs(self.target.dx)+windowX+self.target.width:
            left_points += 1
            if powerleft < 100:
                powerleft += 10
            if powerright < 10:
                powerright = 0
            else:
                powerright -= 10
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
            self.target.x += 40*(windowX/1440)
        if ballCollidingR:
            ballCollidingR = False
            self.target.dx *= -1
            self.target.x -= 40*(windowX/1440)
        if paccollisionl:
            paclhp -= 25
            if self.target.dx < 0:
                self.target.x -= 50*(windowX/1440)
            if self.target.dx > 0:
                self.target.x += 50*(windowX/1440)
            if self.target.dy < 0:
                self.target.y -= 50*(windowY/900)
            if self.target.dy > 0:
                self.target.y += 50*(windowY/900)
            paccollisionl = False
        if paccollisionr:
            pacrhp -= 25
            if self.target.dx < 0:
                self.target.x -= 50*(windowX/1440)
            if self.target.dx > 0:
                self.target.x += 50*(windowX/1440)
            if self.target.dy < 0:
                self.target.y -= 50*(windowY/900)
            if self.target.dy > 0:
                self.target.y += 50*(windowY/900)
            paccollisionr = False


class MovePaddleLeft(cocos.actions.Move):
    def step(self, dt):
        super().step(dt)
        if self.target.invert is False:
            if keyboard[key.Q] and not keyboard[key.Z]:
                if self.target.y > windowY-(self.target.height/2+110*(windowY/900)):
                    self.target.y = windowY-(self.target.height/2+105*(windowY/900))
                else:
                    self.target.do(MoveBy((0, (15*(windowY/900))/(displayfrequency/60)), 0))
            if keyboard[key.Z] and not keyboard[key.Q]:
                if self.target.y < (self.target.height/2+90*(windowY/900)):
                    self.target.y = self.target.height/2+85*(windowY/900)
                else:
                    self.target.do(MoveBy((0, (-15*(windowY/900))/(displayfrequency/60)), 0))
        if self.target.invert is True:
            if keyboard[key.Z] and not keyboard[key.Q]:
                if self.target.y > windowY-(self.target.height/2+110*(windowY/900)):
                    self.target.y = windowY-(self.target.height/2+105*(windowY/900))
                else:
                    self.target.do(MoveBy((0, (30*(windowY/900))/(displayfrequency/60)), 0))
            if keyboard[key.Q] and not keyboard[key.Z]:
                if self.target.y < (self.target.height/2+90*(windowY/900)):
                    self.target.y = self.target.height/2+85*(windowY/900)
                else:
                    self.target.do(MoveBy((0, (-30*(windowY/900))/(displayfrequency/60)), 0))
        global pl
        pl = self.target.position


class MovePaddleRight(cocos.actions.Move):
    def step(self, dt):
        super().step(dt)
        if self.target.invert is False:
            if keyboard[key.O] and not keyboard[key.PERIOD]:
                if self.target.y > windowY-(self.target.height/2+110*(windowY/900)):
                    self.target.y = windowY-(self.target.height/2+105*(windowY/900))
                else:
                    self.target.do(MoveBy((0, (15*(windowY/900))/(displayfrequency/60)), 0))
            if keyboard[key.PERIOD] and not keyboard[key.O]:
                if self.target.y < (self.target.height/2+90*(windowY/900)):
                    self.target.y = self.target.height/2+85*(windowY/900)
                else:
                    self.target.do(MoveBy((0, (-15*(windowY/900))/(displayfrequency/60)), 0))
        if self.target.invert is True:
            if keyboard[key.PERIOD] and not keyboard[key.O]:
                if self.target.y > windowY-(self.target.height/2+110*(windowY/900)):
                    self.target.y = windowY-(self.target.height/2+105*(windowY/900))
                else:
                    self.target.do(MoveBy((0, (30*(windowY/900))/(displayfrequency/60)), 0))
            if keyboard[key.O] and not keyboard[key.PERIOD]:
                if self.target.y < (self.target.height/2+90*(windowY/900)):
                    self.target.y = self.target.height/2+85*(windowY/900)
                else:
                    self.target.do(MoveBy((0, (-30*(windowY/900))/(displayfrequency/60)), 0))
        global pr
        pr = self.target.position


class MovePacl(cocos.actions.Move):
    def step(self, dt):
        super().step(dt)
        if self.target.invert is False and self.target.stop is False:
            if keyboard[key.W] and not keyboard[key.S]:
                if self.target.y >= windowY-(200*(windowY/900)):
                    self.target.y = windowY-(200*(windowY/900))
                else:
                    self.target.do(MoveBy((0, (10*(windowY/900))/(displayfrequency/60)), 0))
            if keyboard[key.S] and not keyboard[key.W]:
                if self.target.y <= (200*(windowY/900)):
                    self.target.y = 200*(windowY/900)
                else:
                    self.target.do(MoveBy((0, (-10*(windowY/900))/(displayfrequency/60)), 0))
            if keyboard[key.D] and not keyboard[key.A]:
                if self.target.x >= windowX/2-(70*windowX/1440):
                    self.target.x = windowX/2-(70*windowX/1440)
                else:
                    self.target.do(MoveBy(((10*(windowX/1440))/(displayfrequency/60), 0), 0))
                if keyboard[key.W]:
                    if self.target.y >= windowY-(200*(windowY/900)):
                        self.target.y = windowY-(200*(windowY/900))
                    elif self.target.x >= windowX/2-(70*windowX/1440):
                        self.target.x = windowX/2-(70*windowX/1440)
                    else:
                        self.target.do(MoveBy((((((10**2)/2)**0.5)*(windowY/900))/(displayfrequency/60),
                                               ((((10**2)/2)**0.5)*(windowY/900))/(displayfrequency/60)),
                                              0))
                elif keyboard[key.S]:
                    if self.target.y <= (200*(windowY/900)):
                        self.target.y = 200*(windowY/900)
                    elif self.target.x >= windowX/2-(70*windowX/1440):
                        self.target.x = windowX/2-(70*windowX/1440)
                    else:
                        self.target.do(MoveBy((((((10**2)/2)**0.5)*(windowY/900))/(displayfrequency/60),
                                               (-(((10**2)/2)**0.5)*(windowY/900))/(displayfrequency/60)),
                                              0))
            if keyboard[key.A] and not keyboard[key.D]:
                if self.target.x <= 200*(windowX/1440):
                    self.target.x = 200*(windowX/1440)
                else:
                    self.target.do(MoveBy(((-10*(windowX/1440))/(displayfrequency/60), 0), 0))
                if keyboard[key.W]:
                    if self.target.y >= windowY-(200*(windowY/900)):
                        self.target.y = windowY-(200*(windowY/900))
                    elif self.target.x <= 200*(windowX/1440):
                        self.target.x = 200*(windowX/1440)
                    else:
                        self.target.do(MoveBy(((-(((10**2)/2)**0.5)*(windowY/900))/(displayfrequency/60),
                                               ((((10**2)/2)**0.5)*(windowY/900))/(displayfrequency/60)),
                                              0))
                elif keyboard[key.S]:
                    if self.target.y <= (200*(windowY/900)):
                        self.target.y = 200*(windowY/900)
                    elif self.target.x <= 200*(windowX/1440):
                        self.target.x = 200*(windowX/1440)
                    else:
                        self.target.do(MoveBy(((-(((10**2)/2)**0.5)*(windowY/900))/(displayfrequency/60),
                                               (-(((10**2)/2)**0.5)*(windowY/900))/(displayfrequency/60)),
                                              0))
        if self.target.invert is True and self.target.stop is False:
            if keyboard[key.S] and not keyboard[key.W]:
                if self.target.y >= windowY-(200*(windowY/900)):
                    self.target.y = windowY-(200*(windowY/900))
                else:
                    self.target.do(MoveBy((0, (10*(windowY/900))/(displayfrequency/60)*2), 0))
            if keyboard[key.W] and not keyboard[key.S]:
                if self.target.y <= (200*(windowY/900)):
                    self.target.y = 200*(windowY/900)
                else:
                    self.target.do(MoveBy((0, (-10*(windowY/900))/(displayfrequency/60)*2), 0))
            if keyboard[key.A] and not keyboard[key.D]:
                if self.target.x >= windowX/2-(70*windowX/1440):
                    self.target.x = windowX/2-(70*windowX/1440)
                else:
                    self.target.do(MoveBy(((10*(windowX/1440))/(displayfrequency/60)*2, 0), 0))
                if keyboard[key.S]:
                    if self.target.y >= windowY-(200*(windowY/900)):
                        self.target.y = windowY-(200*(windowY/900))
                    elif self.target.x >= windowX/2-(70*windowX/1440):
                        self.target.x = windowX/2-(70*windowX/1440)
                    else:
                        self.target.do(
                            MoveBy((((((10**2)/2)**0.5)*(windowY/900))/(displayfrequency/60)*2,
                                    ((((10**2)/2)**0.5)*(windowY/900))/(displayfrequency/60)*2), 0))
                elif keyboard[key.W]:
                    if self.target.y <= (200*(windowY/900)):
                        self.target.y = 200*(windowY/900)
                    elif self.target.x >= windowX/2-(70*windowX/1440):
                        self.target.x = windowX/2-(70*windowX/1440)
                    else:
                        self.target.do(
                            MoveBy((((((10**2)/2)**0.5)*(windowY/900))/(displayfrequency/60)*2,
                                    (-(((10**2)/2)**0.5)*(windowY/900))/(displayfrequency/60)*2), 0))
            if keyboard[key.D] and not keyboard[key.A]:
                if self.target.x <= 200*(windowX/1440):
                    self.target.x = 200*(windowX/1440)
                else:
                    self.target.do(MoveBy(((-10*(windowX/1440))/(displayfrequency/60)*2, 0), 0))
                if keyboard[key.S]:
                    if self.target.y >= windowY-(200*(windowY/900)):
                        self.target.y = windowY-(200*(windowY/900))
                    elif self.target.x <= 200*(windowX/1440):
                        self.target.x = 200*(windowX/1440)
                    else:
                        self.target.do(
                            MoveBy(((-(((10**2)/2)**0.5)*(windowY/900))/(displayfrequency/60)*2,
                                    ((((10**2)/2)**0.5)*(windowY/900))/(displayfrequency/60)*2), 0))
                elif keyboard[key.W]:
                    if self.target.y <= (200*(windowY/900)):
                        self.target.y = 200*(windowY/900)
                    elif self.target.x <= 200*(windowX/1440):
                        self.target.x = 200*(windowX/1440)
                    else:
                        self.target.do(
                            MoveBy(((-(((10**2)/2)**0.5)*(windowY/900))/(displayfrequency/60)*2,
                                    (-(((10**2)/2)**0.5)*(windowY/900))/(displayfrequency/60)*2), 0))
        else:
            pass
        global pacl
        pacl = self.target.position


class MovePacr(cocos.actions.Move):
    def step(self, dt):
        super().step(dt)
        if self.target.invert is False and self.target.stop is False:
            if keyboard[key.I] and not keyboard[key.K]:
                if self.target.y >= windowY-(200*(windowY/900)):
                    self.target.y = windowY-(200*(windowY/900))
                else:
                    self.target.do(MoveBy((0, (10*(windowY/900))/(displayfrequency/60)), 0))
            if keyboard[key.K] and not keyboard[key.I]:
                if self.target.y <= (200*(windowY/900)):
                    self.target.y = 200*(windowY/900)
                else:
                    self.target.do(MoveBy((0, (-10*(windowY/900))/(displayfrequency/60)), 0))
            if keyboard[key.L] and not keyboard[key.J]:
                if self.target.x >= windowX-200*(windowX/1440):
                    self.target.x = windowX-200*(windowX/1440)
                else:
                    self.target.do(MoveBy(((10*(windowX/1440))/(displayfrequency/60), 0), 0))
                if keyboard[key.I]:
                    if self.target.y >= windowY-(200*(windowY/900)):
                        self.target.y = windowY-(200*(windowY/900))
                    elif self.target.x >= windowX-200*(windowX/1440):
                        self.target.x = windowX-200*(windowX/1440)
                    else:
                        self.target.do(MoveBy((((((10**2)/2)**0.5)*(windowY/900))/(displayfrequency/60),
                                               ((((10**2)/2)**0.5)*(windowY/900))/(displayfrequency/60)),
                                              0))
                elif keyboard[key.K]:
                    if self.target.y <= (200*(windowY/900)):
                        self.target.y = 200*(windowY/900)
                    elif self.target.x >= windowX-200*(windowX/1440):
                        self.target.x = windowX-200*(windowX/1440)
                    else:
                        self.target.do(MoveBy((((((10**2)/2)**0.5)*(windowY/900))/(displayfrequency/60),
                                               (-(((10**2)/2)**0.5)*(windowY/900))/(displayfrequency/60)),
                                              0))
            if keyboard[key.J] and not keyboard[key.L]:
                if self.target.x <= windowX/2+(70*windowX/1440):
                    self.target.x = windowX/2+(70*windowX/1440)
                else:
                    self.target.do(MoveBy(((-10*(windowX/1440))/(displayfrequency/60), 0), 0))
                if keyboard[key.I]:
                    if self.target.y >= windowY-(200*(windowY/900)):
                        self.target.y = windowY-(200*(windowY/900))
                    elif self.target.x <= windowX/2+(70*windowX/1440):
                        self.target.x = windowX/2+(70*windowX/1440)
                    else:
                        self.target.do(MoveBy(((-(((10**2)/2)**0.5)*(windowY/900))/(displayfrequency/60),
                                               ((((10**2)/2)**0.5)*(windowY/900))/(displayfrequency/60)),
                                              0))
                elif keyboard[key.K]:
                    if self.target.y <= (200*(windowY/900)):
                        self.target.y = 200*(windowY/900)
                    elif self.target.x <= windowX/2+(70*windowX/1440):
                        self.target.x = windowX/2+(70*windowX/1440)
                    else:
                        self.target.do(MoveBy(((-(((10**2)/2)**0.5)*(windowY/900))/(displayfrequency/60),
                                               (-(((10**2)/2)**0.5)*(windowY/900))/(displayfrequency/60)),
                                              0))
        if self.target.invert is True and self.target.stop is False:
            if keyboard[key.K] and not keyboard[key.I]:
                if self.target.y >= windowY-(200*(windowY/900)):
                    self.target.y = windowY-(200*(windowY/900))
                else:
                    self.target.do(MoveBy((0, (10*(windowY/900))/(displayfrequency/60)*2), 0))
            if keyboard[key.I] and not keyboard[key.K]:
                if self.target.y <= (200*(windowY/900)):
                    self.target.y = 200*(windowY/900)
                else:
                    self.target.do(MoveBy((0, (-10*(windowY/900))/(displayfrequency/60)*2), 0))
            if keyboard[key.J] and not keyboard[key.L]:
                if self.target.x >= windowX-200*(windowX/1440):
                    self.target.x = windowX-200*(windowX/1440)
                else:
                    self.target.do(MoveBy(((10*(windowX/1440))/(displayfrequency/60)*2, 0), 0))
                if keyboard[key.K]:
                    if self.target.y >= windowY-(200*(windowY/900)):
                        self.target.y = windowY-(200*(windowY/900))
                    elif self.target.x >= windowX-200*(windowX/1440):
                        self.target.x = windowX-200*(windowX/1440)
                    else:
                        self.target.do(
                            MoveBy((((((10**2)/2)**0.5)*(windowY/900))/(displayfrequency/60)*2,
                                    ((((10**2)/2)**0.5)*(windowY/900))/(displayfrequency/60)*2), 0))
                elif keyboard[key.I]:
                    if self.target.y <= (200*(windowY/900)):
                        self.target.y = 200*(windowY/900)
                    elif self.target.x >= windowX-200*(windowX/1440):
                        self.target.x = windowX-200*(windowX/1440)
                    else:
                        self.target.do(
                            MoveBy((((((10**2)/2)**0.5)*(windowY/900))/(displayfrequency/60)*2,
                                    (-(((10**2)/2)**0.5)*(windowY/900))/(displayfrequency/60)*2), 0))
            if keyboard[key.L] and not keyboard[key.J]:
                if self.target.x <= windowX/2+(70*windowX/1440):
                    self.target.x = windowX/2+(70*windowX/1440)
                else:
                    self.target.do(MoveBy(((-10*(windowX/1440))/(displayfrequency/60)*2, 0), 0))
                if keyboard[key.K]:
                    if self.target.y >= windowY-(200*(windowY/900)):
                        self.target.y = windowY-(200*(windowY/900))
                    elif self.target.x <= windowX/2+(70*windowX/1440):
                        self.target.x = windowX/2+(70*windowX/1440)
                    else:
                        self.target.do(
                            MoveBy(((-(((10**2)/2)**0.5)*(windowY/900))/(displayfrequency/60)*2,
                                    ((((10**2)/2)**0.5)*(windowY/900))/(displayfrequency/60)*2), 0))
                elif keyboard[key.I]:
                    if self.target.y <= (200*(windowY/900)):
                        self.target.y = 200*(windowY/900)
                    elif self.target.x <= windowX/2+(70*windowX/1440):
                        self.target.x = windowX/2+(70*windowX/1440)
                    else:
                        self.target.do(
                            MoveBy(((-(((10**2)/2)**0.5)*(windowY/900))/(displayfrequency/60)*2,
                                    (-(((10**2)/2)**0.5)*(windowY/900))/(displayfrequency/60)*2), 0))
        else:
            pass
        global pacr
        pacr = self.target.position


# MAIN MENU #
class MainMenu(Menu):
    def __init__(self):
        super().__init__("PACPONG")
        self.font_title = {'font_name': FN, 'font_size': 30*((windowX+windowY)/(1440+900)),
                           'color': (192, 192, 192, 255), 'anchor_y': 'center', 'anchor_x': 'center'}
        self.font_item = {'font_name': FN, 'font_size': 20*((windowX+windowY)/(1440+900)),
                          'anchor_y': 'center', 'anchor_x': 'center', 'color': (192, 192, 192, 255)}
        self.font_item_selected = {'font_name': FN, 'font_size': 25*((windowX+windowY)/(1440+900)),
                                   'anchor_y': 'center', 'anchor_x': 'center', 'color': (255, 255, 255, 255)}
        self.items = []
        self.items.append(MenuItem('COUNTDOWN MODE', countdown_mode_start))
        self.items.append(MenuItem('INFINITE MODE', infinite_mode_start))
        self.items.append(MenuItem('PRACTICE MODE', practice_mode_start))
        self.items.append(MenuItem('QUIT', self.quit))
        self.selected = 0
        self.items[0].y = 30
        self.items[1].y = 20
        self.items[2].y = 10
        self.create_menu(self.items, shake())

    @staticmethod
    def quit():
        pyglet.app.exit()

    def on_key_press(self, symbol, modifiers):
        if symbol in (key.ENTER, key.NUM_ENTER):
            self._activate_item()
            return True
        elif symbol in (key.DOWN, key.UP):
            if symbol == key.DOWN:
                new_idx = self.selected_index+1
            elif symbol == key.UP:
                new_idx = self.selected_index-1
            if new_idx < 0:
                new_idx = len(self.children)-1
            elif new_idx > len(self.children)-1:
                new_idx = 0
            self._select_item(new_idx)
            return True
        elif symbol in (key.Q, key.PERIOD, key.Z, key.O, key.W, key.S, key.A, key.D, key.J, key.K, key.L, key.I):
            return True


class BackgroundLayer(cocos.layer.Layer):
    def __init__(self, winner=None):
        super().__init__()
        credits1 = cocos.text.Label('CREATOR   -   PATRICK RAVNHOLT',
                                    (windowX-(50*windowX/1440), 80*(windowY/900)),
                                    font_name=FN, color=(150, 150, 150, 255),
                                    font_size=11*((windowX+windowY)/(1440+900)), anchor_x='right',
                                    anchor_y='bottom')
        credits2 = cocos.text.Label('DESIGNER   -   ADRI EVANS',
                                    (windowX-(50*windowX/1440), 40*(windowY/900)),
                                    font_name=FN, color=(150, 150, 150, 255),
                                    font_size=11*((windowX+windowY)/(1440+900)), anchor_x='right',
                                    anchor_y='bottom')
        credits3 = cocos.text.Label('BAUTISTA CAZEAUX  -  CONCEPT & MARKETING',
                                    ((50*windowX/1440), 80*(windowY/900)),
                                    font_name=FN, color=(150, 150, 150, 255),
                                    font_size=11*((windowX+windowY)/(1440+900)), anchor_x='left',
                                    anchor_y='bottom')
        credits4 = cocos.text.Label('PABLO PAZOS  -  MARKETING', ((50*windowX/1440), 40*(windowY/900)),
                                    font_name=FN,
                                    color=(150, 150, 150, 255), font_size=11*((windowX+windowY)/(1440+900)),
                                    anchor_x='left', anchor_y='bottom')
        self.add(Bg('bg1.png'))
        self.add(cocos.layer.ColorLayer(0, 0, 0, 150, windowX, windowY))
        self.add(credits1)
        self.add(credits2)
        self.add(credits3)
        self.add(credits4)
        if winner is None:
            pass
        elif 'LEFT' in winner:
            win = cocos.text.Label('WINNER', (windowX*1.3/8, windowY*4/6), font_name=FN,
                                   color=(0, 200, 30, 255),
                                   font_size=50*((windowX+windowY)/(1440+900)), anchor_x='center',
                                   anchor_y='center')
            lose = cocos.text.Label('LOSER', (windowX*6.7/8, windowY*4/6), font_name=FN,
                                    color=(200, 0, 10, 255),
                                    font_size=50*((windowX+windowY)/(1440+900)), anchor_x='center',
                                    anchor_y='center')
            lose.rotation = 20
            win.rotation = -20
            self.add(win)
            self.add(lose)
        elif 'RIGHT' in winner:
            win = cocos.text.Label('WINNER', (windowX*6.7/8, windowY*4/6), font_name=FN,
                                   color=(0, 200, 30, 255),
                                   font_size=50*((windowX+windowY)/(1440+900)), anchor_x='center',
                                   anchor_y='center')
            lose = cocos.text.Label('LOSER', (windowX*1.3/8, windowY*4/6), font_name=FN,
                                    color=(200, 0, 10, 255),
                                    font_size=50*((windowX+windowY)/(1440+900)), anchor_x='center',
                                    anchor_y='center')
            lose.rotation = -20
            win.rotation = 20
            self.add(win)
            self.add(lose)
        elif 'TIE' in winner:
            win = cocos.text.Label('TIED', (windowX*1.3/8, windowY*4/6), font_name=FN, color=(200, 200, 0, 255),
                                   font_size=50*((windowX+windowY)/(1440+900)), anchor_x='center',
                                   anchor_y='center')
            lose = cocos.text.Label('TIED', (windowX*6.7/8, windowY*4/6), font_name=FN,
                                    color=(200, 200, 0, 255),
                                    font_size=50*((windowX+windowY)/(1440+900)), anchor_x='center',
                                    anchor_y='center')
            lose.rotation = 20
            win.rotation = -20
            self.add(win)
            self.add(lose)


def practice_mode_start():
    practice = Scene()
    practice.add(GameScene(True, False))
    practice.schedule_interval(GameScene(True, False).updateobj, (1/60)/(displayfrequency/144)*1.55)
    practice.schedule_interval(update_powerbar, 1/20)
    practice.schedule_interval(practice_mode, 1/20)
    director.director.push(MoveInLTransition(practice, 1))


def countdown_mode_start():
    global time
    time = 1800
    countdown = Scene()
    countdown.add(GameScene(False, True))
    countdown.schedule_interval(GameScene(False, True).updateobj, (1/60)/(displayfrequency/144)*1.55)
    countdown.schedule_interval(update_powerbar, 1/20)
    countdown.schedule_interval(countdown_mode, 1/10)
    director.director.push(MoveInTTransition(countdown, 1))


def infinite_mode_start():
    infinite = Scene()
    infinite.add(GameScene(False, False))
    infinite.schedule_interval(GameScene(False, False).updateobj, (1/60)/(displayfrequency/144)*1.55)
    infinite.schedule_interval(update_powerbar, 1/20)
    director.director.push(MoveInRTransition(infinite, 1))


def on_game_end(winner=None):
    endscene = Scene()
    endscene.add(MainMenu(), z=-2, name="MENU")
    endscene.add(BackgroundLayer(winner), z=-3, name="BG")
    return endscene


def update_powerbar(dt):
    global powerright, powerleft
    if 0 <= powerright < 100:
        powerright += 0.05
    elif powerright >= 100:
        powerright = 100
    if 0 <= powerleft < 100:
        powerleft += 0.05
    elif powerleft >= 100:
        powerleft = 100


def practice_mode(dt):
    global powerright, powerleft, paclhp, pacrhp
    if paclhp < 100:
        if paclhp < 50:
            paclhp += 20
        paclhp += 1
    if pacrhp < 100:
        if pacrhp < 50:
            pacrhp += 20
        pacrhp += 1
    if powerright < 100:
        powerright += 4
    if powerleft < 100:
        powerleft += 4


def countdown_mode(dt):
    global time
    time -= 1
