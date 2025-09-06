@echo off
echo Generating SSL certificates for HIPAA Checklist Project...

REM Create ssl directory if it doesn't exist
if not exist ssl mkdir ssl

REM Generate self-signed certificate using PowerShell
powershell -Command "& { $cert = New-SelfSignedCertificate -DnsName 'localhost', '127.0.0.1' -CertStoreLocation 'Cert:\CurrentUser\My' -KeyLength 2048 -KeyAlgorithm RSA -HashAlgorithm SHA256 -Subject 'CN=localhost, O=HIPAA Checklist, OU=IT Department, L=San Francisco, S=CA, C=US'; $certPath = 'Cert:\CurrentUser\My\' + $cert.Thumbprint; $certBytes = $cert.Export([System.Security.Cryptography.X509Certificates.X509ContentType]::Cert); $certPem = '-----BEGIN CERTIFICATE-----' + [Environment]::NewLine + [System.Convert]::ToBase64String($certBytes, [System.Base64FormattingOptions]::InsertLineBreaks) + [Environment]::NewLine + '-----END CERTIFICATE-----'; [System.IO.File]::WriteAllText('ssl\hipaa_checklist.crt', $certPem); $key = $cert.PrivateKey; $rsa = [System.Security.Cryptography.RSA]::Create(); $rsa.ImportParameters($key.ExportParameters($true)); $keyBytes = $rsa.ExportRSAPrivateKey(); $keyPem = '-----BEGIN RSA PRIVATE KEY-----' + [Environment]::NewLine + [System.Convert]::ToBase64String($keyBytes, [System.Base64FormattingOptions]::InsertLineBreaks) + [Environment]::NewLine + '-----END RSA PRIVATE KEY-----'; [System.IO.File]::WriteAllText('ssl\hipaa_checklist.key', $keyPem); Remove-Item $certPath -Force; Write-Host 'Certificates generated successfully!' }"

echo.
echo SSL certificates generated in ssl\ directory:
echo   - hipaa_checklist.crt (certificate)
echo   - hipaa_checklist.key (private key)
echo.
echo Note: These are self-signed certificates for development only.
echo Browsers will show a security warning - click Advanced and Proceed to continue.
echo.
pause
