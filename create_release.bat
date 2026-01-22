@echo off
REM Helper script to create a new release (Windows)

echo ======================================
echo Mouse Tracker - Release Creator
echo ======================================
echo.

REM Check if we're in a git repository
git rev-parse --git-dir >nul 2>&1
if errorlevel 1 (
    echo Error: Not in a git repository!
    pause
    exit /b 1
)

REM Get current version
for /f "tokens=*" %%i in ('git describe --tags --abbrev=0 2^>nul') do set CURRENT_VERSION=%%i
if "%CURRENT_VERSION%"=="" set CURRENT_VERSION=v0.0.0
echo Current version: %CURRENT_VERSION%
echo.

REM Ask for new version
set /p NEW_VERSION="Enter new version (e.g., v1.0.0, v1.1.0): "

echo.
echo Creating release %NEW_VERSION%...
echo.

REM Create and push tag
echo Creating git tag...
git tag -a "%NEW_VERSION%" -m "Release %NEW_VERSION%"

echo Pushing tag to remote...
git push origin "%NEW_VERSION%"

echo.
echo ======================================
echo √ Release %NEW_VERSION% created!
echo ======================================
echo.
echo GitHub Actions will now:
echo   1. Build executables for Windows, Linux, and macOS
echo   2. Create a GitHub Release
echo   3. Upload all executables automatically
echo.
echo Check the Actions tab on GitHub to see progress.
echo.
pause
