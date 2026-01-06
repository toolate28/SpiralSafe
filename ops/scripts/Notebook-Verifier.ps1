<#
.SYNOPSIS
    SpiralSafe Notebook Verification & Registry

.DESCRIPTION
    Cross-platform Jupyter notebook (.ipynb) verification pipeline
    with Merkle tree hashing, signature generation, and registry integration.

.NOTES
    H&&S:WAVE | Hope&&Sauced
    Part of SpiralSafe Multi-Architecture Deployment
#>

param(
    [Parameter(Mandatory=$false)]
    [string]$NotebookPath,

    [Parameter(Mandatory=$false)]
    [ValidateSet('Verify', 'Hash', 'Register', 'List', 'Export')]
    [string]$Action = 'Verify',

    [Parameter(Mandatory=$false)]
    [string]$OutputPath,

    [Parameter(Mandatory=$false)]
    [string]$RegistryPath,

    [Parameter(Mandatory=$false)]
    [switch]$Recursive
)

#region Platform & Environment Detection
$Script:Platform = switch ($true) {
    $IsWindows { 'Windows' }
    $IsMacOS   { 'macOS' }
    $IsLinux   { 'Linux' }
    default    { 'Windows' }
}

$Script:Environment = @{
    Platform = $Script:Platform
    Shell = $PSVersionTable.PSEdition
    PSVersion = $PSVersionTable.PSVersion.ToString()
    AI = $env:SPIRALSAFE_AI_PLATFORM ?? 'claude-code'
    IDE = $env:SPIRALSAFE_IDE ?? 'vscode'
}

$Script:RegistryFile = $RegistryPath ?? (Join-Path $env:USERPROFILE '.spiralsafe' 'notebook-registry.json')
#endregion

#region Cryptographic Functions
function Get-SHA256 {
    param([string]$Content)
    $bytes = [System.Text.Encoding]::UTF8.GetBytes($Content)
    $hasher = [System.Security.Cryptography.SHA256]::Create()
    $hashBytes = $hasher.ComputeHash($bytes)
    return [BitConverter]::ToString($hashBytes).Replace('-', '').ToLower()
}

function Get-MerkleRoot {
    param([string[]]$Hashes)

    if ($Hashes.Count -eq 0) { return $null }
    if ($Hashes.Count -eq 1) { return $Hashes[0] }

    $currentLevel = $Hashes

    while ($currentLevel.Count -gt 1) {
        $nextLevel = @()
        for ($i = 0; $i -lt $currentLevel.Count; $i += 2) {
            if ($i + 1 -lt $currentLevel.Count) {
                $combined = $currentLevel[$i] + $currentLevel[$i + 1]
                $nextLevel += Get-SHA256 -Content $combined
            } else {
                # Odd number - hash with itself
                $combined = $currentLevel[$i] + $currentLevel[$i]
                $nextLevel += Get-SHA256 -Content $combined
            }
        }
        $currentLevel = $nextLevel
    }

    return $currentLevel[0]
}
#endregion

#region Notebook Parsing
function Read-Notebook {
    param([string]$Path)

    if (-not (Test-Path $Path)) {
        throw "Notebook not found: $Path"
    }

    $raw = Get-Content $Path -Raw
    $notebook = $raw | ConvertFrom-Json

    $cells = @()
    $index = 0

    foreach ($cell in $notebook.cells) {
        $source = if ($cell.source -is [array]) {
            $cell.source -join ''
        } else {
            $cell.source
        }

        $outputHash = $null
        if ($cell.outputs -and $cell.outputs.Count -gt 0) {
            $outputJson = $cell.outputs | ConvertTo-Json -Depth 10 -Compress
            $outputHash = Get-SHA256 -Content $outputJson
        }

        $cellData = @{
            Index = $index
            Type = $cell.cell_type
            Source = $source
            SourceHash = Get-SHA256 -Content $source
            OutputHash = $outputHash
            Metadata = $cell.metadata
        }

        # Combined cell hash
        $cellJson = $cellData | ConvertTo-Json -Depth 5 -Compress
        $cellData.CellHash = Get-SHA256 -Content $cellJson

        $cells += $cellData
        $index++
    }

    return @{
        Path = $Path
        FileName = Split-Path $Path -Leaf
        KernelSpec = $notebook.metadata.kernelspec
        Language = $notebook.metadata.language_info
        CellCount = $cells.Count
        Cells = $cells
        CellHashes = $cells | ForEach-Object { $_.CellHash }
        Metadata = $notebook.metadata
    }
}
#endregion

