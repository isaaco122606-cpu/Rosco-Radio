@echo off
setlocal
set "CHANNEL=stable"
if /I "%~1"=="beta" set "CHANNEL=beta"

powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0RoscoRadio-Online-Installer.ps1" -Channel "%CHANNEL%"
set "RC=%ERRORLEVEL%"
if not "%RC%"=="0" pause
exit /b %RC%
