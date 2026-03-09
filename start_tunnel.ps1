$ErrorActionPreference = "Continue"
Write-Host "Starting Future India Auto-Tunnel..." -ForegroundColor Green

while ($true) {
    Write-Host "Launching localtunnel on port 8000..." -ForegroundColor Cyan
    # Run localtunnel
    lt --port 8000 --subdomain future-india-backend
    
    # If it crashes or disconnects, it hits this line
    Write-Host "Tunnel disconnected! Restarting in 3 seconds..." -ForegroundColor Yellow
    Start-Sleep -Seconds 3
}
