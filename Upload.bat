@echo off
:: 1. Обновляем индекс packwiz
echo [1/4] Updating packwiz index...
packwiz.exe refresh

:: 2. Очищаем индекс Git от игнорируемых файлов (на всякий случай)
echo [2/4] Cleaning Git index...
git rm -r --cached . >nul 2>&1
git add .

:: 3. Описание комита
set /p comment="Enter commit message (or Enter for 'update'): "
if "%comment%"=="" set comment=update

:: 4. Делаем комит
echo [3/4] Committing...
git commit -m "%comment%"

:: 5. Пушим (сначала пробуем обычно, если не выйдет - предложит force)
echo [4/4] Pushing to GitHub...
git push origin main
if %errorlevel% neq 0 (
    echo.
    echo [!] Normal push failed. Trying FORCE push...
    git push origin main --force
)

echo.
echo === DONE! Your pack is updated ===
pause