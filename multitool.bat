@echo off
color 7
cls

:menu
cls 
echo ========================= MAIN MENU =========================
echo.
echo   [01] Run "Username Tracker"   [05] Run "Youtube V-Downloader"
echo   [02] Run "Webhook Delter"     [06] Run "Port Scanner"
echo   [03] Run "Webhook Spammer"    [07] Run "Ip Geo-Locater"
echo   [04] Run "DDOS Tool"          [08] Run "no option yet"
echo.
echo   [00] Exit
echo =============================================================
echo.

set /p choice=Enter option number:

if "%choice%"=="01" goto option1
if "%choice%"=="02" goto option2
if "%choice%"=="03" goto option3
if "%choice%"=="04" goto option4
if "%choice%"=="05" goto option5
if "%choice%"=="06" goto option6
if "%choice%"=="07" goto option7
if "%choice%"=="08" goto option8
if "%choice%"=="00" goto exit

echo Invalid choice!
pause
goto menu

:: ======= Option 1 =======
:option1
echo Running option1.py...
cd tools
python option1.py
pause
goto menu

:: ======= Option 2 =======
:option2
echo Running option2.py...
cd tools
python option2.py
pause
goto menu

:: ======= Option 3 =======
:option3
echo Running option3.py...
cd tools
start cmd /k python option3.py
pause
goto menu

:: ======= Option 4 =======
:option4
echo Running option4.py...
cd tools
python option4.py
pause
goto menu

:: ======= Option 5 =======
:option5
echo Running option5.py...
cd tools
python option5.py
pause
goto menu

:: ======= Option 6 =======
:option6
echo Running option6.py..
cd tools.
python option6.py
pause
goto menu

:: ======= Option 7 =======
:option7
echo Running option7.py...
cd tools
python option7.py
pause
goto menu

:: ======= Option 8 =======
:option8
echo Running option8.py...
cd tools
python option8.py
pause
goto menu

:exit
echo Exiting...
timeout /t 1 >nul
exit
