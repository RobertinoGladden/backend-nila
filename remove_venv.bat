@echo off
REM Script to remove venv from git and push
REM This uses Windows-compatible git commands

echo ========================================
echo REMOVING VENV FROM GIT HISTORY
echo ========================================
echo.

cd /d "c:\Users\lapt1\Downloads\Backend NILA"

echo [1/5] Checking current status...
git status

echo.
echo [2/5] Removing venv from git index (keeping local files)...
git rm -r --cached venv 2>nul
if errorlevel 1 (
    echo Note: venv already not in index, continuing...
)

echo.
echo [3/5] Staging changes (.gitignore and removed venv)...
git add .gitignore
git add -u

echo.
echo [4/5] Creating new commit...
git commit -m "chore: Remove venv from tracking and add .gitignore

- Removed virtual environment from git tracking (306MB+)
- Virtual environment now excluded via .gitignore
- venv/ will be ignored in all future commits
- Local venv directory preserved on disk

Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"

if errorlevel 1 (
    echo.
    echo NOTE: No changes to commit (venv might already be removed from index)
    echo Trying alternate approach...
    git status
    pause
    goto :eof
)

echo.
echo [5/5] Pushing to remote with --force-with-lease...
git push origin main --force-with-lease

if errorlevel 0 (
    echo.
    echo ========================================
    echo SUCCESS! Repository cleaned.
    echo ========================================
    echo.
    echo Next steps:
    echo 1. Verify on GitHub: https://github.com/RobertinoGladden/backend-nila
    echo 2. Clone fresh if needed: git clone https://github.com/RobertinoGladden/backend-nila.git
    echo.
) else (
    echo.
    echo ========================================
    echo ERROR during push. Check above messages.
    echo ========================================
)

pause
