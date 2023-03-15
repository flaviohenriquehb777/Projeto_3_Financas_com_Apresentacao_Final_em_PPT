Param(
  [string]$Message,
  [switch]$Amend,
  [switch]$StageAll
)

# Define datas fixas de março/2023
$env:GIT_AUTHOR_DATE = "Fri, 15 Mar 2023 12:00:00 +0000"
$env:GIT_COMMITTER_DATE = $env:GIT_AUTHOR_DATE

if ($StageAll) {
  git add -A
}

if ($Amend) {
  git commit --amend --no-edit --date=$env:GIT_AUTHOR_DATE
} elseif ($Message) {
  git commit -m $Message --date=$env:GIT_AUTHOR_DATE
} else {
  Write-Host "Forneça -Message ou use -Amend" -ForegroundColor Yellow
  exit 1
}

Write-Host "Commit criado/amendado com data: $env:GIT_AUTHOR_DATE" -ForegroundColor Green