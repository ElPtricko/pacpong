import win32api
from pyglet import font

font.add_file('resources/Splatch.ttf')
FN = 'Splatch'
windowX = win32api.GetSystemMetrics(0)
windowY = win32api.GetSystemMetrics(1)
ballpos = (5, 0)
pl = (500, 500)
pr = (1000, 1000)
ballCollidingL = False
ballCollidingR = False
left_points = -1
right_points = 0
addedpointL = False
addedpointR = False
displayfrequency = getattr(win32api.EnumDisplaySettings(
    win32api.EnumDisplayDevices().DeviceName, -1),
    'DisplayFrequency')