#region Verification Functions
function New-NotebookSignature {
    param([hashtable]$NotebookData)

    $cellHashes = $NotebookData.CellHashes
    $merkleRoot = Get-MerkleRoot -Hashes $cellHashes

    $signature = @{
        Id = [guid]::NewGuid().ToString('N').Substring(0,16)
        NotebookPath = $NotebookData.Path
        FileName = $NotebookData.FileName
        CellCount = $NotebookData.CellCount
        MerkleRoot = $merkleRoot
        CellHashes = $cellHashes
        Environment = $Script:Environment
        Timestamp = Get-Date -Format 'o'
        Protocol = 'H&&S:WAVE'
        Signature = "Hope&&Sauced"
        Version = '1.0.0'
    }

    # Sign the signature itself
    $signatureJson = $signature | ConvertTo-Json -Depth 10 -Compress
    $signature.IntegrityHash = Get-SHA256 -Content $signatureJson

    return $signature
}

function Test-NotebookSignature {
    param(
        [hashtable]$Signature,
        [hashtable]$NotebookData
    )

    $currentMerkle = Get-MerkleRoot -Hashes $NotebookData.CellHashes

    $result = @{
        Valid = $currentMerkle -eq $Signature.MerkleRoot
        ExpectedMerkle = $Signature.MerkleRoot
        ActualMerkle = $currentMerkle
        CellCountMatch = $NotebookData.CellCount -eq $Signature.CellCount
        ChangedCells = @()
    }

    # Find changed cells
    for ($i = 0; $i -lt [Math]::Max($NotebookData.CellHashes.Count, $Signature.CellHashes.Count); $i++) {
        $current = if ($i -lt $NotebookData.CellHashes.Count) { $NotebookData.CellHashes[$i] } else { $null }
        $expected = if ($i -lt $Signature.CellHashes.Count) { $Signature.CellHashes[$i] } else { $null }

        if ($current -ne $expected) {
            $result.ChangedCells += @{
                Index = $i
                Status = if ($null -eq $current) { 'Deleted' } elseif ($null -eq $expected) { 'Added' } else { 'Modified' }
            }
        }
    }

    return $result
}
#endregion

#region Registry Functions
function Initialize-Registry {
    $registryDir = Split-Path $Script:RegistryFile -Parent
    if (-not (Test-Path $registryDir)) {
        New-Item -ItemType Directory -Path $registryDir -Force | Out-Null
    }

    if (-not (Test-Path $Script:RegistryFile)) {
        @{
            Version = '1.0.0'
            Protocol = 'H&&S:WAVE'
            Created = Get-Date -Format 'o'
            Entries = @{}
        } | ConvertTo-Json -Depth 10 | Set-Content $Script:RegistryFile
    }

    return Get-Content $Script:RegistryFile -Raw | ConvertFrom-Json
}

function Add-ToRegistry {
    param([hashtable]$Signature)

    $registry = Initialize-Registry

    $entries = @{}
    if ($registry.Entries) {
        $registry.Entries.PSObject.Properties | ForEach-Object {
            $entries[$_.Name] = $_.Value
        }
    }

    $entries[$Signature.Id] = $Signature
    $registry.Entries = $entries
    $registry.Updated = Get-Date -Format 'o'

    $registry | ConvertTo-Json -Depth 10 | Set-Content $Script:RegistryFile

    return $Signature.Id
}

function Get-RegistryEntries {
    $registry = Initialize-Registry
    return $registry.Entries
}
#endregion

#region Output Functions
function Write-VerificationReport {
    param(
        [hashtable]$Signature,
        [hashtable]$VerificationResult
    )

    $status = if ($VerificationResult.Valid) { '✓ VERIFIED' } else { '✗ MODIFIED' }
    $color = if ($VerificationResult.Valid) { 'Green' } else { 'Red' }

    Write-Host "`n╔══════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
    Write-Host "║  SpiralSafe Notebook Verification | H&&S:WAVE               ║" -ForegroundColor Cyan
    Write-Host "╚══════════════════════════════════════════════════════════════╝`n" -ForegroundColor Cyan

    Write-Host "  Notebook: $($Signature.FileName)" -ForegroundColor White
    Write-Host "  Status:   $status" -ForegroundColor $color
    Write-Host "  Cells:    $($Signature.CellCount)" -ForegroundColor DarkGray
    Write-Host "  Merkle:   $($Signature.MerkleRoot.Substring(0,32))..." -ForegroundColor DarkGray

    if ($VerificationResult.ChangedCells.Count -gt 0) {
        Write-Host "`n  Changes detected:" -ForegroundColor Yellow
        foreach ($change in $VerificationResult.ChangedCells) {
            Write-Host "    Cell $($change.Index): $($change.Status)" -ForegroundColor Yellow
        }
    }

    Write-Host "`n  Platform: $($Script:Platform) | $($Script:Environment.Shell)" -ForegroundColor DarkGray
    Write-Host "  Hope&&Sauced`n" -ForegroundColor Cyan
}
#endregion

