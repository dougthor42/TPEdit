# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 13:08:24 2015

@author: dthor
"""

### #------------------------------------------------------------------------
### Imports
### #------------------------------------------------------------------------
# Standard Library
import sys

# Third Party
from cx_Freeze import setup, Executable

# Package / Application
#from pybank import (__version__,
#                    __project_url__,
#                    __project_name__,
#                    )

# turn off logging if we're going to build a distribution
#logging.disable(logging.CRITICAL)

#include_files = ["pybank\\test_database.db",
#                 ("log\\README.txt", "log\\README.txt"),  # (source, dest)
#                 ]


build_exe_opts = {
#                  "includes": ["pybank/pbsql", ],
#                  "include_files": include_files,
                  "silent": True,
                  }

base = None
if sys.platform == 'win32':
    base = "Win32GUI"

exes_to_build = [Executable("tpedit\\tpedit_mockup.py", base=base),
                 ]

setup(
    name="gTPEditor_Mockup",
    version="0.0.1",
    description="gTPEditor_Mockup",
    options={"build_exe": build_exe_opts},
    executables=exes_to_build,
)
