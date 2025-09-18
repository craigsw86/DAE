# Generate self-signed SSL certificate for HIPAA Checklist Project
# This script creates a self-signed certificate for local HTTPS testing

# Create a self-signed certificate
$cert = New-SelfSignedCertificate -DnsName "localhost", "127.0.0.1" -CertStoreLocation "Cert:\CurrentUser\My" -KeyLength 2048 -KeyAlgorithm RSA -HashAlgorithm SHA256

# Export the certificate to PEM format
$certPath = "Cert:\CurrentUser\My\$($cert.Thumbprint)"
$pwd = ConvertTo-SecureString -String "hipaa123" -Force -AsPlainText

# Export certificate
Export-Certificate -Cert $certPath -FilePath "hipaa-cert.pem" -Type CERT

# Export private key
$cert | Export-PfxCertificate -FilePath "hipaa-temp.pfx" -Password $pwd

# Convert PFX to PEM using OpenSSL (if available) or use alternative method
try {
    # Try to use OpenSSL if available
    openssl pkcs12 -in hipaa-temp.pfx -out hipaa-key.pem -nodes -passin pass:hipaa123
    Remove-Item "hipaa-temp.pfx"
    Write-Host "SSL certificates generated successfully!"
    Write-Host "Certificate: hipaa-cert.pem"
    Write-Host "Private Key: hipaa-key.pem"
} catch {
    Write-Host "OpenSSL not available. Creating basic certificate files..."
    # Create basic certificate files for testing
    $certBytes = $cert.Export([System.Security.Cryptography.X509Certificates.X509ContentType]::Cert)
    [System.IO.File]::WriteAllBytes("hipaa-cert.pem", $certBytes)
    Write-Host "Basic certificate created. For production, use proper certificate management."
}

# Clean up
Remove-Item "hipaa-temp.pfx" -ErrorAction SilentlyContinue