#region Main Execution
switch ($Action) {
    'Verify' {
        if (-not $NotebookPath) { throw "NotebookPath required for Verify" }

        $notebook = Read-Notebook -Path $NotebookPath
        $signature = New-NotebookSignature -NotebookData $notebook

        # Check if already in registry
        $registry = Initialize-Registry
        $existingId = $null
        if ($registry.Entries) {
            $registry.Entries.PSObject.Properties | ForEach-Object {
                if ($_.Value.FileName -eq $signature.FileName) {
                    $existingId = $_.Name
                }
            }
        }

        if ($existingId) {
            $existing = $registry.Entries.$existingId
            $existingHash = @{
                MerkleRoot = $existing.MerkleRoot
                CellCount = $existing.CellCount
                CellHashes = $existing.CellHashes
            }
            $result = Test-NotebookSignature -Signature $existingHash -NotebookData $notebook
            Write-VerificationReport -Signature $signature -VerificationResult $result
        } else {
            Write-Host "`n[H&&S:WAVE] Notebook not in registry. Use -Action Register to add.`n" -ForegroundColor Yellow
            $result = @{ Valid = $true; ChangedCells = @() }
            Write-VerificationReport -Signature $signature -VerificationResult $result
        }

        return $signature
    }

    'Hash' {
        if (-not $NotebookPath) { throw "NotebookPath required for Hash" }

        $notebook = Read-Notebook -Path $NotebookPath
        $merkle = Get-MerkleRoot -Hashes $notebook.CellHashes

        @{
            Notebook = $NotebookPath
            CellCount = $notebook.CellCount
            MerkleRoot = $merkle
            CellHashes = $notebook.CellHashes
            Protocol = 'H&&S:WAVE'
            Timestamp = Get-Date -Format 'o'
        }
    }

    'Register' {
        if (-not $NotebookPath) { throw "NotebookPath required for Register" }

        $notebook = Read-Notebook -Path $NotebookPath
        $signature = New-NotebookSignature -NotebookData $notebook
        $id = Add-ToRegistry -Signature $signature

        Write-Host "`n[H&&S:WAVE] Notebook registered" -ForegroundColor Cyan
        Write-Host "  ID:       $id" -ForegroundColor White
        Write-Host "  Notebook: $($signature.FileName)" -ForegroundColor DarkGray
        Write-Host "  Merkle:   $($signature.MerkleRoot.Substring(0,32))..." -ForegroundColor DarkGray
        Write-Host "  Registry: $Script:RegistryFile" -ForegroundColor DarkGray
        Write-Host "`n  Hope&&Sauced`n" -ForegroundColor Cyan

        return $signature
    }

    'List' {
        $entries = Get-RegistryEntries

        Write-Host "`n╔══════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
        Write-Host "║  SpiralSafe Notebook Registry | H&&S:WAVE                   ║" -ForegroundColor Cyan
        Write-Host "╚══════════════════════════════════════════════════════════════╝`n" -ForegroundColor Cyan

        if ($entries) {
            $entries.PSObject.Properties | ForEach-Object {
                $entry = $_.Value
                Write-Host "  [$($_.Name.Substring(0,8))] $($entry.FileName)" -ForegroundColor White
                Write-Host "           Cells: $($entry.CellCount) | $($entry.Timestamp)" -ForegroundColor DarkGray
            }
        } else {
            Write-Host "  No notebooks registered yet." -ForegroundColor Yellow
        }

        Write-Host "`n  Hope&&Sauced`n" -ForegroundColor Cyan
    }

    'Export' {
        $registry = Initialize-Registry

        $export = @{
            ExportDate = Get-Date -Format 'o'
            Platform = $Script:Platform
            Environment = $Script:Environment
            Protocol = 'H&&S:WAVE'
            Registry = $registry
        }

        if ($OutputPath) {
            $export | ConvertTo-Json -Depth 20 | Set-Content $OutputPath
            Write-Host "[H&&S:WAVE] Registry exported to: $OutputPath" -ForegroundColor Cyan
        }

        return $export
    }
}
#endregion
