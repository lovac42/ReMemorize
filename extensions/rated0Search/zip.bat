@echo off
set ZIP=C:\PROGRA~1\7-Zip\7z.exe a -tzip -y -r
set REPO=Rated0Search

%ZIP% %REPO%_20.zip %REPO%.py

%ZIP% %REPO%_21.ankiaddon *.py *.json
