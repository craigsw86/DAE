@echo off
echo Switching to JDK 11 for Black Duck Detect...
set JAVA_HOME=C:\Program Files\OpenJDK\jdk-11
set PATH=%JAVA_HOME%\bin;%PATH%
echo.
echo Verifying Java version:
java -version
echo.
echo JAVA_HOME: %JAVA_HOME%
pause
