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
import logging

# Third Party
from cx_Freeze import setup, Executable

# Package / Application
from tpedit import (__version__,
                    __project_url__,
                    __project_name__,
                    )

# turn off logging if we're going to build a distribution
logging.disable(logging.CRITICAL)

#include_files = ["pybank\\test_database.db",
#                 ("log\\README.txt", "log\\README.txt"),  # (source, dest)
#                 ]

include_packages = [
                    "lxml",
                    "gzip",
                    ]
#include_modules = [
#                   "lxml._elementpath",
#                   "gzip",
#                   ]
build_exe_opts = {
                  "packages": include_packages,
#                  "includes": include_modules,
#                  "include_files": include_files,
                  "silent": True,
                  }

base = None
#if sys.platform == 'win32':        # uncomment this to remove console window.
#    base = "Win32GUI"

exes_to_build = [Executable("tpedit\\main.py", base=base),
                 ]

setup(
    name=__project_name__,
    version=__version__,
    description="FTI test program editor and diff tool.",
    options={"build_exe": build_exe_opts},
    executables=exes_to_build,
)
