# Pose le bot Telegram « livraisons » de Claude, sans que le jeton passe par la conversation.
#   powershell -ExecutionPolicy Bypass -File poser-bot.ps1
# 1. saisie masquée du jeton (donné par @BotFather), vérifié par getMe avant écriture ;
# 2. tu envoies un message au bot depuis ton téléphone : le script y lit ton chat_id ;
# 3. écrit ~/.claude/secrets/telegram.env (lisible par toi seul) puis envoie un message de test.
# Le jeton n'est jamais affiché ; en cas d'erreur, seul le code HTTP l'est.

$ErrorActionPreference = 'Stop'
$dossier = Join-Path $env:USERPROFILE '.claude\secrets'
$fichier = Join-Path $dossier 'telegram.env'

function Appel($jeton, $methode, $corps) {
    try {
        $url = "https://api.telegram.org/bot$jeton/$methode"
        if ($corps) { return Invoke-RestMethod -Method Post -Uri $url -ContentType 'application/json; charset=utf-8' -Body ([Text.Encoding]::UTF8.GetBytes(($corps | ConvertTo-Json -Compress))) }
        return Invoke-RestMethod -Uri $url
    } catch {
        $code = $_.Exception.Response.StatusCode.value__
        throw "Telegram a refusé $methode (HTTP $code)."
    }
}

$sec = Read-Host -AsSecureString 'Jeton du bot (donné par @BotFather, la saisie reste masquée)'
$jeton = [Runtime.InteropServices.Marshal]::PtrToStringBSTR([Runtime.InteropServices.Marshal]::SecureStringToBSTR($sec)).Trim()
if ($jeton -notmatch '^\d{6,12}:[A-Za-z0-9_-]{30,}$') { Write-Host 'Ce texte ne ressemble pas à un jeton de bot. Rien n''a été écrit.'; exit 1 }

$moi = (Appel $jeton 'getMe').result
Write-Host "Jeton valide : bot @$($moi.username)."
Write-Host "Depuis ton téléphone, ouvre https://t.me/$($moi.username), appuie sur Démarrer ou envoie « salut »."
Write-Host 'J''attends ton message (2 minutes au plus)...'

$chat = $null
$limite = (Get-Date).AddMinutes(2)
while (-not $chat -and (Get-Date) -lt $limite) {
    $maj = (Appel $jeton 'getUpdates' @{ timeout = 20; allowed_updates = @('message') }).result
    $msg = $maj | Where-Object { $_.message.chat.type -eq 'private' } | Select-Object -Last 1
    if ($msg) { $chat = $msg.message.chat.id }
}
if (-not $chat) { Write-Host 'Aucun message reçu : relance le script et écris au bot pendant l''attente.'; exit 1 }

New-Item -ItemType Directory -Force $dossier | Out-Null
Set-Content -Path $fichier -Encoding ASCII -Value @("TELEGRAM_BOT_TOKEN=$jeton", "TELEGRAM_CHAT_ID=$chat")
# Droits : toi seul (héritage coupé, Administrateurs et SYSTEM retirés).
icacls $fichier /inheritance:r /grant:r "$($env:USERNAME):(R,W)" | Out-Null
$jeton = $null

$cfg = Get-Content $fichier | ConvertFrom-StringData
Appel $cfg.TELEGRAM_BOT_TOKEN 'sendMessage' @{ chat_id = $chat; text = 'Bot de livraison prêt : Claude t''enverra ici les vidéos, aperçus et liens à voir.' } | Out-Null
Write-Host "C'est prêt : message de test envoyé. Configuration dans $fichier (lisible par toi seul)."
