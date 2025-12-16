@echo off
echo === TopEndSports MCP Server - Windows Setup ===
echo.

REM Try to find Node.js
where node >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [OK] Node.js found in PATH
    node --version
    goto :build
)

echo [!] Node.js not in PATH. Searching common locations...

if exist "C:\Program Files\nodejs\node.exe" (
    echo Found at: C:\Program Files\nodejs\node.exe
    set "PATH=C:\Program Files\nodejs;%PATH%"
    goto :build
)

if exist "%LOCALAPPDATA%\Programs\nodejs\node.exe" (
    echo Found at: %LOCALAPPDATA%\Programs\nodejs\node.exe
    set "PATH=%LOCALAPPDATA%\Programs\nodejs;%PATH%"
    goto :build
)

if exist "%APPDATA%\nvm" (
    echo Found nvm installation at: %APPDATA%\nvm
    for /d %%i in ("%APPDATA%\nvm\v*") do (
        if exist "%%i\node.exe" (
            echo Using: %%i
            set "PATH=%%i;%PATH%"
            goto :build
        )
    )
)

if exist "%ProgramFiles%\nodejs\node.exe" (
    echo Found at: %ProgramFiles%\nodejs\node.exe
    set "PATH=%ProgramFiles%\nodejs;%PATH%"
    goto :build
)

echo [ERROR] Node.js not found! Please install from https://nodejs.org
pause
exit /b 1

:build
echo.
echo === Building MCP Server ===
cd /d "%~dp0"
call npm install
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] npm install failed!
    pause
    exit /b 1
)

call npm run build
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Build failed!
    pause
    exit /b 1
)

echo.
echo === Build Successful ===
echo.
echo Add this to your Claude Desktop config file:
echo Location: %APPDATA%\Claude\claude_desktop_config.json
echo.
echo {
echo   "mcpServers": {
echo     "topendsports-briefs": {
echo       "command": "node",
echo       "args": ["%~dp0dist\index.js"]
echo     }
echo   }
echo }
echo.
echo Then restart Claude Desktop.
pause
