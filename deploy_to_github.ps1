# Enhanced ChuhaBot Swarm Framework - GitHub Deployment Script
# ================================================================

Write-Host "🚀 Enhanced ChuhaBot Swarm Framework Deployment" -ForegroundColor Cyan
Write-Host "=================================================" -ForegroundColor Cyan
Write-Host ""

# Check if GitHub CLI is installed
Write-Host "🔍 Checking GitHub CLI..." -ForegroundColor Yellow
try {
    $ghVersion = gh --version
    Write-Host "✅ GitHub CLI found: $($ghVersion[0])" -ForegroundColor Green
} catch {
    Write-Host "❌ GitHub CLI not found. Please install it first:" -ForegroundColor Red
    Write-Host "   winget install GitHub.cli" -ForegroundColor Gray
    Write-Host "   or download from: https://cli.github.com/" -ForegroundColor Gray
    exit 1
}

# Check if user is authenticated
Write-Host "🔐 Checking GitHub authentication..." -ForegroundColor Yellow
try {
    $authStatus = gh auth status 2>&1
    if ($authStatus -match "Logged in to github.com") {
        Write-Host "✅ GitHub authentication verified" -ForegroundColor Green
    } else {
        Write-Host "❌ Not authenticated. Please run: gh auth login" -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host "❌ Not authenticated. Please run: gh auth login" -ForegroundColor Red
    exit 1
}

# Get repository details
$reponame = Read-Host "Enter repository name (default: enhanced-chuhabot-swarm)"
if ([string]::IsNullOrWhiteSpace($reponame)) {
    $reponame = "enhanced-chuhabot-swarm"
}

$description = "Advanced modular swarm robotics framework with adaptive intelligence, C/Python implementations, and cross-platform support"

Write-Host ""
Write-Host "📋 Repository details:" -ForegroundColor Yellow
Write-Host "   Name: $reponame" -ForegroundColor Gray
Write-Host "   Description: $description" -ForegroundColor Gray
Write-Host "   Visibility: Public" -ForegroundColor Gray
$confirm = Read-Host "Continue? (Y/n)"

if ($confirm -ne "n" -and $confirm -ne "N") {
    Write-Host ""
    Write-Host "🔄 Removing old origin..." -ForegroundColor Green
    git remote remove origin 2>$null
    
    Write-Host "🏗️ Creating GitHub repository..." -ForegroundColor Green
    try {
        gh repo create $reponame --public --description $description --clone=false
        Write-Host "✅ Repository created successfully!" -ForegroundColor Green
    } catch {
        Write-Host "⚠️ Repository might already exist or there was an error" -ForegroundColor Yellow
        Write-Host "Continuing with deployment..." -ForegroundColor Gray
    }
    
    Write-Host "🔗 Adding new origin..." -ForegroundColor Green
    $username = gh api user --jq '.login'
    git remote add origin "https://github.com/$username/$reponame.git"
    
    Write-Host "📤 Pushing to GitHub..." -ForegroundColor Green
    git push -u origin master
    git push origin v2.0.0
    
    Write-Host ""
    Write-Host "✅ Deployment Complete!" -ForegroundColor Green
    Write-Host "=================================================" -ForegroundColor Cyan
    Write-Host "🌐 Repository URL: https://github.com/$username/$reponame" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "🏷️ Creating GitHub release..." -ForegroundColor Green
    try {
        gh release create v2.0.0 --title "Enhanced ChuhaBot Swarm Framework v2.0.0" --notes-file RELEASE_NOTES.md
        Write-Host "✅ Release v2.0.0 created successfully!" -ForegroundColor Green
    } catch {
        Write-Host "⚠️ Could not create release automatically" -ForegroundColor Yellow
        Write-Host "Please create it manually on GitHub" -ForegroundColor Gray
    }
    
    Write-Host ""
    Write-Host "📋 What's Next:" -ForegroundColor White
    Write-Host "1. Visit your repository: https://github.com/$username/$reponame" -ForegroundColor Gray
    Write-Host "2. Check the release: https://github.com/$username/$reponame/releases" -ForegroundColor Gray
    Write-Host "3. Star the repository and share with the community!" -ForegroundColor Gray
    Write-Host "4. Enable GitHub Pages for documentation (optional)" -ForegroundColor Gray
    Write-Host ""
    
    # Open repository in browser
    $openBrowser = Read-Host "Open repository in browser? (Y/n)"
    if ($openBrowser -ne "n" -and $openBrowser -ne "N") {
        gh repo view --web
    }
} else {
    Write-Host "Deployment cancelled." -ForegroundColor Red
}
