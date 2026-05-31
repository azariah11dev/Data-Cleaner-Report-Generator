Write-Host "Starting Data Cleaner System..."

# Start backend
Write-Host "Starting FastAPI backend..."
$backend = Start-Process -FilePath "uvicorn" -ArgumentList "app:app --host 127.0.0.1 --port 8000" -WorkingDirectory ".\src\backend" -PassThru

Start-Sleep -Seconds 2

# Start frontend
Write-Host "Starting Express frontend..."
$frontend = Start-Process -FilePath "node" -ArgumentList "server.js" -WorkingDirectory "." -PassThru

Start-Sleep -Seconds 2

Write-Host "Backend running at http://localhost:8000"
Write-Host "Frontend running at http://localhost:3000"
Write-Host "System ready."

#Automatically open browser
Start-Process "http://localhost:3000"

Write-Host ""
Write-Host "Press CTRL+C to stop everything."
Wait-Process -Id $backend.Id, $frontend.Id

Write-Host "Stopping Data Cleaner System..."