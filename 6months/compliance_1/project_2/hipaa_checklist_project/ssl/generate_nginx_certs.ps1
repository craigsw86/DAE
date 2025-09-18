# Generate SSL certificates for Nginx HTTPS configuration
# This script creates self-signed certificates compatible with the nginx-https.conf

Write-Host "Generating SSL certificates for HIPAA Checklist Project..." -ForegroundColor Green

# Create ssl directory if it doesn't exist
if (!(Test-Path "ssl")) {
    New-Item -ItemType Directory -Name "ssl" | Out-Null
}

# Generate a self-signed certificate with the correct subject
$cert = New-SelfSignedCertificate -DnsName "localhost", "127.0.0.1" -CertStoreLocation "Cert:\CurrentUser\My" -KeyLength 2048 -KeyAlgorithm RSA -HashAlgorithm SHA256 -Subject "CN=localhost, O=HIPAA Checklist, OU=IT Department, L=San Francisco, S=CA, C=US"

Write-Host "Certificate generated with thumbprint: $($cert.Thumbprint)" -ForegroundColor Yellow

# Export certificate to PEM format
$certPath = "Cert:\CurrentUser\My\$($cert.Thumbprint)"
$certBytes = $cert.Export([System.Security.Cryptography.X509Certificates.X509ContentType]::Cert)

# Create certificate file
$certPem = "-----BEGIN CERTIFICATE-----`n" + [System.Convert]::ToBase64String($certBytes, [System.Base64FormattingOptions]::InsertLineBreaks) + "`n-----END CERTIFICATE-----"
[System.IO.File]::WriteAllText("ssl\hipaa_checklist.crt", $certPem)

# Export private key
$privateKey = $cert.PrivateKey
$rsa = [System.Security.Cryptography.RSA]::Create()
$rsa.ImportParameters($privateKey.ExportParameters($true))

# Convert private key to PEM format
$keyBytes = $rsa.ExportRSAPrivateKey()
$keyPem = "-----BEGIN RSA PRIVATE KEY-----`n" + [System.Convert]::ToBase64String($keyBytes, [System.Base64FormattingOptions]::InsertLineBreaks) + "`n-----END RSA PRIVATE KEY-----"
[System.IO.File]::WriteAllText("ssl\hipaa_checklist.key", $keyPem)

# Set proper permissions
try {
    icacls "ssl\hipaa_checklist.key" /inheritance:r /grant:r "$env:USERNAME:F" | Out-Null
    icacls "ssl\hipaa_checklist.crt" /inheritance:r /grant:r "$env:USERNAME:F" | Out-Null
} catch {
    Write-Host "Could not set file permissions (this is normal on some systems)" -ForegroundColor Yellow
}

# Clean up certificate from store
Remove-Item "Cert:\CurrentUser\My\$($cert.Thumbprint)" -Force

Write-Host "SSL certificates generated successfully!" -ForegroundColor Green
Write-Host "Certificate files created in ssl\ directory:" -ForegroundColor Cyan
Write-Host "   - hipaa_checklist.crt (certificate)" -ForegroundColor White
Write-Host "   - hipaa_checklist.key (private key)" -ForegroundColor White
Write-Host ""
Write-Host "Note: These are self-signed certificates for development only." -ForegroundColor Yellow
Write-Host "Browsers will show a security warning - click Advanced and Proceed to continue." -ForegroundColor Yellow
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "   1. Start the Docker containers with: docker-compose -f docker-compose.nginx.yml up" -ForegroundColor White
Write-Host "   2. Test HTTPS setup with: python test_https_setup.py" -ForegroundColor White
Write-Host "   3. Access the application at: https://localhost" -ForegroundColor White