<#
Push project to GitHub with minimal steps.
Usage examples:
  .\push_to_github.ps1 -RemoteUrl "git@github.com:username/repo.git" -Branch main
  .\push_to_github.ps1 -RemoteUrl "https://github.com/username/repo.git" -Branch main

Notes:
- Requires `git` installed and available in PATH.
- You must have push access to the remote repository. For HTTPS, you may be prompted
  for credentials; for SSH, ensure your SSH key is configured.
- This script will only initialize a repo and push if the current folder is not
  already a git repo. If it is a git repo, it will add/commit latest changes and push.
#>
param(
    [Parameter(Mandatory=$true)] [string]$RemoteUrl,
    [string]$Branch = "main",
    [string]$CommitMessage = "Initial commit: add assignment 2 files"
)

function Check-Git {
    $git = Get-Command git -ErrorAction SilentlyContinue
    if (-not $git) {
        Write-Error "git not found. Please install Git and ensure it's in PATH: https://git-scm.com/downloads"
        exit 1
    }
}

Check-Git

# If not a git repo, initialize
if (-not (Test-Path .git)) {
    git init
    git checkout -b $Branch
    git add --all
    git commit -m "$CommitMessage"
    git remote add origin $RemoteUrl
    git push -u origin $Branch
    Write-Host "Repository initialized and pushed to $RemoteUrl"
} else {
    Write-Host "Existing git repo detected. Adding and committing changes."
    git add --all
    git commit -m "$CommitMessage" -q
    git push origin $Branch
    Write-Host "Changes pushed to $RemoteUrl (branch $Branch)"
}

Write-Host "Done."