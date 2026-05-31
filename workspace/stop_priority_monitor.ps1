$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$PidPath = Join-Path $Root "state\priority_monitor.pid"

if (-not (Test-Path $PidPath)) {
    Write-Output "Priority monitor is not running: pid file not found."
    exit 0
}

$MonitorPid = Get-Content $PidPath -ErrorAction SilentlyContinue
if ($MonitorPid -and (Get-Process -Id ([int]$MonitorPid) -ErrorAction SilentlyContinue)) {
    Stop-Process -Id ([int]$MonitorPid) -Force
    Write-Output "Priority monitor stopped. PID=$MonitorPid"
} else {
    Write-Output "Priority monitor process not found. Cleaning pid file."
}

Remove-Item -LiteralPath $PidPath -Force -ErrorAction SilentlyContinue

