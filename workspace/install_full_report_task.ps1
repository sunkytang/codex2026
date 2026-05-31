$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$TaskName = "CodexFuturesFullReport15m"
$ScriptPath = Join-Path $Root "run_full_report_task.ps1"
$Action = "powershell.exe -NoProfile -ExecutionPolicy Bypass -File `"$ScriptPath`""

schtasks /Create /TN $TaskName /SC MINUTE /MO 15 /TR $Action /F | Out-Host
Write-Output "Installed Windows scheduled task: $TaskName"
Write-Output "Latest report: $Root\state\full_report_latest.md"

