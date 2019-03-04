import cocos, pyglet, random, cocos.collision_model as cm,\
    cocos.euclid as eu
from cocos import director
from cocos.menu import *
from cocos.scene import Scene
from cocos.actions import *
from cocos.scenes import *
from pyglet import font
from pyglet.window import key

font.add_file('resources/SIMPLICITY PERSONALUSE.ttf')
FN = 'SIMPLCITY PERSONAL USE'
windowX = 1400
windowY = 800


class Paddle(cocos.sprite.Sprite):
    def __init__(self, image, x, side):
        super().__init__(image)
        self.velocity = (0, 0)
        self.scale_y = 1.8 * (windowY / 900)
        self.scale_x = 1.2 * (windowX / 1440)
        self.cshape = cm.AARectShape(eu.Vector2(*self.position), self.width/2, self.height/2)
        if side == 'left':
            self.position = x * (windowX / 1440), (windowY / 2)
            self.do(MovePaddleLeft())
        if side == 'right':
            self.position = windowX - 100 * (windowX / 1440), (windowY / 2)
            self.do(MovePaddleRight())


class PacMan(cocos.sprite.Sprite):
    def __init__(self, image):
        super().__init__(image)
        self.position = (windowX / 2), (windowY / 2)
        self.velocity = (0, 0)
        self.cshape = cm.AARectShape(eu.Vector2(*self.position), self.width/2, self.height/2)
        self.dx = 1.6 * (windowX / 1440)
        self.dy = 1.6 * (windowY / 900)
        self.scale_x = 1.8 * (windowX / 1440)
        self.scale_y = self.scale_x
        self.do(MoveBall())


class GameScene(cocos.layer.ColorLayer):
    def __init__(self):
        super(GameScene, self).__init__(255, 255, 255, 255)
        label = cocos.text.RichLabel('PacPong', ((windowX / 2), (windowY - 20)), font_size=38, font_name=FN,
                                     color=(0, 0, 0, 255), anchor_x='center', anchor_y='center')
        self.add(label)

        # Paddles
        self.paddleLeft = Paddle("resources/paddle.png", 100, 'left')
        self.add(self.paddleLeft, z=1)
        self.paddleRight = Paddle("resources/paddle.png", 100, 'right')
        self.add(self.paddleRight, z=1)

        # PacMan
        self.pacMan = PacMan("resources/pacman.png")
        self.add(self.pacMan, z=2)

        self.coll_manager = cm.CollisionManagerBruteForce()
        self.coll_manager.add(self.pacMan)
        self.coll_manager.add(self.paddleRight)
        self.coll_manager.add(self.paddleLeft)

    def updateobj(self, dt):
        self.coll_manager.clear()
        self.pacMan.cshape.center = eu.Vector2(*self.pacMan.position)
        self.paddleLeft.cshape.center = eu.Vector2(*self.paddleLeft.position)
        self.paddleRight.cshape.center = eu.Vector2(*self.paddleRight.position)
        self.coll_manager.add(self.pacMan)
        self.coll_manager.add(self.paddleRight)
        self.coll_manager.add(self.paddleLeft)

        if self.coll_manager.they_collide(self.pacMan, self.paddleRight):
            print("colliding")


########################
    # Move actions #
########################
class MoveBall(cocos.actions.Move):
    def step(self, dt):
        super().step(dt)
        self.target.y = (self.target.y + self.target.dy)
        self.target.x = (self.target.x + self.target.dx)

        if self.target.y > windowY - (70 * (windowY / 900)):
            self.target.y = windowY - (70 * (windowY / 900))
            self.target.dy *= -1
        if self.target.y < (70 * (windowY / 900)):
            self.target.y = (70 * (windowY / 900))
            self.target.dy *= -1
        if self.target.x > windowX:
            self.target.x = (70 * (windowX / 900))
            self.target.position = (windowX/2, windowY/2)
            self.target.dx *= random.randrange(-1, 2, 2)
            self.target.dy *= random.randrange(-1, 2, 2)
        if self.target.x < 1:
            self.target.x = (70 * (windowX / 900))
            self.target.position = (windowX/2, windowY/2)
            self.target.dx *= random.randrange(-1, 2, 2)
            self.target.dy *= random.randrange(-1, 2, 2)


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


class MovePaddleRight(cocos.actions.Move):
    def step(self, dt):
        super().step(dt)
        if keyboard[key.UP]:
            if self.target.y > windowY - (165 * (windowY / 900)):
                self.target.y = windowY - (160 * (windowY / 900))
            else:
                self.target.do(MoveBy((0, 8 * (windowY / 900)), 0.01))
        if keyboard[key.DOWN]:
            if self.target.y < (145 * (windowY / 900)):
                self.target.y = 140 * (windowY / 900)
            else:
                self.target.do(MoveBy((0, -8 * (windowY / 900)), 0.01))


def on_game_start():
    thisgamescene = Scene()
    thisgamescene.add(GameScene(), z=2, name="Game")

    return thisgamescene


##########################
    # MAIN MENU #
##########################


class MainMenu(Menu):
    def __init__(self):
        super().__init__("PacPong")

    # Style of menu items
        self.font_title = {'font_name': FN, 'font_size': 100, 'color': (192, 192, 192, 255), 'anchor_y': 'center',
                           'anchor_x': 'center'}
        self.font_item = {'font_name': FN, 'font_size': 50, 'anchor_y': 'center', 'anchor_x': 'center',
                          'color': (192, 192, 192, 255)}
        self.font_item_selected = {'font_name': FN, 'font_size': 70, 'anchor_y': 'center', 'anchor_x': 'center',
                                   'color': (255, 255, 255, 255)}

    # Menu items incl. functions they trigger
        items = []
        items.append(MenuItem('Play', self.start_game))
        items[0].y = 40
        items.append(MenuItem('Quit', self.quit))

        self.create_menu(items, shake(), shake_back())

    def start_game(self):
        scene2 = Scene()
        scene2.schedule_interval(GameScene().updateobj, 1 / 60)
        scene2.add(on_game_start())
        director.director.run(FadeTransition(
            scene2, 1.0))

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
