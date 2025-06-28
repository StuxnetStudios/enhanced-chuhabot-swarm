# Simple PowerShell Build Script for ChuhaBot C Controller
param([string]$Action = "help")

$ControllerName = "chuha_c_controller"
$SourceFile = "$ControllerName.c"
$OutputFile = "$ControllerName.exe"

function Show-Help {
    Write-Host "ChuhaBot C Controller Build System" -ForegroundColor Yellow
    Write-Host "Available commands:" -ForegroundColor White
    Write-Host "  check  - Check build requirements" -ForegroundColor Green
    Write-Host "  info   - Show build information" -ForegroundColor Green
    Write-Host "  help   - Show this help" -ForegroundColor Green
}

function Test-Requirements {
    Write-Host "Checking build requirements..." -ForegroundColor Cyan
    
    # Check source file
    if (Test-Path $SourceFile) {
        Write-Host "✓ Source file found: $SourceFile" -ForegroundColor Green
    } else {
        Write-Host "✗ Source file not found: $SourceFile" -ForegroundColor Red
        return
    }
    
    # Check for Webots
    $webotsPaths = @(
        $env:WEBOTS_HOME,
        "C:\Program Files\Webots",
        "C:\Webots"
    )
    
    $webotFound = $false
    foreach ($path in $webotsPaths) {
        if ($path -and (Test-Path "$path\include\controller\c\webots\robot.h")) {
            Write-Host "✓ Webots found at: $path" -ForegroundColor Green
            $webotFound = $true
            break
        }
    }
    
    if (-not $webotFound) {
        Write-Host "✗ Webots not found. Install Webots or set WEBOTS_HOME" -ForegroundColor Red
    }
    
    # Check for compilers
    $compilers = @("gcc", "cl", "clang")
    $compilerFound = $false
    
    foreach ($comp in $compilers) {
        try {
            $null = Get-Command $comp -ErrorAction Stop
            Write-Host "✓ Compiler found: $comp" -ForegroundColor Green
            $compilerFound = $true
            break
        } catch {
            # Continue
        }
    }
    
    if (-not $compilerFound) {
        Write-Host "✗ No compiler found (gcc, cl, clang)" -ForegroundColor Red
        Write-Host "  Install Visual Studio Build Tools or MinGW" -ForegroundColor Yellow
    }
    
    if ($webotFound -and $compilerFound) {
        Write-Host "Ready to build!" -ForegroundColor Green
    }
}

function Show-Info {
    Write-Host "ChuhaBot C Controller Information" -ForegroundColor Cyan
    Write-Host "Current directory: $(Get-Location)" -ForegroundColor White
    
    if (Test-Path $SourceFile) {
        $size = (Get-Item $SourceFile).Length
        Write-Host "Source: $SourceFile ($size bytes)" -ForegroundColor White
    }
    
    if (Test-Path $OutputFile) {
        $size = (Get-Item $OutputFile).Length
        $date = (Get-Item $OutputFile).LastWriteTime
        Write-Host "Executable: $OutputFile ($size bytes)" -ForegroundColor Green
        Write-Host "Last built: $date" -ForegroundColor Green
    } else {
        Write-Host "Executable not found" -ForegroundColor Yellow
    }
    
    Write-Host ""
    Write-Host "To use in Webots:" -ForegroundColor Cyan
    Write-Host "1. Open Webots" -ForegroundColor White
    Write-Host "2. Load world with ChuhaBot robots" -ForegroundColor White
    Write-Host "3. Set controller to 'chuha_c_controller'" -ForegroundColor White
    Write-Host "4. Start simulation" -ForegroundColor White
}

# Main execution
switch ($Action.ToLower()) {
    "check" { Test-Requirements }
    "info" { Show-Info }
    "help" { Show-Help }
    default { 
        Write-Host "Unknown action: $Action" -ForegroundColor Red
        Show-Help 
    }
}
