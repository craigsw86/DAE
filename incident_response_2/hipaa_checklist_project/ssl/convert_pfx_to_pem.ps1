# Convert PFX to PEM format for Nginx
$pfxPath = "ssl\hipaa_checklist.pfx"
$keyPath = "ssl\hipaa_checklist.key"
$password = "password"

# Load the PFX file
$pfx = New-Object System.Security.Cryptography.X509Certificates.X509Certificate2
$pfx.Import($pfxPath, $password, [System.Security.Cryptography.X509Certificates.X509KeyStorageFlags]::Exportable)

# Get the private key
$privateKey = $pfx.PrivateKey
$rsa = [System.Security.Cryptography.RSA]::Create()
$rsa.ImportParameters($privateKey.ExportParameters($true))

# Export as PEM
$keyBytes = $rsa.ExportRSAPrivateKey()
$keyPem = "-----BEGIN RSA PRIVATE KEY-----`n" + [System.Convert]::ToBase64String($keyBytes, [System.Base64FormattingOptions]::InsertLineBreaks) + "`n-----END RSA PRIVATE KEY-----"

# Write to file
[System.IO.File]::WriteAllText($keyPath, $keyPem)

Write-Host "Private key converted to PEM format: $keyPath"
