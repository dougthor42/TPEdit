# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 13:08:24 2015

@author: dthor
"""

# ---------------------------------------------------------------------------
### Imports
# ---------------------------------------------------------------------------
# Standard Library
import sys
import logging

# Third Party
from cx_Freeze import setup, Executable

# Package / Application
from tpedit import (__version__,
                    __project_url__,
                    __project_name__,
                    __short_description__,
                    )


# ---------------------------------------------------------------------------
### General Setup
# ---------------------------------------------------------------------------
# turn off logging if we're going to build a distribution
logging.disable(logging.CRITICAL)


# ---------------------------------------------------------------------------
### build_exe Setup
# ---------------------------------------------------------------------------


# included packages and their submodules
packages = [
            "lxml",
            "gzip",
            ]

# included modules
includes = [
            "lxml._elementpath",
            "gzip",
            ]

# Files to include (and their destinations)
include_files = ["pybank\\test_database.db",
                 ("log\\README.txt", "log\\README.txt"),  # (source, dest)
                 ]

# list of names of files to include when determining dependencies of
# binary files that would normally be excluded; note that version
# numbers that normally follow the shared object extension are
# stripped prior to performing the comparison
bin_includes = [

                ]

# Options for build_exe
build_exe_opts = {
                  "packages": packages,
#                  "includes": includes,
#                  "include_files": include_files,
                  "silent": True,
                  }


# ---------------------------------------------------------------------------
### Executable Definitions
# ---------------------------------------------------------------------------
file_to_build = "tpedit\\main.py"

# Application Base
base = None
#if sys.platform == 'win32':        # uncomment this to remove console window.
#    base = "Win32GUI"

exe1 = Executable(file_to_build,
                  base=base,
                  targetName="TPEdit.exe",
                  )

# List of which executables to build
exes_to_build = [
                 exe1,
                 ]


# ---------------------------------------------------------------------------
### setup()
# ---------------------------------------------------------------------------
setup(
    name=__project_name__,
    version=__version__,
    description=__short_description__,
    options={"build_exe": build_exe_opts},
    executables=exes_to_build,
)
