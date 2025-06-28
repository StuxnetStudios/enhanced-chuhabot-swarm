@echo off
REM Simple batch file to check C controller requirements

echo ChuhaBot C Controller - Build Check
echo ====================================

echo.
echo Checking source file...
if exist chuha_c_controller.c (
    echo [OK] Source file found: chuha_c_controller.c
) else (
    echo [ERROR] Source file not found: chuha_c_controller.c
    goto :end
)

echo.
echo Checking for Webots installation...
set WEBOTS_FOUND=0

if defined WEBOTS_HOME (
    if exist "%WEBOTS_HOME%\include\controller\c\webots\robot.h" (
        echo [OK] Webots found at: %WEBOTS_HOME%
        set WEBOTS_FOUND=1
    )
)

if %WEBOTS_FOUND%==0 (
    if exist "C:\Program Files\Webots\include\controller\c\webots\robot.h" (
        echo [OK] Webots found at: C:\Program Files\Webots
        set WEBOTS_FOUND=1
    )
)

if %WEBOTS_FOUND%==0 (
    echo [ERROR] Webots not found. Please install Webots or set WEBOTS_HOME
)

echo.
echo Checking for compiler...
gcc --version >nul 2>&1
if %errorlevel%==0 (
    echo [OK] GCC compiler found
    goto :compiler_found
)

cl >nul 2>&1
if %errorlevel%==0 (
    echo [OK] Visual Studio compiler found
    goto :compiler_found
)

clang --version >nul 2>&1
if %errorlevel%==0 (
    echo [OK] Clang compiler found
    goto :compiler_found
)

echo [ERROR] No compiler found. Install Visual Studio Build Tools, MinGW, or GCC
goto :end

:compiler_found
echo.
echo Build requirements check complete!
echo.
echo To build the controller:
echo 1. Install Webots if not found
echo 2. Set up a C compiler (Visual Studio, MinGW, etc.)
echo 3. Use the appropriate build command for your system
echo.
echo To use in Webots:
echo 1. Open Webots
echo 2. Load a world with ChuhaBot robots
echo 3. Set controller to 'chuha_c_controller'
echo 4. Start simulation

:end
pause
