import cocos
import pyglet
from cocos import director
from cocos.menu import *
from cocos.scene import Scene
from cocos.actions import *
from cocos.scenes import *
from pyglet import font
from pyglet.window import key

font.add_file('resources/SIMPLICITY PERSONALUSE.ttf')
FN = 'SIMPLCITY PERSONAL USE'
windowX = 1000
windowY = 700


class GameScene(cocos.layer.ColorLayer):

    def __init__(self):
        super(GameScene, self).__init__(255, 255, 255, 255)

        label = cocos.text.RichLabel('PacPong', ((windowX / 2), (windowY - 20)), font_size=38, font_name=FN,
                                     color=(0, 0, 0, 255), anchor_x='center', anchor_y='center')
        self.add(label)

        # Paddles
        self.paddleLeft = cocos.sprite.Sprite('resources/paddle.png')
        self.paddleLeft.position = 100 * (windowX / 1440), (windowY / 2)
        self.paddleLeft.velocity = (0, 0)
        self.add(self.paddleLeft, z=1)

        self.paddleRight = cocos.sprite.Sprite('resources/paddle.png')
        self.paddleRight.position = (windowX - 100 * (windowX / 1440)), (windowY / 2)
        self.paddleRight.velocity = (0, 0)
        self.add(self.paddleRight, z=1)

        # PacMan
        self.pacMan = cocos.sprite.Sprite('resources/pacman.png')
        self.pacMan.position = (windowX / 2), (windowY / 2)
        self.add(self.pacMan, z=2)

        # Object scales
        self.paddleLeft.scale_y = 1.8 * (windowY / 900)
        self.paddleRight.scale_y = 1.8 * (windowY / 900)
        self.pacMan.scale_x = 1.8 * (windowX / 1440)
        self.paddleLeft.scale_x = 1.2 * (windowX / 1440)
        self.paddleRight.scale_x = 1.2 * (windowX / 1440)
        self.pacMan.scale_y = self.pacMan.scale_x # Same as ScaleX so that the pacman isn't streched
        # PACMAN DO CUSTOM MOVE CLASS

        self.paddleRight.do(MovePaddleRight())
        self.paddleLeft.do(MovePaddleLeft())

    # Move the ball
    def move_ball(self):
        self.pacMan.do(MoveBy((10, 10), 0.1))
        if self.pacMan.y > windowY-110:
            self.pacMan.do(MoveBy((10, 10)*-1, 0.1))


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
        director.director.run(FadeTransition(
            on_game_start(), 1.0))

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
