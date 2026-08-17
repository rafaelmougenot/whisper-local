[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"
$ProjectDir = $PSScriptRoot
$ReleaseRoot = Join-Path $ProjectDir "releases"
$ReleaseDir = Join-Path $ReleaseRoot "WHISPER_LOCAL_PORTATIL"
$WorkDir = Join-Path $ProjectDir "build\pyinstaller"
$SpecDir = Join-Path $ProjectDir "build\spec"
$SourceFile = Join-Path $ProjectDir "src\transcrever.py"
$TemplateDir = Join-Path $ProjectDir "WHISPER_LOCAL_DISTRIBUICAO"

$PythonLauncher = Get-Command py -ErrorAction SilentlyContinue
$PythonArgs = @()

if ($PythonLauncher) {
    $PythonExe = $PythonLauncher.Source
    $PythonArgs = @("-3")
}
else {
    $PythonCommand = Get-Command python -ErrorAction SilentlyContinue
    if (-not $PythonCommand) {
        throw "Python 3 não encontrado. Instale o Python 3.11, 3.12 ou 3.13."
    }
    $PythonExe = $PythonCommand.Source
}

& $PythonExe @PythonArgs -c "import sys; raise SystemExit(0 if (3, 11) <= sys.version_info[:2] <= (3, 13) else 1)"
if ($LASTEXITCODE -ne 0) {
    throw "É necessário usar Python 3.11, 3.12 ou 3.13."
}

& $PythonExe @PythonArgs -m PyInstaller --version *> $null
if ($LASTEXITCODE -ne 0) {
    throw "PyInstaller ausente. Execute: python -m pip install --user -r requirements-build.txt"
}

if (Test-Path -LiteralPath $ReleaseDir) {
    throw "A release já existe: $ReleaseDir. Renomeie ou remova essa pasta antes de gerar outra."
}

New-Item -ItemType Directory -Path $ReleaseRoot -Force | Out-Null
New-Item -ItemType Directory -Path $WorkDir -Force | Out-Null
New-Item -ItemType Directory -Path $SpecDir -Force | Out-Null

& $PythonExe @PythonArgs -m PyInstaller `
    --noconfirm `
    --clean `
    --onedir `
    --console `
    --name "WHISPER_LOCAL_PORTATIL" `
    --distpath $ReleaseRoot `
    --workpath $WorkDir `
    --specpath $SpecDir `
    --collect-data faster_whisper `
    $SourceFile

if ($LASTEXITCODE -ne 0) {
    throw "A geração do executável falhou."
}

Copy-Item -LiteralPath (Join-Path $TemplateDir "Iniciar Whisper.bat") -Destination $ReleaseDir
Copy-Item -LiteralPath (Join-Path $TemplateDir "LEIA-ME.txt") -Destination $ReleaseDir
New-Item -ItemType Directory -Path (Join-Path $ReleaseDir "input") | Out-Null
New-Item -ItemType Directory -Path (Join-Path $ReleaseDir "output") | Out-Null

Write-Host ""
Write-Host "Distribuição criada em: $ReleaseDir"
Write-Host "O ZIP não foi criado automaticamente. Inspecione a pasta antes de compactar."
