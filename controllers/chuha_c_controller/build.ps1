# PowerShell Build Script for ChuhaBot C Controller
# For Windows systems without make/gcc

param(
    [Parameter(Mandatory=$false)]
    [string]$Target = "help"
)

# Configuration
$ControllerName = "chuha_c_controller"
$SourceFile = "$ControllerName.c"
$OutputFile = "$ControllerName.exe"

# Colors for output
function Write-Success { param($Message) Write-Host $Message -ForegroundColor Green }
function Write-Error { param($Message) Write-Host $Message -ForegroundColor Red }
function Write-Info { param($Message) Write-Host $Message -ForegroundColor Cyan }
function Write-Warning { param($Message) Write-Host $Message -ForegroundColor Yellow }

function Show-Help {
    Write-Host "ChuhaBot C Controller Build System" -ForegroundColor Yellow
    Write-Host "==================================" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Available commands:" -ForegroundColor White
    Write-Host "  .\build.ps1 build    - Build the controller" -ForegroundColor Green
    Write-Host "  .\build.ps1 clean    - Clean build files" -ForegroundColor Green
    Write-Host "  .\build.ps1 check    - Check build requirements" -ForegroundColor Green
    Write-Host "  .\build.ps1 help     - Show this help" -ForegroundColor Green
    Write-Host ""
    Write-Host "Requirements:" -ForegroundColor White
    Write-Host "  - Webots installed (with C API)" -ForegroundColor Gray
    Write-Host "  - Visual Studio Build Tools or MinGW" -ForegroundColor Gray
    Write-Host "  - WEBOTS_HOME environment variable (optional)" -ForegroundColor Gray
    Write-Host ""
    Write-Host "Note: This controller provides high-performance" -ForegroundColor Yellow
    Write-Host "      C-based swarm behaviors for ChuhaBot robots." -ForegroundColor Yellow
}

function Test-BuildRequirements {
    Write-Info "Checking build requirements..."
    
    $errors = @()
    
    # Check for source file
    if (-not (Test-Path $SourceFile)) {
        $errors += "Source file '$SourceFile' not found"
    } else {
        Write-Success "✓ Source file found: $SourceFile"
    }
    
    # Check for Webots
    $webots_paths = @(
        $env:WEBOTS_HOME,
        "C:\Program Files\Webots",
        "C:\Webots"
    )
    
    $webots_found = $false
    foreach ($path in $webots_paths) {
        if ($path -and (Test-Path "$path\include\controller\c\webots\robot.h")) {
            Write-Success "✓ Webots found at: $path"
            $script:WebotsPPath = $path
            $webots_found = $true
            break
        }
    }
    
    if (-not $webots_found) {
        $errors += "Webots installation not found. Install Webots or set WEBOTS_HOME"
    }
    
    # Check for compiler
    $compilers = @("gcc", "cl", "clang")
    $compiler_found = $false
    
    foreach ($compiler in $compilers) {
        try {
            $null = Get-Command $compiler -ErrorAction Stop
            Write-Success "✓ Compiler found: $compiler"
            $script:Compiler = $compiler
            $compiler_found = $true
            break
        } catch {
            # Compiler not found, continue checking
        }
    }
    
    if (-not $compiler_found) {
        $errors += "No suitable compiler found. Install Visual Studio Build Tools, MinGW, or GCC"
    }
    
    if ($errors.Count -gt 0) {
        Write-Error "Build requirements not met:"
        foreach ($error in $errors) {
            Write-Error "  ✗ $error"
        }
        return $false
    }
    
    Write-Success "All build requirements satisfied!"
    return $true
}

function Build-Controller {
    Write-Info "Building ChuhaBot C Controller..."
    
    if (-not (Test-BuildRequirements)) {
        return $false
    }
    
    # Prepare build command based on available compiler
    $includeDir = "$script:WebotsPPath\include\controller\c"
    $libDir = "$script:WebotsPPath\lib\controller"
    
    switch ($script:Compiler) {
        "gcc" {
            $buildCommand = "gcc -Wall -O2 -I`"$includeDir`" -L`"$libDir`" -o $OutputFile $SourceFile -lController"
        }
        "clang" {
            $buildCommand = "clang -Wall -O2 -I`"$includeDir`" -L`"$libDir`" -o $OutputFile $SourceFile -lController"
        }
        "cl" {
            # Visual Studio compiler
            $buildCommand = "cl /O2 /I`"$includeDir`" $SourceFile /link /LIBPATH:`"$libDir`" Controller.lib /OUT:$OutputFile"
        }
        default {
            Write-Error "Unsupported compiler: $script:Compiler"
            return $false
        }
    }
    
    Write-Info "Build command: $buildCommand"
    
    try {
        Invoke-Expression $buildCommand
        
        if (Test-Path $OutputFile) {
            Write-Success "✓ Controller built successfully: $OutputFile"
            return $true
        } else {
            Write-Error "✗ Build failed - output file not found"
            return $false
        }
    } catch {
        Write-Error "✗ Build failed: $($_.Exception.Message)"
        return $false
    }
}

function Clean-BuildFiles {
    Write-Info "Cleaning build files..."
    
    $files_to_clean = @($OutputFile, "*.obj", "*.pdb", "*.exp", "*.lib")
    
    foreach ($pattern in $files_to_clean) {
        $files = Get-ChildItem -Path . -Name $pattern -ErrorAction SilentlyContinue
        foreach ($file in $files) {
            Remove-Item $file -Force
            Write-Success "Removed: $file"
        }
    }
    
    Write-Success "Clean complete"
}

function Show-BuildInfo {
    Write-Info "ChuhaBot C Controller"
    Write-Info "Current directory: $(Get-Location)"
    
    if (Test-Path $SourceFile) {
        $size = (Get-Item $SourceFile).Length
        Write-Info "Source file: $SourceFile ($size bytes)"
    }
    
    if (Test-Path $OutputFile) {
        $size = (Get-Item $OutputFile).Length
        $date = (Get-Item $OutputFile).LastWriteTime
        Write-Success "Executable: $OutputFile ($size bytes, built $date)"
    } else {
        Write-Warning "Executable not found - run 'build' to compile"
    }
}

# Main execution
switch ($Target.ToLower()) {
    "build" {
        if (Build-Controller) {
            Write-Host ""
            Write-Success "🚀 Ready to use in Webots!"
            Write-Info "1. Open Webots"
            Write-Info "2. Load a world with ChuhaBot robots"
            Write-Info "3. Set controller to 'chuha_c_controller'"
            Write-Info "4. Start simulation"
        }
    }
    "clean" {
        Clean-BuildFiles
    }
    "check" {
        Test-BuildRequirements
        Show-BuildInfo
    }
    "help" {
        Show-Help
    }
    default {
        Write-Warning "Unknown target: $Target"
        Show-Help
    }
}
