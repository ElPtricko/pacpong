import cocos, pyglet, random, cocos.collision_model as cm,\
    cocos.euclid as eu
from cocos import director
from cocos.menu import *
from cocos.scene import Scene
from cocos.actions import *
from cocos.scenes import *
from pyglet.window import key
from glvars import *


class Paddle(cocos.sprite.Sprite):
    def __init__(self, image, x, side):
        super().__init__(image)
        self.velocity = (0, 0)
        self.scale_y = 1.8 * (windowY / 900)
        self.scale_x = 0.8 * (windowX / 1440)
        if side == 'left':
            self.position = x * (windowX / 1440), (windowY / 2)
            self.do(MovePaddleLeft())
        if side == 'right':
            self.position = windowX - 100 * (windowX / 1440), (windowY / 2)
            self.do(MovePaddleRight())
        self.cshape = cm.AARectShape(eu.Vector2(*self.position), self.width/2, self.height/2)


class PacMan(cocos.sprite.Sprite):
    def __init__(self, image):
        super().__init__(image)
        self.velocity = (0, 0)
        self.color = (255, 255, 0)
        self.scale_x = 0.6 * (windowX/1440)
        self.scale_y = self.scale_x
        self.dx = (14.4 * (windowX/1440)) / (displayfrequency/60)
        self.dy = (14.4 * (windowY/900)) / (displayfrequency/60)
        self.position = (windowX - 500 * (windowX/1440)), (windowY/2)
        self.cshape = cm.CircleShape(eu.Vector2(*self.position), self.width/2)
        self.do(MoveBall())
        self.do(Repeat(RotateBy(15, 0.05) + RotateBy(-30, 0.1) + RotateBy(15, 0.05)))


class GameScene(cocos.layer.ColorLayer):
    def __init__(self):
        super(GameScene, self).__init__(70, 100, 175, 255)
        hits = cocos.text.RichLabel('TOTAL HITS: 0', ((windowX / 2), (windowY - 40)),
                                    font_size=16*((windowX+windowY) / (1440+900)), font_name=FN, color=(0, 0, 0, 255),
                                    anchor_x='center', anchor_y='center')
        hits.do(BallCollisions())
        self.add(hits)

        self.pointsl = cocos.text.Label('POINTS: 0', ((120*(windowX/1440)), (windowY - 40)),
                                        font_size=16*((windowX+windowY) / (1440+900)), font_name=FN,
                                        color=(0, 0, 0, 255), anchor_x='center', anchor_y='center')
        self.pointsl.do(PointslAction())
        self.add(self.pointsl)

        self.pointsr = cocos.text.Label('POINTS: 0', ((windowX-120*(windowX/1440)), (windowY - 40)),
                                        font_size=16*((windowX+windowY) / (1440+900)), font_name=FN,
                                        color=(0, 0, 0, 255), anchor_x='center', anchor_y='center')
        self.pointsr.do((RotateBy(10, 0.04) + RotateBy(-20, 0.08) +
                        RotateBy(10, 0.04)) * 11)
        self.pointsr.do(ScaleBy(1.7, 1.1) + ScaleTo(1, 0.5))
        self.pointsr.do(MoveBy((-135 * (windowX / 1440), 0), 0.63) +
                        MoveBy((0, -70 * (windowY / 900)), 0.63) +
                        MoveBy((0, 70 * (windowY / 900)), 0.3) +
                        MoveBy((135 * (windowX / 1440), 0), 0.3))
        self.pointsr.do(PointsrAction())
        self.add(self.pointsr)

        # Paddles
        self.paddleLeft = Paddle("resources/paddle.png", 100, 'left')
        self.add(self.paddleLeft, z=1)
        self.paddleRight = Paddle("resources/paddle.png", 100, 'right')
        self.add(self.paddleRight, z=1)

        # PacMan
        self.pacMan = PacMan("resources/ghost.png")
        self.add(self.pacMan)

        self.coll_manager = cm.CollisionManagerBruteForce()

    def updateobj(self, dt):
        global ballCollidingL, ballCollidingR
        self.pacMan.position = ballpos
        self.paddleLeft.position = pl
        self.paddleRight.position = pr
        self.pacMan.cshape.center = eu.Vector2(*self.pacMan.position)
        self.paddleLeft.cshape.center = eu.Vector2(*self.paddleLeft.position)
        self.paddleRight.cshape.center = eu.Vector2(*self.paddleRight.position)
        if self.coll_manager.they_collide(self.pacMan, self.paddleRight):
            ballCollidingR = True
            self.pacMan.x -= self.paddleRight.width + self.pacMan.dx + 50
        if self.coll_manager.they_collide(self.pacMan, self.paddleLeft):
            ballCollidingL = True
            self.pacMan.x += self.paddleRight.width + self.pacMan.dx + 50


########################
    # Move actions #
########################
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
                           MoveBy((0, -70 * (windowY / 900)), 0.3) +
                           MoveBy((0, 70 * (windowY / 900)), 0.3) +
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
                           MoveBy((0, -70 * (windowY / 900)), 0.3) +
                           MoveBy((0, 70 * (windowY / 900)), 0.3) +
                           MoveBy((135 * (windowX / 1440), 0), 0.3))


