import cocos, pyglet, random, cocos.collision_model as cm,\
    cocos.euclid as eu
from cocos import director
from cocos.menu import *
from cocos.scene import Scene
from cocos.actions import *
from cocos.scenes import *
from pyglet import font
from pyglet.window import key

font.add_file('resources/Splatch.ttf')
FN = 'Splatch'
windowX = 1400
windowY = 800
ballpos = (5, 0)
pl = (50, 50)
pr = (100, 100)
ballCollidingL = False
ballCollidingR = False
pointsL = 0
pointsR = 0


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
        self.position = (windowX / 2), (windowY / 2)
        self.velocity = (0, 0)
        self.cshape = cm.CircleShape(eu.Vector2(*self.position), self.width/2)
        self.dx = 3 * (windowX / 1440)
        self.dy = 3 * (windowY / 900)
        self.scale_x = 1.8 * (windowX / 1440)
        self.scale_y = self.scale_x
        self.do(MoveBall())


class GameScene(cocos.layer.ColorLayer):
    def __init__(self):
        super(GameScene, self).__init__(255, 255, 255, 255)
        self.label = cocos.text.RichLabel('PACPONG', ((windowX / 2), (windowY - 40)), font_size=30, font_name=FN,
                                          color=(0, 0, 0, 255), anchor_x='center', anchor_y='center')
        self.add(self.label)

        self.pointsl = cocos.text.RichLabel('POINTS: 0', ((50*1), (windowY - 40)), font_size = 20, font_name = FN,
                                            color = (0, 0, 0, 255), anchor_x='left', anchor_y='center')
        self.updatetext()
        self.add(self.pointsl)

        # Paddles
        self.paddleLeft = Paddle("resources/paddle.png", 100, 'left')
        self.add(self.paddleLeft, z=1)
        self.paddleRight = Paddle("resources/paddle.png", 100, 'right')
        self.add(self.paddleRight, z=1)

        # PacMan
        self.pacMan = PacMan("resources/pacman.png")
        self.add(self.pacMan, z=2)

        self.coll_manager = cm.CollisionManagerBruteForce()

    def updateobj(self, dt):
        global ballCollidingL
        global ballCollidingR
        self.pacMan.position = ballpos
        self.paddleLeft.position = pl
        self.paddleRight.position = pr
        self.pacMan.cshape.center = eu.Vector2(*self.pacMan.position)
        self.paddleLeft.cshape.center = eu.Vector2(*self.paddleLeft.position)
        self.paddleRight.cshape.center = eu.Vector2(*self.paddleRight.position)

        if self.coll_manager.they_collide(self.pacMan, self.paddleRight):
            ballCollidingR = True
            self.pacMan.x -= (self.paddleRight.width + 15)
        if self.coll_manager.they_collide(self.pacMan, self.paddleLeft):
            ballCollidingL = True
            self.pacMan.x += (self.paddleRight.width + 15)

    def updatetext(self):
        global pointsL, pointsR
        if ballpos < (1, windowY):
            pointsL += 1
            self.pointsl.element.text = 'POINTS: ' + str(pointsL)
            print(pointsL)


########################
    # Move actions #
########################
class MoveBall(cocos.actions.Move):
    def step(self, dt):
        super().step(dt)
        self.target.y = (self.target.y + self.target.dy)
        self.target.x = (self.target.x + self.target.dx)
        global ballpos, ballCollidingR, ballCollidingL
        ballpos = self.target.position

        if self.target.y > windowY - (70 * (windowY / 900)):
            self.target.y = windowY - (70 * (windowY / 900))
            self.target.dy *= -1
        if self.target.y < (70 * (windowY / 900)):
            self.target.y = (70 * (windowY / 900))
            self.target.dy *= -1

        if self.target.x > windowX+self.target.width+1251: # if dx=1, the ball can travel 139PX in 1 second/2085=5s dx=3
            self.target.position = (windowX/2, windowY/2)
            self.target.dx *= random.randrange(-1, 2, 2)
            self.target.dy *= random.randrange(-1, 2, 2)
        if self.target.x < -self.target.width-1251: # 1251=3s with dx=3
            self.target.position = (windowX/2, windowY/2)
            self.target.dx *= random.randrange(-1, 2, 2)
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
                self.target.do(MoveBy((0, 8 * (windowY / 900)), 0.01))
        if keyboard[key.S]:
            if self.target.y < (145 * (windowY / 900)):
                self.target.y = 140 * (windowY / 900)
            else:
                self.target.do(MoveBy((0, -8 * (windowY / 900)), 0.01))
        global pl
        pl = self.target.position


class MovePaddleRight(cocos.actions.Move):
    def step(self, dt):
        super().step(dt)
        if keyboard[key.UP]:
            if self.target.y > windowY - (165 * (windowY / 900)):
                self.target.y = windowY - (160 * (windowY / 900))
            else:
                self.target.do(MoveBy((0, 15 * (windowY / 900)), 0.01))
        if keyboard[key.DOWN]:
            if self.target.y < (145 * (windowY / 900)):
                self.target.y = 140 * (windowY / 900)
            else:
                self.target.do(MoveBy((0, -15 * (windowY / 900)), 0.01))
        global pr
        pr = self.target.position


def on_game_start():
    thisgamescene = Scene()
    thisgamescene.add(GameScene(), z=2, name="Game")
    thisgamescene.schedule_interval(GameScene().updateobj, 1 / 16)

    return thisgamescene


##########################
    # MAIN MENU #
##########################


class MainMenu(Menu):
    def __init__(self):
        super().__init__("PACPONG")

    # Style of menu items
        self.font_title = {'font_name': FN, 'font_size': 50, 'color': (192, 192, 192, 255), 'anchor_y': 'center',
                           'anchor_x': 'center'}
        self.font_item = {'font_name': FN, 'font_size': 30, 'anchor_y': 'center', 'anchor_x': 'center',
                          'color': (192, 192, 192, 255)}
        self.font_item_selected = {'font_name': FN, 'font_size': 50, 'anchor_y': 'center', 'anchor_x': 'center',
                                   'color': (255, 255, 255, 255)}

    # Menu items incl. functions they trigger
        items = []
        items.append(MenuItem('PLAY', self.start_game))
        items[0].y = 40
        items.append(MenuItem('QUIT', self.quit))

        self.create_menu(items, shake(), shake_back())

    def start_game(self):
        director.director.run(FadeTransition(on_game_start(), 1.0))

    def quit(self):
        pyglet.app.exit()

    def on_key_press(self, symbol, modifiers):
        if symbol is 'ESC':
            pyglet.app.exit()


# Centered background capable of handling animations #
class BackgroundLayer(cocos.layer.Layer):
    def __init__(self):
        super().__init__()
        bg = cocos.sprite.Sprite(pyglet.image.load_animation('resources/bg.gif'))
        bg.scale = 1.2 * ((windowX+windowY) / (1440+900))
        bg.position = ((windowX / 2) - (100 * (windowX/1440)), windowY / 2)
        self.add(bg)


################################
        # MAIN DIRECTOR #
################################

if __name__ == '__main__':

    director.director.init(width=windowX, height=windowY, caption="PacPong",
                           # fullscreen=True
                           )
    director.director.window.pop_handlers()
    keyboard = key.KeyStateHandler()
    director.director.window.push_handlers(keyboard)

    scene = Scene()
    scene.add(MainMenu(), z=1)
    scene.add(BackgroundLayer(), z=0)

    director.director.run(scene)
