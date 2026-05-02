@echo off
REM Script to remove venv from git - FIXED VERSION
REM Using Git Bash if available, otherwise raw git commands

echo ========================================
echo REMOVING VENV FROM GIT HISTORY
echo ========================================
echo.

cd /d "c:\Users\lapt1\Downloads\Backend NILA"

echo [1/4] Current git status...
git status

echo.
echo [2/4] Resetting last 3 commits (these have venv in them)...
echo Resetting to origin/main...
git reset --soft origin/main

echo.
echo [3/4] Removing venv and staging clean files...
REM Remove venv from staging
git reset HEAD venv/ 2>nul

REM Add everything except venv
git add -A
git reset HEAD venv/ 2>nul

echo.
echo Files to commit:
git status

echo.
echo [4/4] Creating new clean commit...
git commit -m "feat: Complete backend system with 26 endpoints and full documentation

Features:
- 26 API endpoints (Auth, Farming, Feed, ML)
- 17 database tables with proper relationships
- JWT authentication with bcrypt password hashing
- Farming cycle management (seed to harvest)
- Feed stock tracking and transaction history
- ML predictions for harvest and feeding
- Comprehensive documentation (English and Indonesian)
- Added .gitignore to prevent venv tracking

Co-authored-by: Copilot (223556219+Copilot@users.noreply.github.com)"

echo.
echo [5/5] Pushing to remote with force...
git push origin main --force-with-lease

echo.
echo ========================================
if %ERRORLEVEL% EQU 0 (
    echo SUCCESS! Venv removed and pushed cleanly.
) else (
    echo ERROR during push.
)
echo ========================================
pause