class BallCollisions(cocos.actions.Action):
    def step(self, dt):
        super().step(dt)
        newhits = int(self.target.element.text.split()[2]) + 1
        if ballCollidingR or ballCollidingL:
            self.target.element.text = 'TOTAL HITS: %d' % newhits


class MoveBall(cocos.actions.Move):
    def step(self, dt):
        super().step(dt)
        global ballpos, ballCollidingR, ballCollidingL, left_points, \
            right_points, addedpointR, addedpointL
        self.target.y = (self.target.y + self.target.dy)
        self.target.x = (self.target.x + self.target.dx)
        ballpos = self.target.position

        if self.target.y > windowY - (70 * (windowY / 900)):
            self.target.y = windowY - (70 * (windowY / 900))
            self.target.dy *= -1
        if self.target.y < (70 * (windowY / 900)):
            self.target.y = (70 * (windowY / 900))
            self.target.dy *= -1

        if -self.target.width > self.target.x > (-abs(self.target.dx))-self.target.width:
            right_points += 1
            addedpointR = True
        if windowX+self.target.width < self.target.x < abs(self.target.dx)+windowX+self.target.width:
            left_points += 1
            addedpointL = True

        if self.target.x > windowX+self.target.width+(1251*(windowX/1440)): # if dx=1, the ball can travel
            self.target.position = (windowX/2, windowY/2)                   # 139PX in 1 second/2085=5s dx=3
            self.target.dx *= -1
            self.target.dy *= random.randrange(-1, 2, 2)
        if self.target.x < -self.target.width-(1251*(windowX/1440)): # 1251=3s with dx=3
            self.target.position = (windowX/2, windowY/2)
            self.target.dx *= -1
            self.target.dy *= random.randrange(-1, 2, 2)

        if ballCollidingL:
            ballCollidingL = False
            self.target.dx *= -1
            self.target.x += 30
        if ballCollidingR:
            ballCollidingR = False
            self.target.dx *= -1
            self.target.x -= 30


class MovePaddleLeft(cocos.actions.Move):
    def step(self, dt):
        super().step(dt)
        if keyboard[key.W]:
            if self.target.y > windowY - (165 * (windowY / 900)):
                self.target.y = windowY - (160 * (windowY / 900))
            else:
                self.target.do(MoveBy((0, (15 * (windowY / 900)) / (displayfrequency/60)),
                                      0.01 / (displayfrequency/60)))
        if keyboard[key.S]:
            if self.target.y < (145 * (windowY / 900)):
                self.target.y = 140 * (windowY / 900)
            else:
                self.target.do(MoveBy((0, (-15 * (windowY / 900)) / (displayfrequency/60)),
                                      0.01 / (displayfrequency/60)))
        global pl
        pl = self.target.position


class MovePaddleRight(cocos.actions.Move):
    def step(self, dt):
        super().step(dt)
        if keyboard[key.UP]:
            if self.target.y > windowY - (165 * (windowY / 900)):
                self.target.y = windowY - (160 * (windowY / 900))
            else:
                self.target.do(MoveBy((0, (15 * (windowY / 900)) / (displayfrequency/60)),
                                      0.01 / (displayfrequency/60)))
        if keyboard[key.DOWN]:
            if self.target.y < (145 * (windowY / 900)):
                self.target.y = 140 * (windowY / 900)
            else:
                self.target.do(MoveBy((0, (-15 * (windowY / 900)) / (displayfrequency/60)),
                                      0.01 / (displayfrequency/60)))
        global pr
        pr = self.target.position


# Used for starting the game
def on_game_start():
    thisgamescene = Scene()
    thisgamescene.add(GameScene(), z=2, name="Game")
    thisgamescene.schedule_interval(GameScene().updateobj, (1/60)/(displayfrequency/144) * 1.1)
    return thisgamescene


##########################
    # MAIN MENU #
##########################
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
        director.director.run(FadeTransition(on_game_start(), 1))

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


# Centered background capable of handling animations #
class BackgroundLayer(cocos.layer.Layer):
    def __init__(self):
        super().__init__()
        bg = cocos.sprite.Sprite(pyglet.image.load_animation('resources/bg.gif'))
        bg.scale = 1.2 * ((windowX+windowY) / (1440+900))
        bg.position = ((windowX / 2) - (100 * (windowX/1440)), windowY/2)
        self.add(bg)


################################
        # MAIN DIRECTOR #
################################
class Handlers(object):
    def on_key_press(symbol, modifiers):
        if symbol is key.ESCAPE:
            return True


if __name__ == '__main__':

    director.director.init(width=windowX, height=windowY, caption="PacPong",
                           # fullscreen=True
                           )
    director.director.window.pop_handlers()
    keyboard = key.KeyStateHandler()
    director.director.window.push_handlers(keyboard)
    director.director.window.push_handlers(Handlers)
    scene = Scene()
    scene.add(MainMenu(), z=1)
    scene.add(BackgroundLayer(), z=0)
    director.director.run(scene)
