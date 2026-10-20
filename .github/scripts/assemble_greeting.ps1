param(
    [Parameter(Mandatory=$true)][string]$Sheet,
    [string]$Ffmpeg = "ffmpeg"
)
$ErrorActionPreference = "Stop"
$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "../..")).Path
$sheetPath = (Resolve-Path -LiteralPath $Sheet).Path
$scratch = Join-Path ([System.IO.Path]::GetTempPath()) ("nishan-profile-gif-" + [guid]::NewGuid().ToString("N"))
New-Item -ItemType Directory -Path $scratch | Out-Null

# The artwork is generated as a 4-by-2 sheet. FFmpeg only separates
# those frames and assembles them; it does not synthesize character motion.
for ($index = 0; $index -lt 8; $index++) {
    $column = $index % 4
    $row = [math]::Floor($index / 4)
    $crop = "crop=iw/4:ih/2:$column*iw/4:$row*ih/2,scale=512:512:flags=lanczos"
    $framePath = Join-Path $scratch ("frame-{0:D2}.png" -f $index)
    & $Ffmpeg -hide_banner -loglevel error -y -i $sheetPath -vf $crop -frames:v 1 -update 1 $framePath
    if ($LASTEXITCODE -ne 0) { throw "Could not extract frame $index." }
}

# Wave twice, turn back to the keyboard, type, then turn to greet again.
$sequence = @(0,1,0,1,2,3,4,5,4,5,4,5,4,5,4,5,6,7)
$manifest = @("ffconcat version 1.0")
foreach ($frameIndex in $sequence) {
    $manifest += ("file 'frame-{0:D2}.png'" -f $frameIndex)
    $manifest += "duration 0.25"
}
$manifest += "file 'frame-07.png'"
$manifestPath = Join-Path $scratch "frames.ffconcat"
[System.IO.File]::WriteAllLines($manifestPath, $manifest, [System.Text.UTF8Encoding]::new($false))
$output = Join-Path $repoRoot "assets/developer-hello-work.gif"
$filter = "[0:v]fps=12,split[a][b];[a]palettegen=max_colors=224:stats_mode=full[p];[b][p]paletteuse=dither=sierra2_4a"
& $Ffmpeg -hide_banner -loglevel error -y -f concat -safe 0 -i $manifestPath -filter_complex $filter -loop 0 $output
if ($LASTEXITCODE -ne 0) { throw "GIF assembly failed." }
Copy-Item -LiteralPath (Join-Path $scratch "frame-00.png") -Destination (Join-Path $repoRoot "assets/developer-hello-work-preview.png")
Write-Output "Created $output"
Write-Output "Source frames retained at $scratch"
