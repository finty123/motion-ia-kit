# Instalador do kit Motion IA (skills do curso pro Claude Code e pro chat do Claude.ai)
# Uso normal: clique duas vezes em INSTALAR.cmd
# Opções:  -Sim            não faz perguntas (usa o config.json / padrões)
#          -SoSkills       só reaplica o config e copia as skills (não mexe em programas)
#          -ComBlender     também instala o Blender (só a skill do comercial 3D de lata usa)
param([switch]$Sim, [switch]$SoSkills, [switch]$ComBlender, [switch]$SoFerramentas)
if ($SoSkills -and $SoFerramentas) { throw 'Escolha apenas um dos modos de instalação.' }

$ErrorActionPreference = 'Stop'
try { [Console]::OutputEncoding = [Text.Encoding]::UTF8 } catch {}
$env:PYTHONUTF8 = '1'; $env:PYTHONIOENCODING = 'utf-8'
$KIT = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $KIT

function Titulo($t) { Write-Host ""; Write-Host "== $t" -ForegroundColor Cyan }
function Ok($t) { Write-Host "  [ok] $t" -ForegroundColor Green }
function Aviso($t) { Write-Host "  [!] $t" -ForegroundColor Yellow }
function Tem($c) { [bool](Get-Command $c -ErrorAction SilentlyContinue) }
function PythonCompativel {
    if (-not (Tem 'python')) { return $false }
    try {
        & python -c 'import sys; sys.exit(sys.version_info[:2] < (3, 10))' 2>$null
        return ($LASTEXITCODE -eq 0)
    } catch { return $false }
}
function RecarregarPath { $env:Path = [Environment]::GetEnvironmentVariable('Path', 'Machine') + ';' + [Environment]::GetEnvironmentVariable('Path', 'User') }
function Perguntar($texto, $padrao) {
    if ($Sim) { return $padrao }
    $r = Read-Host "$texto [$padrao]"
    if ([string]::IsNullOrWhiteSpace($r)) { return $padrao } else { return $r.Trim() }
}
function InstalarComWinget($id, $nome) {
    if (-not (Tem 'winget')) { Aviso "Sem winget. Instale $nome manualmente e rode de novo."; return }
    Write-Host "  instalando $nome ($id)..."
    winget.exe install -e --id $id --accept-source-agreements --accept-package-agreements
    RecarregarPath
}

Write-Host "Kit Motion IA - instalador" -ForegroundColor White
Write-Host "Pasta do kit: $KIT"

# ------------------------------------------------------------------ 1. programas
if (-not $SoSkills) {
    Titulo "1/6 Programas (Python, Node.js, FFmpeg)"
    RecarregarPath
    if (PythonCompativel) { Ok ("Python " + (python --version 2>&1)) } else { InstalarComWinget 'Python.Python.3.12' 'Python 3.12' }
    $nodeOk = $false
    if (Tem 'node') { $nv = (node -v); if ([int]($nv.TrimStart('v').Split('.')[0]) -ge 22) { $nodeOk = $true; Ok "Node.js $nv" } }
    if (-not $nodeOk) { InstalarComWinget 'OpenJS.NodeJS.LTS' 'Node.js LTS' }
    if (Tem 'ffmpeg') { Ok 'FFmpeg' } else { InstalarComWinget 'Gyan.FFmpeg' 'FFmpeg' }
    if ($ComBlender) {
        if (Test-Path "$env:ProgramFiles\Blender Foundation") { Ok 'Blender' } else { InstalarComWinget 'BlenderFoundation.Blender' 'Blender' }
    }
    if (-not (PythonCompativel)) {
        Aviso 'O comando python precisa abrir o Python 3.10 ou superior. Confira os aliases de execução de aplicativos do Windows e rode o instalador novamente.'
        exit 1
    }
    foreach ($c in 'node', 'npx.cmd', 'ffmpeg', 'ffprobe') {
        if (-not (Tem $c)) { Aviso "$c ainda não aparece. Feche e abra o terminal (ou o Claude) e rode o INSTALAR.cmd de novo."; exit 1 }
    }

    # -------------------------------------------------------------- 2. python
    Titulo "2/6 Bibliotecas Python + navegador do Playwright"
    python -m pip install --upgrade --quiet faster-whisper librosa soundfile scipy pillow playwright numpy opencv-python psutil pyloudnorm
    if ($LASTEXITCODE -ne 0) { throw 'Falha ao instalar as bibliotecas Python. Confira a mensagem do pip.' } else { Ok 'bibliotecas Python' }
    python -m playwright install chromium
    if ($LASTEXITCODE -ne 0) { throw 'Falha ao instalar o Chromium do Playwright.' }
    Ok 'Chromium do Playwright'

    # -------------------------------------------------------------- 3. hyperframes
    Titulo "3/6 HyperFrames (prévia e render das skills)"
    npx.cmd -y hyperframes browser ensure
    foreach ($v in '0.8.190', '0.8.210', '0.9.5') {
        npx.cmd -y "hyperframes@$v" --version *> $null
        if ($LASTEXITCODE -eq 0) { Ok "hyperframes@$v no cache" } else { Aviso "hyperframes@$v não baixou agora (baixa sozinho no primeiro uso)" }
    }
    Write-Host "  conferência (só importam Node, FFmpeg, FFprobe e Chrome; o resto é opcional e o curso não usa):"
    npx.cmd -y hyperframes doctor
}

