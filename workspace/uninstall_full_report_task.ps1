$ErrorActionPreference = "Stop"

$TaskName = "CodexFuturesFullReport15m"
schtasks /Delete /TN $TaskName /F | Out-Host
Write-Output "Deleted Windows scheduled task: $TaskName"

