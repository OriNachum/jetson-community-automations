# PowerShell script to initialize Python virtual environment
# Usage: .\init-venv.ps1

Write-Host "Initializing Python virtual environment..." -ForegroundColor Green

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    Write-Host "Found $pythonVersion" -ForegroundColor Cyan
} catch {
    Write-Host "Error: Python is not installed or not in PATH" -ForegroundColor Red
    exit 1
}

# Check if .venv already exists
if (Test-Path ".venv") {
    Write-Host "Virtual environment already exists at .venv" -ForegroundColor Yellow
    $response = Read-Host "Do you want to recreate it? (y/N)"
    if ($response -ne "y" -and $response -ne "Y") {
        Write-Host "Keeping existing virtual environment" -ForegroundColor Green
        exit 0
    }
    Write-Host "Removing existing virtual environment..." -ForegroundColor Yellow
    Remove-Item -Recurse -Force ".venv"
}

# Create virtual environment
Write-Host "Creating virtual environment..." -ForegroundColor Cyan
python -m venv .venv

if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Failed to create virtual environment" -ForegroundColor Red
    exit 1
}

Write-Host "Virtual environment created successfully!" -ForegroundColor Green

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Cyan
& ".\.venv\Scripts\Activate.ps1"

# Upgrade pip
Write-Host "Upgrading pip..." -ForegroundColor Cyan
python -m pip install --upgrade pip

# Install requirements if they exist
if (Test-Path "discord\requirements.txt") {
    Write-Host "Installing discord requirements..." -ForegroundColor Cyan
    pip install -r discord\requirements.txt
}

if (Test-Path "requirements.txt") {
    Write-Host "Installing root requirements..." -ForegroundColor Cyan
    pip install -r requirements.txt
}

Write-Host "`nSetup complete!" -ForegroundColor Green
Write-Host "To activate the virtual environment in the future, run:" -ForegroundColor Yellow
Write-Host "  .\.venv\Scripts\Activate.ps1" -ForegroundColor Cyan