if ($SoFerramentas) {
    Write-Host 'Crie o projeto com python ferramentas/novo_projeto.py CAMINHO_DA_NOVA_PASTA.'
    exit 0
}

# ------------------------------------------------------------------ 4. config
Titulo "4/6 Suas pastas e assinatura"
$cfgPath = Join-Path $KIT 'config.json'
$modelo = if (Test-Path -LiteralPath $cfgPath) { $cfgPath } else { Join-Path $KIT 'config.exemplo.json' }
$cfg = Get-Content -LiteralPath $modelo -Raw -Encoding UTF8 | ConvertFrom-Json
if (-not $cfg.pasta_projetos) {
    $videos = [Environment]::GetFolderPath([Environment+SpecialFolder]::MyVideos)
    if (-not $videos) { $videos = Join-Path $HOME 'Videos' }
    $cfg.pasta_projetos = Join-Path $videos 'Motion-Projetos'
}
$projetosAntes = $cfg.pasta_projetos
$cfg.pasta_projetos = Perguntar 'Pasta onde ficam os projetos de vídeo' $cfg.pasta_projetos
if (-not $cfg.pasta_resultados -or $cfg.pasta_resultados -eq (Join-Path $projetosAntes 'resultados')) {
    $cfg.pasta_resultados = Join-Path $cfg.pasta_projetos 'resultados'
}
$cfg.pasta_resultados = Perguntar 'Pasta dos vídeos prontos' $cfg.pasta_resultados
$cfg.assinatura = Perguntar 'Seu @ pra assinar os vídeos (Enter = perguntar em cada vídeo)' $cfg.assinatura
$json = $cfg | ConvertTo-Json -Depth 5
[IO.File]::WriteAllText($cfgPath, $json, (New-Object Text.UTF8Encoding($false)))
foreach ($p in $cfg.pasta_projetos, $cfg.pasta_resultados) { New-Item -ItemType Directory -Force -Path $p | Out-Null }
$launch = Join-Path $cfg.pasta_projetos '.claude\launch.json'
if (-not (Test-Path $launch)) {
    New-Item -ItemType Directory -Force -Path (Split-Path $launch) | Out-Null
    [IO.File]::WriteAllText($launch, "{`n  `"version`": `"0.0.1`",`n  `"configurations`": []`n}`n", (New-Object Text.UTF8Encoding($false)))
}
Ok "projetos: $($cfg.pasta_projetos)"
Ok "resultados: $($cfg.pasta_resultados)"

# ------------------------------------------------------------------ 5. skills
Titulo "5/6 Adaptando e instalando as skills"
python ferramentas/trazer_aprendizados.py
if ($LASTEXITCODE -ne 0) { throw 'Falha ao preservar as correções locais.' }
python ferramentas/adaptar.py
if ($LASTEXITCODE -ne 0) { Aviso 'adaptar.py falhou'; exit 1 }
$claudeDir = if ($env:CLAUDE_CONFIG_DIR) { $env:CLAUDE_CONFIG_DIR } else { Join-Path $HOME '.claude' }
$destino = Join-Path $claudeDir 'skills'
$antigas = Join-Path $claudeDir 'skills-antigas'
New-Item -ItemType Directory -Force -Path $destino | Out-Null
$stamp = Get-Date -Format 'yyyyMMdd-HHmmss-fff'
Get-ChildItem (Join-Path $KIT 'skills') -Directory | ForEach-Object {
    $alvo = Join-Path $destino $_.Name
    if (Test-Path $alvo) {
        New-Item -ItemType Directory -Force -Path $antigas | Out-Null
        Move-Item $alvo (Join-Path $antigas "$($_.Name)-$stamp")
        Write-Host "  versão anterior guardada em skills-antigas\$($_.Name)-$stamp"
    }
    Copy-Item $_.FullName $alvo -Recurse
    Ok $_.Name
}
python ferramentas/empacotar_chat.py
if ($LASTEXITCODE -ne 0) { throw 'Falha ao preparar os ZIPs.' }

# ------------------------------------------------------------------ 6. conferência
Titulo "6/6 Conferência final"
python ferramentas/verificar.py
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host ""
Write-Host "Feche e abra o Claude Code uma vez pra ele carregar as skills novas." -ForegroundColor White
Write-Host "Pra usar no chat do Claude.ai: suba os zips da pasta 'chat' em Personalizar > Habilidades." -ForegroundColor White
Write-Host "Passo a passo completo: docs\01-tutorial-passo-a-passo.md" -ForegroundColor White
