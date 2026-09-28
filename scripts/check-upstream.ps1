$ErrorActionPreference = 'Stop'
$scriptPath = Join-Path $PSScriptRoot 'check_upstream.py'
if (Get-Command python -ErrorAction SilentlyContinue) {
    & python $scriptPath @args
} elseif (Get-Command py -ErrorAction SilentlyContinue) {
    & py -3 $scriptPath @args
} else {
    throw 'PATH 中找不到 Python，也找不到 Windows py 启动器。'
}
exit $LASTEXITCODE
