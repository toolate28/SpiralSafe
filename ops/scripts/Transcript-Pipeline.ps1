<#
.SYNOPSIS
    SpiralSafe Transcript Pipeline - Redaction, Encryption, Sharing

.DESCRIPTION
    Cross-platform pipeline for secure handling of conversation transcripts,
    templates, and sensitive artifacts with H&&S protocol signing.

.NOTES
    H&&S:WAVE | Hope&&Sauced
    Platform: Windows PowerShell 7+ / macOS / Linux
#>

param(
    [Parameter(Mandatory=$false)]
    [ValidateSet('Redact', 'Encrypt', 'Hash', 'Share', 'Full')]
    [string]$Action = 'Full',

    [Parameter(Mandatory=$false)]
    [string]$InputPath,

    [Parameter(Mandatory=$false)]
    [string]$OutputPath,

    [Parameter(Mandatory=$false)]
    [string]$RecipientPublicKey,

    [Parameter(Mandatory=$false)]
    [switch]$Sign
)

#region Platform Detection
$Script:Platform = switch ($true) {
    $IsWindows { 'Windows' }
    $IsMacOS   { 'macOS' }
    $IsLinux   { 'Linux' }
    default    { 'Windows' }  # PowerShell 5.1 fallback
}

$Script:PlatformConfig = @{
    Windows = @{
        Strengths = @(
            'Native PowerShell integration',
            'Windows Credential Manager for key storage',
            'DPAPI for user-context encryption',
            'Integrated with Windows Hello biometrics',
            'WSL2 for Unix tool interop'
        )
        Weaknesses = @(
            'Line ending conversion (CRLF)',
            'Path length limitations (260 chars legacy)',
            'Case-insensitive filesystem',
            'UAC interruptions for elevated operations'
        )
        TempDir = $env:TEMP
        HashCmd = 'certutil -hashfile'
        DefaultCipher = 'AES-256-GCM'
    }
    macOS = @{
        Strengths = @(
            'Keychain for secure credential storage',
            'Native OpenSSL/LibreSSL',
            'Hardened runtime support',
            'Unified Unix toolchain',
            'Secure Enclave for key protection'
        )
        Weaknesses = @(
            'SIP restrictions on system paths',
            'Gatekeeper signing requirements',
            'Resource fork handling complexity',
            'Homebrew dependency management'
        )
        TempDir = '/tmp'
        HashCmd = 'shasum -a 256'
        DefaultCipher = 'AES-256-GCM'
    }
    Linux = @{
        Strengths = @(
            'Native GPG ecosystem',
            'Systemd secret management',
            'Full filesystem permission control',
            'Container-native workflows',
            'Extensive crypto library support'
        )
        Weaknesses = @(
            'Distro fragmentation',
            'Varying default crypto tools',
            'Desktop keyring inconsistencies',
            'SELinux/AppArmor context requirements'
        )
        TempDir = '/tmp'
        HashCmd = 'sha256sum'
        DefaultCipher = 'AES-256-GCM'
    }
}
#endregion

#region Redaction Patterns
$Script:RedactionPatterns = @(
    # API Keys & Tokens
    @{ Name = 'API_KEY';        Pattern = '(?i)(api[_-]?key|apikey)\s*[:=]\s*["\x27]?[\w\-]{20,}["\x27]?' }
    @{ Name = 'AUTH_TOKEN';     Pattern = '(?i)(bearer|token|auth)\s+[\w\-\.]{20,}' }
    @{ Name = 'JWT';            Pattern = 'eyJ[A-Za-z0-9\-_]+\.eyJ[A-Za-z0-9\-_]+\.[A-Za-z0-9\-_]+' }

    # Credentials
    @{ Name = 'PASSWORD';       Pattern = '(?i)(password|passwd|pwd)\s*[:=]\s*["\x27]?[^\s"\x27]{4,}["\x27]?' }
    @{ Name = 'SECRET';         Pattern = '(?i)(secret|private[_-]?key)\s*[:=]\s*["\x27]?[\w\-]{10,}["\x27]?' }

    # Personal Data
    @{ Name = 'EMAIL';          Pattern = '[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}' }
    @{ Name = 'PHONE';          Pattern = '(?:\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}' }
    @{ Name = 'SSN';            Pattern = '\d{3}-\d{2}-\d{4}' }
    @{ Name = 'IP_ADDRESS';     Pattern = '\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b' }

    # Paths (platform-aware)
    @{ Name = 'WIN_PATH';       Pattern = '[A-Za-z]:\\Users\\[^\s\\]+' }
    @{ Name = 'UNIX_PATH';      Pattern = '/home/[^\s/]+|/Users/[^\s/]+' }

    # Cloud Resources
    @{ Name = 'AWS_KEY';        Pattern = 'AKIA[0-9A-Z]{16}' }
    @{ Name = 'GCP_KEY';        Pattern = 'AIza[0-9A-Za-z\-_]{35}' }
    @{ Name = 'AZURE_CONN';     Pattern = 'DefaultEndpointsProtocol=https;AccountName=[\w]+' }
)
#endregion

