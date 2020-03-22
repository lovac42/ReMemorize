@echo off
set ZIP=C:\PROGRA~1\7-Zip\7z.exe a -tzip -y -r
set REPO=rememorize

set VERSION=1.3.1


REM Init, Version info
echo from .main import * >>%REPO%/__init__.py

echo %VERSION% >%REPO%/VERSION


REM Create checksums
fsum -r -jm -md5 -d%REPO% * > checksum.md5
move checksum.md5 %REPO%/checksum.md5


REM PACK ZIP FILES
%ZIP% %REPO%_v%VERSION%_Anki20.zip *.py %REPO%/*.*


cd %REPO%
quick_manifest.exe "ReMemorize" "323586997" >manifest.json
%ZIP% ../%REPO%_v%VERSION%_Anki21.ankiaddon *.*


quick_manifest.exe "ReMemorize" "ReMemorize" >manifest.json
%ZIP% ../%REPO%_v%VERSION%_CCBC.adze *
