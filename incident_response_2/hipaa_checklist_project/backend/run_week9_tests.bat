@echo off
echo ========================================
echo Week 9: API CRUD and SQL Verification
echo ========================================
echo.

echo Starting Django backend...
start /B python manage.py runserver

echo Waiting for server to start...
timeout /t 5 /nobreak > nul

echo.
echo ========================================
echo Running SQL Verification Tests...
echo ========================================
echo.

echo Testing database structure and queries...
sqlite3 db.sqlite3 < sql_verification.sql

echo.
echo ========================================
echo Running API CRUD Tests...
echo ========================================
echo.

echo Testing all API endpoints...
python api_test_script.py

echo.
echo ========================================
echo Running Django Model Tests...
echo ========================================
echo.

echo Testing Django models and CRUD operations...
python test_crud_and_sql.py

echo.
echo ========================================
echo Week 9 Tests Complete!
echo ========================================
echo.
echo Check the generated reports:
echo - database_summary.csv (SQL verification results)
echo - api_test_report.json (API testing results)
echo.
pause
