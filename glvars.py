import platform
from pyglet import *
from pyglet.window import key

keyboard = key.KeyStateHandler()
resource.path = ['resources']
resource.reindex()
resource.add_font('pixelated.ttf')
FN = 'Pixelated'
ballpos = (5, 0)
pl = (500, 500)
pr = (1000, 1000)
pacl = (1500, 1500)
pacr = (2000, 2000)
paclhp = 100.0
pacrhp = 100.0
ballCollidingL = False
ballCollidingR = False
paccollisionr = False
paccollisionl = False
left_points = 0
right_points = 0
addedpointL = False
addedpointR = False
ballcollr = None
ballcoll = None
powerleft = -10.0
powerright = 5.0
time = 1.0
if platform.system() == 'Windows':
    import win32api
    displayfrequency = getattr(win32api.EnumDisplaySettings(
        win32api.EnumDisplayDevices().DeviceName, -1), 'DisplayFrequency')
    windowX = win32api.GetSystemMetrics(0)
    windowY = win32api.GetSystemMetrics(1)
elif platform.system() == 'Darwin':
    import AppKit
    for screen in AppKit.NSScreen.screens():
        windowX = int(screen.frame().size.width)
        windowY = int(screen.frame().size.height)
        displayfrequency = 60

else:
    raise OSError('Your platform is not supported!')


def calculate_seconds(balldx, seconds):
    ballsmth = 60*balldx*seconds
    return abs(ballsmth)


def on_key_press(symbol, modifiers):
    if symbol is key.ESCAPE:
        return True