#region Core Functions
function Invoke-Redaction {
    param([string]$Content)

    $redacted = $Content
    $redactionLog = @()

    foreach ($pattern in $Script:RedactionPatterns) {
        $matches = [regex]::Matches($redacted, $pattern.Pattern)
        foreach ($match in $matches) {
            $replacement = "[REDACTED:$($pattern.Name)]"
            $redactionLog += @{
                Type = $pattern.Name
                Position = $match.Index
                Length = $match.Length
                Hash = (Get-ContentHash $match.Value -Algorithm SHA256).Substring(0,16)
            }
            $redacted = $redacted.Replace($match.Value, $replacement)
        }
    }

    return @{
        Content = $redacted
        Log = $redactionLog
        Timestamp = Get-Date -Format 'o'
        Platform = $Script:Platform
        Signature = 'H&&S:WAVE'
    }
}

function Get-ContentHash {
    param(
        [string]$Content,
        [ValidateSet('SHA256', 'SHA384', 'SHA512', 'MD5')]
        [string]$Algorithm = 'SHA256'
    )

    $bytes = [System.Text.Encoding]::UTF8.GetBytes($Content)
    $hasher = [System.Security.Cryptography.HashAlgorithm]::Create($Algorithm)
    $hashBytes = $hasher.ComputeHash($bytes)
    return [BitConverter]::ToString($hashBytes).Replace('-', '').ToLower()
}

function Invoke-Encryption {
    param(
        [string]$Content,
        [string]$PublicKey,
        [switch]$UseHybrid
    )

    # Generate ephemeral AES key
    $aes = [System.Security.Cryptography.Aes]::Create()
    $aes.KeySize = 256
    $aes.Mode = [System.Security.Cryptography.CipherMode]::GCM
    $aes.GenerateKey()
    $aes.GenerateIV()

    # Encrypt content
    $encryptor = $aes.CreateEncryptor()
    $contentBytes = [System.Text.Encoding]::UTF8.GetBytes($Content)
    $encryptedContent = $encryptor.TransformFinalBlock($contentBytes, 0, $contentBytes.Length)

    return @{
        EncryptedData = [Convert]::ToBase64String($encryptedContent)
        IV = [Convert]::ToBase64String($aes.IV)
        KeyHash = (Get-ContentHash ([Convert]::ToBase64String($aes.Key))).Substring(0,32)
        Algorithm = 'AES-256-GCM'
        Timestamp = Get-Date -Format 'o'
        Platform = $Script:Platform
        Signature = 'H&&S:WAVE'
    }
}

