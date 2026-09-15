# =====================================================================
#  Estatein -> GitHub + GitHub Pages
#  Запускать через deploy.bat (двойной клик) или:
#  powershell -NoProfile -ExecutionPolicy Bypass -File deploy.ps1
# =====================================================================

$RepoName = 'estatein-landing'
$Branch   = 'main'

function Say($text, $color = 'White') { Write-Host $text -ForegroundColor $color }
function Ok($text)   { Say "  [ok]  $text" 'Green' }
function Info($text) { Say "  ...   $text" 'Gray' }
function Warn($text) { Say "  [!]   $text" 'Yellow' }
function Fail($text) { Say "  [x]   $text" 'Red' }

Set-Location -LiteralPath $PSScriptRoot
Say ""
Say "=== Estatein -> GitHub ===" 'Cyan'
Say "Папка: $PSScriptRoot"
Say ""

# ---------- 1. git ----------
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Fail "Git не установлен."
    Say  "Поставь Git for Windows (настройки по умолчанию) и запусти скрипт снова:"
    Say  "  https://git-scm.com/download/win" 'Cyan'
    exit 1
}
$gitVersion = git --version
Ok "$gitVersion"

# ---------- 2. имя и почта для коммитов ----------
$userName = git config --get user.name 2>$null
if (-not $userName) {
    $userName = Read-Host "Имя для коммитов (например: Daniil)"
}
$userEmail = git config --get user.email 2>$null
if (-not $userEmail) {
    $userEmail = Read-Host "E-mail от GitHub-аккаунта"
}

# ---------- 3. репозиторий ----------
if (-not (Test-Path '.git')) {
    Info "Инициализирую репозиторий..."
    git init -q
    git branch -M $Branch
    Ok "git init"
} else {
    Ok "Репозиторий уже инициализирован"
}
git config user.name  "$userName"
git config user.email "$userEmail"

# ---------- 4. коммит ----------
git add -A
$staged = @(git diff --cached --name-only)
if ($staged.Count -gt 0) {
    git commit -q -m "Estatein: verstka po maketu (6 stranic, adaptiv, vanilla JS)"
    Ok "Коммит создан, файлов: $($staged.Count)"
} else {
    Info "Изменений нет — коммитить нечего"
}

# ---------- 5. GitHub CLI ----------
$gh = Get-Command gh -ErrorAction SilentlyContinue
if (-not $gh) {
    Say ""
    Warn "GitHub CLI (gh) не найден."
    Say ""
    Say "  Вариант А (проще всего) — поставить gh и запустить скрипт снова:" 'White'
    Say "      winget install --id GitHub.cli" 'Cyan'
    Say ""
    Say "  Вариант Б — вручную:" 'White'
    Say "      1) Создай пустой репозиторий: https://github.com/new" 'White'
    Say "         имя: $RepoName, Public, без README / .gitignore / лицензии" 'White'
    Say "      2) В этой папке выполни (подставь свой ник):" 'White'
    Say "         git remote add origin https://github.com/NICK/$RepoName.git" 'Cyan'
    Say "         git push -u origin $Branch" 'Cyan'
    Say "      3) Settings -> Pages -> Deploy from a branch -> $Branch / (root) -> Save" 'White'
    Say ""
    Say "  Сайт будет тут: https://NICK.github.io/$RepoName/" 'Green'
    exit 0
}
$ghVersion = (gh --version | Select-Object -First 1)
Ok "$ghVersion"

# ---------- 6. авторизация ----------
gh auth status *>$null
if ($LASTEXITCODE -ne 0) {
    Warn "Нужен вход в GitHub — откроется браузер, подтверди код."
    gh auth login --hostname github.com --git-protocol https --web
    if ($LASTEXITCODE -ne 0) { Fail "Вход не выполнен."; exit 1 }
}
$owner = (gh api user --jq .login).Trim()
Ok "Аккаунт: $owner"

# ---------- 7. репозиторий на GitHub ----------
$remotes = @(git remote)
if ($remotes -notcontains 'origin') {
    gh repo view "$owner/$RepoName" *>$null
    if ($LASTEXITCODE -eq 0) {
        Info "Репозиторий $owner/$RepoName уже существует — подключаю"
        git remote add origin "https://github.com/$owner/$RepoName.git"
        git push -u origin $Branch
    } else {
        Info "Создаю публичный репозиторий $owner/$RepoName..."
        gh repo create $RepoName --public --source=. --remote=origin --push --description "Verstka po maketu Estatein (Figma): 6 stranic, adaptiv, HTML/CSS/JS bez frameworkov"
    }
} else {
    Info "Пушу изменения..."
    git push -u origin $Branch
}
if ($LASTEXITCODE -ne 0) { Fail "Push не прошёл — смотри сообщение выше."; exit 1 }
Ok "Код залит: https://github.com/$owner/$RepoName"

# ---------- 8. GitHub Pages ----------
Info "Включаю GitHub Pages..."
$body = '{"source":{"branch":"' + $Branch + '","path":"/"}}'
$body | gh api --method POST "repos/$owner/$RepoName/pages" --input - *>$null
if ($LASTEXITCODE -ne 0) {
    Start-Sleep -Seconds 5
    $body | gh api --method POST "repos/$owner/$RepoName/pages" --input - *>$null
}
if ($LASTEXITCODE -ne 0) {
    $body | gh api --method PUT "repos/$owner/$RepoName/pages" --input - *>$null
}
$site = "https://$owner.github.io/$RepoName/"
if ($LASTEXITCODE -eq 0) {
    Ok "Pages включены"
} else {
    Warn "Через API не вышло. Включи руками: Settings -> Pages -> Deploy from a branch -> $Branch / (root)"
}

# ---------- 9. ссылка на демо в README ----------
$readme = Join-Path $PSScriptRoot 'README.md'
if (Test-Path $readme) {
    $text = Get-Content $readme -Raw -Encoding UTF8
    $new  = [regex]::Replace($text, '(?m)^.*\*\*Live demo:\*\*.*$', "🔗 **Live demo:** $site")
    if ($new -ne $text) {
        Set-Content $readme -Value $new -Encoding UTF8 -NoNewline
        git add README.md
        git commit -q -m "docs: live demo link"
        git push -q
        Ok "Ссылка на демо добавлена в README"
    }
}

# ---------- 10. описание и топики (для портфолио) ----------
gh repo edit "$owner/$RepoName" --homepage $site --add-topic html --add-topic css --add-topic javascript --add-topic responsive-design --add-topic figma --add-topic landing-page *>$null

Say ""
Say "==================================================" 'Cyan'
Say " Готово!" 'Green'
Say " Репозиторий: https://github.com/$owner/$RepoName" 'White'
Say " Сайт:        $site" 'Green'
Say ""
Say " Pages собираются 1-2 минуты после пуша." 'Gray'
Say " Прогресс: https://github.com/$owner/$RepoName/deployments" 'Gray'
Say "==================================================" 'Cyan'
Say ""
