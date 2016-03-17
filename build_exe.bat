call C:\WinPython27\Scripts\env.bat
cd C:\gitlab\dthor\TPEdit
echo ----- Deleting previous build -----
RMDIR /S /Q .\build\exe.win32-2.7
echo ----- Running build script -----
python build_executables.py build
echo ----- Launching Application -----
cd .\build\exe.win32-2.7
TPEdit.exe
cd ..\..
echo ----- Finished -----
@echo off
set size=0
for /r %%x in (.\build\exe.win32-2.7\*) do set /a size+=%%~zx
set /a mb = %size% / 1000000
echo %size% Bytes
echo %mb% MB