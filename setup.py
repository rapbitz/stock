from distutils.core import setup
import py2exe

setup(console=['main.py'])

# -----------------------------------------------------------
# import sys
# from cx_Freeze import setup, Executable

# base = None
# if sys.platform == 'win32':
#     base = 'Win32GUI'

# executables = [
#     Executable('main.py', base=base)
# ]

# setup(name='simple_Stock',
#       version='0.1',
#       description='cx_Freeze Tkinter RnD Stock',
#       executables=executables
#       )