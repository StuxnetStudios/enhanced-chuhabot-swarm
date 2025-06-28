# Enhanced ChuhaBot Swarm Framework - GitHub Deployment Script
# ================================================================

Write-Host "🚀 Enhanced ChuhaBot Swarm Framework Deployment" -ForegroundColor Cyan
Write-Host "=================================================" -ForegroundColor Cyan
Write-Host ""

# Get user input for repository details
$username = Read-Host "Enter your GitHub username"
$reponame = Read-Host "Enter your repository name (e.g., enhanced-chuhabot-swarm)"

Write-Host ""
Write-Host "📋 Repository URL will be: https://github.com/$username/$reponame" -ForegroundColor Yellow
$confirm = Read-Host "Continue? (y/N)"

if ($confirm -eq "y" -or $confirm -eq "Y") {
    Write-Host ""
    Write-Host "🔄 Removing old origin..." -ForegroundColor Green
    git remote remove origin
    
    Write-Host "🔗 Adding new origin..." -ForegroundColor Green
    git remote add origin "https://github.com/$username/$reponame.git"
    
    Write-Host "📤 Pushing to GitHub..." -ForegroundColor Green
    git push -u origin master
    git push origin v2.0.0
    
    Write-Host ""
    Write-Host "✅ Deployment Complete!" -ForegroundColor Green
    Write-Host "=================================================" -ForegroundColor Cyan
    Write-Host "🌐 Repository URL: https://github.com/$username/$reponame" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "📋 Next Steps:" -ForegroundColor White
    Write-Host "1. Visit your repository: https://github.com/$username/$reponame" -ForegroundColor Gray
    Write-Host "2. Go to Releases → Create new release" -ForegroundColor Gray
    Write-Host "3. Use tag: v2.0.0" -ForegroundColor Gray
    Write-Host "4. Copy release notes from RELEASE_NOTES.md" -ForegroundColor Gray
    Write-Host "5. Publish the release" -ForegroundColor Gray
    Write-Host ""
} else {
    Write-Host "Deployment cancelled." -ForegroundColor Red
}
