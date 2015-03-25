'''
Setup file to generate cx_freeze executables.

@author: Erick Fonseca
'''

import sys
import os
from cx_Freeze import setup, Executable

includes = []

data_path = 'data'
files_path = 'files'
include_files = [(data_path, 'data'), (files_path, 'files')]

excludes = ['_gtkagg', '_tkagg', 'bsddb', 'curses', 'email', 'pywin.debugger',
            'pywin.debugger.dbgcon', 'pywin.dialogs', 'tcl',
            'Tkconstants', 'Tkinter', 'sqlite3']

packages = ['nlpnet']
path = ['src'] + sys.path

base = None
is_windows = sys.platform == "win32"
if is_windows:
    base = "Win32GUI"

exe_name = 'nlpnet.exe' if is_windows else 'nlpnet' 
executable = Executable(script= 'src/interface.py',
                        base=base,
                        targetName = exe_name,
                        )

setup(

    version = "0.1",
    description = "Graphical User Interface to nlpnet",
    author = "Erick Fonseca",
    name = "NLPNet GUI",
    options = {"build_exe": {"includes": includes,
                             "excludes": excludes,
                             "packages": packages,
                             "path": path,
                             "include_files": include_files,
                             "icon": os.path.join(files_path, "icon.ico"),
                             }
               },
    executables = [executable]
    )

