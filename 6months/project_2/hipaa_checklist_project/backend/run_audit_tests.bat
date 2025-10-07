@echo off
echo  Running Week 9 Day 4: Audit Logging Tests...
echo ================================================

echo.
echo  Running backend audit logging tests...
python audit_logging_tests.py

echo.
echo  Backend audit logging tests completed!
echo  Check WEEK9_DAY4_AUDIT_LOGGING_REPORT.json for detailed results

echo.
echo  To run frontend audit log tests:
echo    cd ..\frontend
echo    npm test -- --testPathPattern=AuditLog.test.js

pause
