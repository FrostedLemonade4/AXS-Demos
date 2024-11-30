@echo off
setlocal

REM Define Miniconda download URL and installer
set "MINICONDA_URL=https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe"
set "INSTALLER=Miniconda3-latest-Windows-x86_64.exe"

REM Download Miniconda installer
echo Downloading Miniconda installer...
powershell -Command "Invoke-WebRequest -Uri %MINICONDA_URL% -OutFile %INSTALLER%"
if not exist %INSTALLER% (
    echo Error: Failed to download Miniconda installer.
    exit /b 1
)

REM Run the Miniconda installer silently
echo Installing Miniconda...
%INSTALLER% /InstallationType=JustMe /AddToPath=1 /RegisterPython=1 /S /D=%~dp0miniconda

REM Check if installation was successful
if not exist "%~dp0miniconda\Scripts\activate.bat" (
    echo Error: Miniconda installation failed.
    exit /b 1
)

REM Activate Miniconda and create a Python environment
echo Activating Miniconda and creating environment...
call "%~dp0miniconda\Scripts\activate.bat"
conda create -n my_env python=3.9 -y
conda activate my_env

echo Miniconda setup complete!
pause
