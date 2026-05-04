@echo off
REM User Management System - Quick Test Script
REM Usage: Run this script to test all user management endpoints

REM Configuration
set BASE_URL=http://localhost:8000
set FARMER_EMAIL=farmer@test.com
set FARMER_PASSWORD=SecurePass123
set ADMIN_EMAIL=admin@test.com
set ADMIN_PASSWORD=AdminPass123

echo.
echo ========================================
echo User Management System - Quick Test
echo ========================================
echo.

REM Step 1: Register Farmer
echo [1/5] Registering farmer account...
curl -X POST %BASE_URL%/auth/register ^
  -H "Content-Type: application/json" ^
  -d "{\"email\":\"%FARMER_EMAIL%\",\"password\":\"%FARMER_PASSWORD%\",\"full_name\":\"Test Farmer\",\"phone_number\":\"081234567890\",\"greenhouse_location\":\"Jakarta\",\"address\":\"Jl Test No 1\"}"

timeout /t 2

REM Step 2: Register Admin (manual role promotion needed)
echo.
echo [2/5] Registering admin account...
curl -X POST %BASE_URL%/auth/register ^
  -H "Content-Type: application/json" ^
  -d "{\"email\":\"%ADMIN_EMAIL%\",\"password\":\"%ADMIN_PASSWORD%\",\"full_name\":\"Test Admin\",\"phone_number\":\"089999999999\",\"greenhouse_location\":\"Bandung\",\"address\":\"Jl Admin No 1\"}"

timeout /t 2

REM Step 3: Login Farmer (get token)
echo.
echo [3/5] Logging in farmer account...
echo Note: Save the access_token from response below!
echo.
for /f "tokens=*" %%i in ('curl -s -X POST %BASE_URL%/auth/login ^
  -H "Content-Type: application/json" ^
  -d "{\"email\":\"%FARMER_EMAIL%\",\"password\":\"%FARMER_PASSWORD%\"}"') do (
  set RESPONSE=%%i
  echo %%i
)

timeout /t 2

REM Step 4: Get Dashboard
echo.
echo [4/5] Testing dashboard endpoint...
echo Note: Replace TOKEN with access_token from Step 3
echo.
echo curl -X GET %BASE_URL%/users/dashboard ^
  -H "Authorization: Bearer TOKEN"
echo.

REM Step 5: Instructions
echo [5/5] Next steps:
echo.
echo 1. Copy the access_token from Step 3 response
echo 2. Run this command (replace TOKEN):
echo    curl -X GET %BASE_URL%/users/dashboard -H "Authorization: Bearer TOKEN"
echo.
echo 3. To promote admin:
echo    - Open pgAdmin4
echo    - Find users table
echo    - Set role='admin' for admin@test.com
echo.
echo 4. Then test admin endpoints:
echo    curl -X GET %BASE_URL%/users ^
echo      -H "Authorization: Bearer ADMIN_TOKEN"
echo.

echo.
echo ========================================
echo Test Complete!
echo ========================================
echo.
echo For detailed testing guide, see: SETUP_USER_MANAGEMENT.md
echo For full API reference, see: USER_MANAGEMENT_ENDPOINTS_INDONESIAN.md
echo.

pause
