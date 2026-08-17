[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"
$ProjectDir = $PSScriptRoot
Push-Location $ProjectDir

try {
    & git rev-parse --is-inside-work-tree *> $null
    if ($LASTEXITCODE -ne 0) {
        throw "Este diretório ainda não é um repositório Git."
    }

    $candidateFiles = @(
        & git ls-files --cached --others --exclude-standard
    )
    if ($LASTEXITCODE -ne 0) {
        throw "Não foi possível obter a lista de arquivos publicáveis."
    }

    $candidateFiles = @(
        $candidateFiles |
            Where-Object { $_ -and (Test-Path -LiteralPath $_ -PathType Leaf) } |
            Sort-Object -Unique
    )

    $problems = [System.Collections.Generic.List[string]]::new()
    $forbiddenExtensions = @(
        ".aac", ".aiff", ".avi", ".bin", ".ckpt", ".dll", ".exe", ".flac",
        ".gguf", ".key", ".m4a", ".mkv", ".mov", ".mp3", ".mp4", ".onnx",
        ".opus", ".p12", ".pem", ".pfx", ".pt", ".pth", ".pyd",
        ".safetensors", ".srt", ".vtt", ".wav", ".webm", ".wma", ".zip"
    )
    $sensitiveNamePattern = '(?i)(^|/)(\.env($|\.)|credentials[^/]*\.json$|service[-_]?account[^/]*\.json$|secrets?[^/]*\.json$)'
    $credentialPattern = '(?i)(api[_-]?key|client[_-]?secret|access[_-]?token|password|passwd|authorization)\s*[:=]\s*["''][^"'']{8,}'
    $tokenPattern = '(ghp_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|sk-[A-Za-z0-9_-]{20,}|xox[baprs]-[A-Za-z0-9-]{20,}|AIza[A-Za-z0-9_-]{20,})'
    $privateKeyPattern = 'BEGIN (RSA |OPENSSH |EC )?PRIVATE KEY'
    $localPathPattern = '(?i)([A-Z]:\\Users\\[^\\]+|/Users/[^/]+|/home/[^/]+)'
    $emailPattern = '(?i)\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b'
    $cpfPattern = '\b\d{3}\.\d{3}\.\d{3}-\d{2}\b'

    foreach ($relativePath in $candidateFiles) {
        $normalizedPath = $relativePath.Replace("\", "/")
        $extension = [IO.Path]::GetExtension($relativePath).ToLowerInvariant()
        $file = Get-Item -LiteralPath $relativePath

        if ($forbiddenExtensions -contains $extension) {
            $problems.Add("Tipo de arquivo proibido: $normalizedPath")
        }
        if ($normalizedPath -match $sensitiveNamePattern) {
            $problems.Add("Nome de arquivo sensível: $normalizedPath")
        }
        if ($file.Length -gt 5MB) {
            $problems.Add("Arquivo maior que 5 MB: $normalizedPath")
        }

        if ($normalizedPath -eq "auditar_publicacao.ps1") {
            continue
        }

        $content = Get-Content -LiteralPath $relativePath -Raw -ErrorAction SilentlyContinue
        if ($null -eq $content) {
            continue
        }
        if ($content -match $credentialPattern -or
            $content -match $tokenPattern -or
            $content -match $privateKeyPattern) {
            $problems.Add("Possível credencial no conteúdo: $normalizedPath")
        }
        if ($content -match $localPathPattern) {
            $problems.Add("Caminho pessoal absoluto no conteúdo: $normalizedPath")
        }
        if ($content -match $emailPattern -or $content -match $cpfPattern) {
            $problems.Add("Possível dado pessoal no conteúdo: $normalizedPath")
        }
    }

    Write-Host "Arquivos candidatos à publicação: $($candidateFiles.Count)"
    if ($problems.Count -gt 0) {
        Write-Host ""
        Write-Host "AUDITORIA REPROVADA" -ForegroundColor Red
        $problems | Sort-Object -Unique | ForEach-Object { Write-Host "- $_" }
        exit 1
    }

    Write-Host "AUDITORIA APROVADA: nenhum indicador crítico foi encontrado." -ForegroundColor Green
    Write-Host "Ainda é obrigatório revisar git diff --cached antes do push."
}
finally {
    Pop-Location
}
