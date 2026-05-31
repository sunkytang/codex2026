$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$PidPath = Join-Path $Root "state\priority_monitor_visible.pid"

if (-not (Test-Path $PidPath)) {
    Write-Output "Visible priority monitor is not running: pid file not found."
    exit 0
}

$MonitorPid = Get-Content $PidPath -ErrorAction SilentlyContinue
if ($MonitorPid -and (Get-Process -Id ([int]$MonitorPid) -ErrorAction SilentlyContinue)) {
    Stop-Process -Id ([int]$MonitorPid) -Force
    Write-Output "Visible priority monitor stopped. PID=$MonitorPid"
} else {
    Write-Output "Visible priority monitor process not found. Cleaning pid file."
}

Remove-Item -LiteralPath $PidPath -Force -ErrorAction SilentlyContinue

