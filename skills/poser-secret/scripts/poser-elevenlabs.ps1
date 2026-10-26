# Pose la clé ElevenLabs sans qu'elle passe par la conversation.
# Saisie masquée, test auprès d'ElevenLabs, écriture seulement si la clé répond,
# dans un fichier lisible par l'utilisateur Windows courant uniquement.

$ErrorActionPreference = "Stop"
$dossier = Join-Path $env:USERPROFILE ".secrets"
$fichier = Join-Path $dossier "elevenlabs.env"

$sec = Read-Host -AsSecureString "Clé ElevenLabs (xi-api-key)"
$bstr = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($sec)
try {
    $cle = [Runtime.InteropServices.Marshal]::PtrToStringBSTR($bstr).Trim()
} finally {
    [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($bstr)
}
if ($cle.Length -lt 20) { Write-Host "Clé trop courte ($($cle.Length) caractères), rien n'est écrit."; exit 1 }

# Test : la liste des voix suffit (une clé restreinte n'a pas toujours accès au compte).
$code = 0
foreach ($url in @("https://api.elevenlabs.io/v1/voices", "https://api.elevenlabs.io/v1/user")) {
    try {
        $r = Invoke-WebRequest -Uri $url -Headers @{ "xi-api-key" = $cle } -UseBasicParsing -Method Get
        $code = [int]$r.StatusCode
    } catch {
        if ($_.Exception.Response) { $code = [int]$_.Exception.Response.StatusCode } else { $code = -1 }
    }
    if ($code -eq 200) { break }
}
if ($code -ne 200) { Write-Host "ElevenLabs refuse la clé (HTTP $code). Rien n'est écrit."; exit 1 }

New-Item -ItemType Directory -Force -Path $dossier | Out-Null
Set-Content -Path $fichier -Value "ELEVENLABS_API_KEY=$cle" -Encoding ascii -NoNewline
$cle = $null

# Droits : seul l'utilisateur courant lit le dossier et le fichier.
icacls $dossier /inheritance:r /grant:r "$($env:USERNAME):(OI)(CI)F" | Out-Null
icacls $fichier /inheritance:r /grant:r "$($env:USERNAME):F" | Out-Null

Write-Host "Clé ElevenLabs vérifiée (HTTP 200) et enregistrée dans $fichier"
