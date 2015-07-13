call C:\WinPython27\Scripts\env.bat
RMDIR /S /Q .\build\exe.win32-2.7 
%WINPYDIR%\python.exe build_executables.py build
.\build\exe.win32-2.7\main.exe