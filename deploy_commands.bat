@echo off
echo ========================================
echo Enhanced ChuhaBot Swarm Framework
echo GitHub Deployment Commands
echo ========================================
echo.

echo Step 1: Remove old origin
git remote remove origin

echo.
echo Step 2: Add your new repository origin
echo Replace YOUR_USERNAME and REPO_NAME with your values:
echo git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git
echo.
pause

echo Step 3: Push to your new repository
git push -u origin master
git push origin v2.0.0

echo.
echo ========================================
echo Deployment Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Go to your GitHub repository
echo 2. Create a release using tag v2.0.0
echo 3. Copy content from RELEASE_NOTES.md
echo 4. Publish the release
echo.
pause
