from cx_Freeze import setup, Executable
import sys, platform

if platform.system() == 'Windows':
    build_exe_options = {"packages": ["os", "cocos", "pyglet", "random", "win32api"],
                         "includes": ["pyglet.resource"],
                         "include_files": ["resources", "glvars.py", "Game.py", "progressBar.py", "sprites.py"],
                         "excludes": ["tkinter"]}
elif platform.system() == 'Darwin':
    build_exe_options = {"packages": ["os", "cocos", "pyglet", "random",
                                      "AppKit", "pkg_resources._vendor", "_sysconfigdata_m_darwin_darwin",
                                      ],
                         "includes": ["pyglet.resource"],
                         "include_files": ["resources", "glvars.py", "Game.py", "progressBar.py", "sprites.py"],
                         "excludes": ["tkinter"]}

else:
    raise OSError('Your platform is not supported!')

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(options={"build_exe": build_exe_options},
      name='PacPong',
      version='0.1',
      description='PacPong',
      executables=[Executable("main.py", base=base)])
