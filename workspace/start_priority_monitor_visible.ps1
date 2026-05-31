$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$State = Join-Path $Root "state"
$PidPath = Join-Path $State "priority_monitor_visible.pid"

New-Item -ItemType Directory -Path $State -Force | Out-Null

if (Test-Path $PidPath) {
    $ExistingPid = Get-Content $PidPath -ErrorAction SilentlyContinue
    $ParsedPid = 0
    if ([int]::TryParse($ExistingPid, [ref]$ParsedPid)) {
        if (Get-Process -Id $ParsedPid -ErrorAction SilentlyContinue) {
            Write-Output "Visible priority monitor already running. PID=$ParsedPid"
            exit 0
        }
    }
    Remove-Item -LiteralPath $PidPath -Force -ErrorAction SilentlyContinue
}

$Command = "cd /d `"$Root`"; python -m src.priority_monitor_loop --interval 300"
$Process = Start-Process -FilePath "cmd.exe" -ArgumentList "/k title Futures 5m Monitor && $Command" -WorkingDirectory $Root -PassThru
Set-Content -Path $PidPath -Value $Process.Id -Encoding UTF8
Write-Output "Visible priority monitor started. PID=$($Process.Id)"
Write-Output "A terminal window should now print the summary every 5 minutes."

