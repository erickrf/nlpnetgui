'''
Setup file to generate cx_freeze executables.

@author: Erick Fonseca
'''

import sys
import os
from cx_Freeze import setup, Executable

includes = ['run']

data_path = os.path.join('..', 'nlpnet', 'data')
files_path = os.path.join('..', 'files')
include_files = [(data_path, 'data'), (files_path, 'files')]

excludes = ['_gtkagg', '_tkagg', 'bsddb', 'curses', 'email', 'pywin.debugger',
            'pywin.debugger.dbgcon', 'pywin.dialogs', 'tcl',
            'Tkconstants', 'Tkinter', 'sqlite3']

packages = []
path = [os.path.join('..', 'nlpnet')] + sys.path

base = None
is_windows = sys.platform == "win32"
if is_windows:
    base = "Win32GUI"

exe_name = 'nlpnet.exe' if is_windows else 'nlpnet' 
executable = Executable(script= "interface.py",
                        base=base,
                        targetName = exe_name,
                        )

setup(

    version = "0.1",
    description = "Graphical User Interface to the NLPNET software",
    author = "Erick Fonseca",
    name = "NLPNET GUI",
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

