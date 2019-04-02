from cx_Freeze import setup, Executable
import sys
# import os.path

build_exe_options = {"packages": ["os", "cocos", "pyglet", "random"
                                  # "AppKit", "pkg_resources._vendor", "_sysconfigdata_m_darwin_darwin",
                                  ],
                     "includes": ["pyglet.resource"],
                     "include_files": [# "tcl86t.dll", "tk86t.dll",
                                       "resources", "glvars.py"],
                     "excludes": ["tkinter"]}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

# PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
# os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
# os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')


setup(options={"build_exe": build_exe_options},
      name='PacPong',
      version='0.1',
      description='PacPong',
      executables=[Executable("Game.py", base=base)])
