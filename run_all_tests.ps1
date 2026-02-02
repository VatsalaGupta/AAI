# Run all tests script for Assignment
# Usage: .\run_all_tests.ps1 -MaxDays 10 -N 2 -K 5 -PrintSchedule
param(
    [int]$MaxDays = 10,
    [int]$N = 2,
    [int]$K = 5,
    [switch]$PrintSchedule
)

$flags = ""
if ($PrintSchedule) { $flags += " --print-schedule" }

New-Item -ItemType Directory -Path .\results -Force | Out-Null
Get-ChildItem -Filter 'input*.txt' | ForEach-Object {
    $in = $_.Name
    Write-Host "Running $in (normal)"
    python .\assg02.py $in $MaxDays $N $K $flags > ".\results\$($in)_normal.out"
    Write-Host "Running $in (nextday)"
    python .\assg02.py $in $MaxDays $N $K --nextday $flags > ".\results\$($in)_nextday.out"
}

Write-Host "All tests finished. Results are in .\results\"