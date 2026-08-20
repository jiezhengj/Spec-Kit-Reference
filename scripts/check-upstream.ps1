$ErrorActionPreference = 'Stop'
$scriptPath = Join-Path $PSScriptRoot 'check_upstream.py'
if (Get-Command python -ErrorAction SilentlyContinue) {
    & python $scriptPath @args
} elseif (Get-Command py -ErrorAction SilentlyContinue) {
    & py -3 $scriptPath @args
} else {
    throw 'Neither python nor the Windows py launcher is available on PATH.'
}
exit $LASTEXITCODE
