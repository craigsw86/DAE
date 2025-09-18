# PowerShell script to switch between JDK 8 and JDK 11
# Usage: .\switch-java-version.ps1 -Version 11 (or 8)

param(
    [Parameter(Mandatory=$true)]
    [ValidateSet("8", "11")]
    [string]$Version
)

Write-Host "Switching to JDK $Version..." -ForegroundColor Green

if ($Version -eq "11") {
    # Set JDK 11 as default
    $env:JAVA_HOME = "C:\Program Files\OpenJDK\jdk-11"
    $env:Path = "$env:JAVA_HOME\bin;" + $env:Path
    Write-Host "JDK 11 set as default" -ForegroundColor Yellow
} else {
    # Set JDK 8 as default
    $env:JAVA_HOME = "C:\Program Files\Java\jre1.8.0_461"
    $env:Path = "$env:JAVA_HOME\bin;" + $env:Path
    Write-Host "JDK 8 set as default" -ForegroundColor Yellow
}

# Verify the switch
Write-Host "`nVerifying Java version:" -ForegroundColor Cyan
java -version

Write-Host "`nJava locations:" -ForegroundColor Cyan
where java

Write-Host "`nJAVA_HOME: $env:JAVA_HOME" -ForegroundColor Cyan
