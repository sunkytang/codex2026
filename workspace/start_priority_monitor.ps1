$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$State = Join-Path $Root "state"
$PidPath = Join-Path $State "priority_monitor.pid"
$OutPath = Join-Path $State "priority_monitor.stdout.log"
$ErrPath = Join-Path $State "priority_monitor.stderr.log"

New-Item -ItemType Directory -Path $State -Force | Out-Null

if (Test-Path $PidPath) {
    $ExistingPid = Get-Content $PidPath -ErrorAction SilentlyContinue
    $ParsedPid = 0
    if ([int]::TryParse($ExistingPid, [ref]$ParsedPid)) {
        if (Get-Process -Id $ParsedPid -ErrorAction SilentlyContinue) {
            Write-Output "Priority monitor already running. PID=$ParsedPid"
            exit 0
        }
    }
    Remove-Item -LiteralPath $PidPath -Force -ErrorAction SilentlyContinue
}

$Python = "python"
$Args = "-m src.priority_monitor_loop --interval 300"
$Process = Start-Process -FilePath $Python -ArgumentList $Args -WorkingDirectory $Root -RedirectStandardOutput $OutPath -RedirectStandardError $ErrPath -WindowStyle Hidden -PassThru
Set-Content -Path $PidPath -Value $Process.Id -Encoding UTF8
Write-Output "Priority monitor started. PID=$($Process.Id)"
Write-Output "Latest summary: $State\priority_latest.md"
Write-Output "Log: $State\priority_monitor.log"
