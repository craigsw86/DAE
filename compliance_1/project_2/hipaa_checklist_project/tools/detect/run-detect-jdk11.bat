@echo off
echo ========================================
echo Black Duck Detect with JDK 11
echo ========================================
echo.

REM Set JDK 11 environment
set JAVA_HOME=C:\Program Files\OpenJDK\jdk-11
set PATH=%JAVA_HOME%\bin;%PATH%

echo Verifying Java version:
java -version
echo.

echo Current directory: %CD%
echo JAVA_HOME: %JAVA_HOME%
echo.

REM Check if detect.ps1 exists
if not exist "detect.ps1" (
    echo Downloading detect.ps1...
    powershell -Command "Invoke-WebRequest -Uri 'https://detect.blackduck.com/detect10.ps1' -OutFile 'detect.ps1'"
)

REM Run Black Duck Detect with comprehensive options
echo Running Black Duck Detect...
echo This may take 15-20 minutes...
echo.

powershell -ExecutionPolicy Bypass -File .\detect.ps1 ^
    --detect.project.name="hipaa_checklist_project" ^
    --detect.source.path=".." ^
    --detect.detector.search.depth=3 ^
    --detect.python.path="python" ^
    --detect.npm.path="npm" ^
    --detect.output.path="../reports/detect" ^
    --detect.log.level=TRACE ^
    *> detect-output.txt 2>&1

echo.
echo ========================================
echo Detect scan completed!
echo ========================================
echo.
echo Check detect-output.txt for detailed logs
echo Check ../reports/detect for scan results
echo.
pause
