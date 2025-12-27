@echo off
:: 1. Обновляем индекс packwiz (чтобы зафиксировать изменения в модах)
echo [1/4] Updating packwiz index...
packwiz.exe refresh

:: 2. Добавляем все изменения в Git
echo [2/4] Adding files to Git...
git add .

:: 3. Спрашиваем описание для комита
set /p comment="Enter commit message (or press Enter for 'update'): "
if "%comment%"=="" set comment=update

:: 4. Делаем комит
echo [3/4] Committing...
git commit -m "%comment%"

:: 5. Пушим на сервер
echo [4/4] Pushing to GitHub...
git push origin main --force

echo.
echo === DONE! Your pack is updated on GitHub ===
pause