from Game import *
from glvars import *

if __name__ == '__main__':
    director.director.init(width=windowX, height=windowY, caption="PacPong",
                           fullscreen=True
                           )
    director.director.window.pop_handlers()
    director.director.window.push_handlers(keyboard)
    director.director.window.push_handlers(on_key_press)
    scene = Scene()
    scene.add(MainMenu(), z=1)
    scene.add(BackgroundLayer(), z=0)
    director.director.run(scene)
