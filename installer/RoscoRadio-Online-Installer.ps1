param(
    [ValidateSet('stable','beta')]
    [string]$Channel = 'stable',
    [string]$InstallDir = "$env:LOCALAPPDATA\Programs\RoscoRadio",
    [switch]$NoLaunch
)

$ErrorActionPreference = 'Stop'
$ProgressPreference = 'SilentlyContinue'

$Server = 'https://nexusupdater.duckdns.org'
$AppId = 'rosco-radio'
$UserAgent = 'RoscoRadio-Online-Installer/0.1'
$ManifestUrl = "$Server/api/v1/apps/$AppId/manifest?channel=$Channel"

function Write-Step([string]$Text) {
    Write-Host "[Rosco Radio] $Text" -ForegroundColor Cyan
}

try {
    Write-Step "Contacting NexusUpdater ($Channel channel)..."
    $headers = @{ 'User-Agent' = $UserAgent }
    $manifest = Invoke-RestMethod -Uri $ManifestUrl -Headers $headers -Method Get

    if (-not $manifest.version -or -not $manifest.package_url -or -not $manifest.sha256) {
        throw 'NexusUpdater returned an incomplete manifest.'
    }

    $packageUri = [Uri]$manifest.package_url
    if ($packageUri.Scheme -ne 'https') {
        throw 'NexusUpdater returned a non-HTTPS package URL. Installation stopped.'
    }

    $version = [string]$manifest.version
    $expectedHash = ([string]$manifest.sha256).Trim().ToLowerInvariant()
    Write-Step "Latest $channel release: v$version"

    $updatesRoot = Join-Path ([Environment]::GetFolderPath('MyDocuments')) 'Rosco Radio\Updates'
    $downloadsDir = Join-Path $updatesRoot 'Downloads'
    $stagingDir = Join-Path $updatesRoot 'Staging\OnlineInstaller'
    $backupRoot = Join-Path $updatesRoot 'Backup'
    New-Item -ItemType Directory -Force -Path $downloadsDir,$stagingDir,$backupRoot | Out-Null

    $zipPath = Join-Path $downloadsDir "RoscoRadio-v$version.zip"
    $partialPath = "$zipPath.part"
    Remove-Item $partialPath -Force -ErrorAction SilentlyContinue

    Write-Step 'Downloading verified package...'
    Invoke-WebRequest -Uri $manifest.package_url -Headers $headers -OutFile $partialPath

    Write-Step 'Verifying SHA-256...'
    $actualHash = (Get-FileHash -Path $partialPath -Algorithm SHA256).Hash.ToLowerInvariant()
    if ($actualHash -ne $expectedHash) {
        Remove-Item $partialPath -Force -ErrorAction SilentlyContinue
        throw "Checksum mismatch. Expected $expectedHash but received $actualHash."
    }
    Move-Item -Force $partialPath $zipPath

    Remove-Item $stagingDir -Recurse -Force -ErrorAction SilentlyContinue
    New-Item -ItemType Directory -Force -Path $stagingDir | Out-Null
    Write-Step 'Extracting package...'
    Expand-Archive -Path $zipPath -DestinationPath $stagingDir -Force

    $children = @(Get-ChildItem -Path $stagingDir -Force)
    if ($children.Count -eq 1 -and $children[0].PSIsContainer) {
        $sourceDir = $children[0].FullName
    } else {
        $sourceDir = $stagingDir
    }

    if (Test-Path $InstallDir) {
        $stamp = Get-Date -Format 'yyyyMMdd-HHmmss'
        $backupDir = Join-Path $backupRoot "OnlineInstaller-$stamp"
        Write-Step "Backing up existing install to $backupDir"
        New-Item -ItemType Directory -Force -Path $backupDir | Out-Null
        Copy-Item -Path (Join-Path $InstallDir '*') -Destination $backupDir -Recurse -Force -ErrorAction SilentlyContinue
        Remove-Item $InstallDir -Recurse -Force
    }

    New-Item -ItemType Directory -Force -Path $InstallDir | Out-Null
    Copy-Item -Path (Join-Path $sourceDir '*') -Destination $InstallDir -Recurse -Force
    Remove-Item $stagingDir -Recurse -Force -ErrorAction SilentlyContinue

    $runBat = Join-Path $InstallDir 'run.bat'
    if (-not (Test-Path $runBat)) {
        throw 'Installation completed, but run.bat was not found in the package.'
    }

    try {
        $desktop = [Environment]::GetFolderPath('Desktop')
        $shortcutPath = Join-Path $desktop 'Rosco Radio.lnk'
        $shell = New-Object -ComObject WScript.Shell
        $shortcut = $shell.CreateShortcut($shortcutPath)
        $shortcut.TargetPath = $runBat
        $shortcut.WorkingDirectory = $InstallDir
        $shortcut.Description = "Rosco Radio v$version"
        $shortcut.Save()
    } catch {
        Write-Warning "Could not create desktop shortcut: $($_.Exception.Message)"
    }

    Write-Host ''
    Write-Host "Rosco Radio v$version installed successfully." -ForegroundColor Green
    Write-Host "Install folder: $InstallDir"
    Write-Host "Verified package: $zipPath"

    if (-not $NoLaunch) {
        Write-Step 'Launching Rosco Radio...'
        Start-Process -FilePath $runBat -WorkingDirectory $InstallDir
    }
    exit 0
}
catch {
    Write-Host ''
    Write-Host 'Rosco Radio installation failed.' -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    exit 1
}
