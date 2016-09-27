# -*- coding: utf-8 -*-

# An advanced setup script to create multiple executables and demonstrate a few
# of the features available to setup scripts
#
# Run the build process by running the command 'python setup.py build'
#
# If everything works well you should find a subdirectory in the build
# subdirectory that contains the files needed to run the script without Python

import sys
from cx_Freeze import setup, Executable

options = {
    'build_exe': {
        'compressed': True,
        'include_files': [],
        'includes': [],
    }
}

executables = [
    Executable('hostServer.py'),
]

setup(name='launcher executable',
      version='0.1',
      description='executable for MES auto testing',
      options=options,
      executables=executables
      )
