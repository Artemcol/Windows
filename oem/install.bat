@echo off
echo ===========================================
echo   Starting custom setup for Windows 10
echo ===========================================

REM --- Установка Roblox Studio (тихая) ---
echo Downloading Roblox Studio...
powershell -Command "Invoke-WebRequest -Uri 'https://setup.rbxcdn.com/RobloxStudioLauncherBeta.exe' -OutFile '%TEMP%\RobloxStudioLauncher.exe'"
if exist %TEMP%\RobloxStudioLauncher.exe (
    echo Installing Roblox Studio...
    start /wait %TEMP%\RobloxStudioLauncher.exe /silent
    echo Roblox Studio installed.
) else (
    echo Failed to download Roblox Studio.
)

REM --- Дополнительные настройки (примеры) ---
REM Отключаем спящий режим
powercfg -change -standby-timeout-ac 0
powercfg -change -standby-timeout-dc 0

REM Устанавливаем часовой пояс (Москва)
tzutil /s "Russian Standard Time"

echo ===========================================
echo   Custom setup completed!
echo ===========================================