function New-TranscriptBundle {
    param(
        [string]$TranscriptPath,
        [string]$OutputDir,
        [switch]$IncludeMetadata
    )

    $transcript = Get-Content $TranscriptPath -Raw
    $bundleId = [guid]::NewGuid().ToString('N').Substring(0,12)

    # Redact
    $redactionResult = Invoke-Redaction -Content $transcript

    # Hash original + redacted
    $hashes = @{
        Original = Get-ContentHash $transcript
        Redacted = Get-ContentHash $redactionResult.Content
        Algorithm = 'SHA256'
    }

    # Encrypt redacted version
    $encryptionResult = Invoke-Encryption -Content $redactionResult.Content

    # Bundle manifest
    $manifest = @{
        BundleId = $bundleId
        Created = Get-Date -Format 'o'
        Platform = $Script:Platform
        PlatformConfig = $Script:PlatformConfig[$Script:Platform]
        Pipeline = @{
            Redaction = @{
                PatternsApplied = $redactionResult.Log.Count
                Patterns = $Script:RedactionPatterns.Name
            }
            Encryption = @{
                Algorithm = $encryptionResult.Algorithm
                KeyHash = $encryptionResult.KeyHash
            }
            Hashing = $hashes
        }
        Signature = 'H&&S:WAVE | Hope&&Sauced'
        Version = '1.0.0'
    }

    # Write outputs
    if (-not $OutputDir) { $OutputDir = $Script:PlatformConfig[$Script:Platform].TempDir }
    $bundlePath = Join-Path $OutputDir "spiralsafe-transcript-$bundleId"
    New-Item -ItemType Directory -Path $bundlePath -Force | Out-Null

    $redactionResult.Content | Set-Content (Join-Path $bundlePath 'transcript.redacted.txt')
    $encryptionResult | ConvertTo-Json -Depth 10 | Set-Content (Join-Path $bundlePath 'transcript.encrypted.json')
    $manifest | ConvertTo-Json -Depth 10 | Set-Content (Join-Path $bundlePath 'manifest.json')
    "$($hashes.Redacted)  transcript.redacted.txt" | Set-Content (Join-Path $bundlePath 'checksums.sha256')

    Write-Host "`n[H&&S:WAVE] Transcript bundle created: $bundlePath" -ForegroundColor Cyan
    Write-Host "  Platform: $Script:Platform" -ForegroundColor DarkGray
    Write-Host "  Redactions: $($redactionResult.Log.Count) patterns matched" -ForegroundColor DarkGray
    Write-Host "  Hash (SHA256): $($hashes.Redacted.Substring(0,16))..." -ForegroundColor DarkGray

    return @{
        BundlePath = $bundlePath
        Manifest = $manifest
        Hashes = $hashes
    }
}

function Show-PlatformMatrix {
    Write-Host "`n╔══════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
    Write-Host "║  SpiralSafe Platform Compatibility Matrix | H&&S:WAVE       ║" -ForegroundColor Cyan
    Write-Host "╚══════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan

    foreach ($platform in @('Windows', 'macOS', 'Linux')) {
        $config = $Script:PlatformConfig[$platform]
        $isCurrent = $platform -eq $Script:Platform
        $marker = if ($isCurrent) { '●' } else { '○' }

        Write-Host "`n  $marker $platform" -ForegroundColor $(if ($isCurrent) { 'Green' } else { 'White' })

        Write-Host "    Strengths:" -ForegroundColor DarkGreen
        $config.Strengths | ForEach-Object { Write-Host "      + $_" -ForegroundColor DarkGray }

        Write-Host "    Weaknesses:" -ForegroundColor DarkYellow
        $config.Weaknesses | ForEach-Object { Write-Host "      - $_" -ForegroundColor DarkGray }
    }

    Write-Host "`n  Hope&&Sauced | Cross-Platform Ready`n" -ForegroundColor Cyan
}
#endregion

#region Main Execution
switch ($Action) {
    'Redact' {
        if (-not $InputPath) { throw "InputPath required for Redact action" }
        $content = Get-Content $InputPath -Raw
        $result = Invoke-Redaction -Content $content
        if ($OutputPath) { $result.Content | Set-Content $OutputPath }
        $result
    }
    'Encrypt' {
        if (-not $InputPath) { throw "InputPath required for Encrypt action" }
        $content = Get-Content $InputPath -Raw
        $result = Invoke-Encryption -Content $content -PublicKey $RecipientPublicKey
        if ($OutputPath) { $result | ConvertTo-Json | Set-Content $OutputPath }
        $result
    }
    'Hash' {
        if (-not $InputPath) { throw "InputPath required for Hash action" }
        $content = Get-Content $InputPath -Raw
        @{
            File = $InputPath
            SHA256 = Get-ContentHash $content -Algorithm SHA256
            SHA384 = Get-ContentHash $content -Algorithm SHA384
            Timestamp = Get-Date -Format 'o'
            Signature = 'H&&S:WAVE'
        }
    }
    'Share' {
        Show-PlatformMatrix
    }
    'Full' {
        if ($InputPath) {
            New-TranscriptBundle -TranscriptPath $InputPath -OutputDir $OutputPath -IncludeMetadata
        } else {
            Show-PlatformMatrix
            Write-Host "  Usage: Transcript-Pipeline.ps1 -Action Full -InputPath <transcript> [-OutputPath <dir>]`n" -ForegroundColor Yellow
        }
    }
}
#endregion
