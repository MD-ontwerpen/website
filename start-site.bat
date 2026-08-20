@echo off
setlocal enabledelayedexpansion
REM ============================================================
REM  MD-ontwerpen - local preview
REM  Double-click this file to view the site in your browser.
REM  Close this black window when you are done to stop it.
REM ============================================================

cd /d "%~dp0"

set "PY="
where python  >nul 2>&1 && set "PY=python"
if not defined PY where python3 >nul 2>&1 && set "PY=python3"
if not defined PY where py      >nul 2>&1 && set "PY=py"

if not defined PY (
  echo.
  echo   ERROR: Python was not found on this computer.
  echo   Install it from https://www.python.org/downloads/
  echo.
  pause
  exit /b 1
)

echo.
echo   MD-ontwerpen - local preview
echo   ---------------------------------------------
echo   On this computer:  http://localhost:5510
for /f "tokens=2 delims=:" %%i in ('ipconfig ^| findstr /i "IPv4"') do (
  set "IP=%%i"
  set "IP=!IP: =!"
  echo   On your phone:     http://!IP!:5510
)
echo   ---------------------------------------------
echo   Keep this window open while testing.
echo   Close it, or press Ctrl+C, to stop.
echo.

start "" http://localhost:5510
%PY% -m http.server 5510
