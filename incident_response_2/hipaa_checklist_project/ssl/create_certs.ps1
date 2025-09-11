# Simple SSL certificate creation for Nginx
$cert = New-SelfSignedCertificate -DnsName "localhost" -CertStoreLocation "Cert:\CurrentUser\My" -KeyLength 2048
$certPath = "Cert:\CurrentUser\My\$($cert.Thumbprint)"

# Export certificate
$cert | Export-Certificate -FilePath "ssl\hipaa_checklist.crt" -Type CERT

# Export private key as PFX
$cert | Export-PfxCertificate -FilePath "ssl\hipaa_checklist.pfx" -Password (ConvertTo-SecureString -String "password" -Force -AsPlainText)

# Clean up
Remove-Item $certPath -Force

Write-Host "Certificate files created in ssl directory"
