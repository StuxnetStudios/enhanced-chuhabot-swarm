# Enhanced ChuhaBot Swarm Framework - GitHub Update Script
# =========================================================

Write-Host "🔄 Updating GitHub Repository" -ForegroundColor Cyan
Write-Host "=============================" -ForegroundColor Cyan
Write-Host ""

# Check for uncommitted changes
$gitStatus = git status --porcelain
if ($gitStatus) {
    Write-Host "📝 Found changes to commit:" -ForegroundColor Yellow
    git status --short
    Write-Host ""
    
    # Stage all changes
    Write-Host "📦 Staging changes..." -ForegroundColor Green
    git add .
    
    # Get commit message
    $commitMessage = Read-Host "Enter commit message (or press Enter for auto-message)"
    if ([string]::IsNullOrWhiteSpace($commitMessage)) {
        $commitMessage = "docs: update README and project documentation"
    }
    
    # Commit changes
    Write-Host "💾 Committing changes..." -ForegroundColor Green
    git commit -m $commitMessage
    
    # Push to GitHub
    Write-Host "📤 Pushing to GitHub..." -ForegroundColor Green
    git push origin master
    
    Write-Host ""
    Write-Host "✅ GitHub repository updated successfully!" -ForegroundColor Green
    Write-Host "🌐 View at: https://github.com/StuxnetStudios/enhanced-chuhabot-swarm" -ForegroundColor Yellow
} else {
    Write-Host "✅ No changes to commit - repository is up to date!" -ForegroundColor Green
}

Write-Host ""
Write-Host "📊 Repository Statistics:" -ForegroundColor White
try {
    $repoInfo = gh repo view --json stargazerCount,forkCount,openIssues
    $repo = $repoInfo | ConvertFrom-Json
    Write-Host "⭐ Stars: $($repo.stargazerCount)" -ForegroundColor Gray
    Write-Host "🍴 Forks: $($repo.forkCount)" -ForegroundColor Gray
    Write-Host "🐛 Issues: $($repo.openIssues)" -ForegroundColor Gray
} catch {
    Write-Host "Unable to fetch repository statistics" -ForegroundColor Gray
}

Write-Host ""
$openRepo = Read-Host "Open repository in browser? (Y/n)"
if ($openRepo -ne "n" -and $openRepo -ne "N") {
    gh repo view --web
}
