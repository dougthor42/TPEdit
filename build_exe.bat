call C:\WinPython27\Scripts\env.bat
cd C:\WinPython27\projects\github\TPEdit
RMDIR /S /Q .\build\exe.win32-2.7 
python build_executables.py build
cd .\build\exe.win32-2.7
main.exe