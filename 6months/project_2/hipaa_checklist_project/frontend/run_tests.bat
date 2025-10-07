@echo off
echo  Running Week 9 Day 3 Jest Tests...
echo =====================================

echo.
echo  Running all tests with coverage...
npm test -- --watchAll=false --coverage --verbose

echo.
echo  Test run completed!
echo  Check the coverage/ directory for detailed coverage reports
echo  HTML coverage report: coverage/lcov-report/index.html

pause
