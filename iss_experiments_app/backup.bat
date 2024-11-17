@echo off
:: Define variables for date and time
for /f "tokens=1-4 delims=/ " %%a in ("%date%") do set datestamp=%%d%%b%%c
for /f "tokens=1-3 delims=:., " %%a in ("%time%") do set timestamp=%%a%%b%%c

:: Ensure timestamp has no leading spaces
set timestamp=%timestamp: =0%

:: Define backup paths and zip file name
set "backupDir=TemporaryBackup"
set "backupStorage=Backups"
set "zipFile=%backupStorage%\Backup_%datestamp%_%timestamp%.zip"

:: Create a Backups folder if it doesn't exist
if not exist "%backupStorage%" (
    mkdir "%backupStorage%"
)

:: Create a temporary backup folder for files
if not exist "%backupDir%" (
    mkdir "%backupDir%"
)

:: Copy all files and subdirectories, excluding specific folders
robocopy . "%backupDir%" /e /xd "%backupDir%" "%backupStorage%" "kivy_env"

:: Compress the temporary backup folder into a zip file in the Backups folder
powershell -Command "Compress-Archive -Path '%backupDir%\*' -DestinationPath '%zipFile%' -Force"

:: Cleanup the temporary backup folder
rmdir /s /q "%backupDir%"

echo Backup complete: %zipFile%
pause
