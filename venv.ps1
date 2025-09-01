$current_location = (Get-Location).Path
$path = $current_location + "\venv"
$activate_script = $current_location + "\venv\Scripts\Activate.ps1"
$src_path = $current_location + "\src"

if (Test-Path -Path $path) {
    echo "venv was found"
    Invoke-Expression $activate_script
    Set-Location $src_path
} else {
    python -m venv $path
    Invoke-Expression $activate_script
    Set-Location $src_path
}
