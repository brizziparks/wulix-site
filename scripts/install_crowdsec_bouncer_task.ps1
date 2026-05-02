# Installe la tâche planifiée Windows pour CrowdSec Bouncer
# Lance python agents/crowdsec_cf_bouncer.py toutes les 15 minutes
# Logs : agents/logs/crowdsec_bouncer.log

$projDir   = "C:\Users\USER\.claude\projects\projet jarvis"
$pythonExe = "C:\Users\USER\AppData\Local\Programs\Python\Python311\python.exe"
$script    = "$projDir\agents\crowdsec_cf_bouncer.py"
$logsDir   = "$projDir\agents\logs"
$logFile   = "$logsDir\crowdsec_bouncer.log"

# Créer le dossier logs s'il n'existe pas
if (-not (Test-Path $logsDir)) {
    New-Item -ItemType Directory -Path $logsDir -Force | Out-Null
}

$taskName = "WULIX_CrowdSec_Bouncer"

# Action : exécuter le script Python
$action = New-ScheduledTaskAction `
    -Execute $pythonExe `
    -Argument "`"$script`"" `
    -WorkingDirectory $projDir

# Trigger : toutes les 15 min, démarre à minuit, pour toujours
$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date) `
    -RepetitionInterval (New-TimeSpan -Minutes 15)

# Settings : ne pas afficher la fenêtre, runIfOffline, retry on failure
$settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -RestartCount 3 `
    -RestartInterval (New-TimeSpan -Minutes 2) `
    -ExecutionTimeLimit (New-TimeSpan -Minutes 5)

# Principal : utilisateur courant, no privileges elevation
$principal = New-ScheduledTaskPrincipal -UserId "$env:USERNAME" -LogonType Interactive -RunLevel Limited

# Supprime l'ancienne tâche si elle existe
Unregister-ScheduledTask -TaskName $taskName -Confirm:$false -ErrorAction SilentlyContinue

# Enregistre la nouvelle tâche
Register-ScheduledTask `
    -TaskName $taskName `
    -Description "WULIX - Sync CrowdSec NAS bans -> Cloudflare Firewall (every 15 min)" `
    -Action $action `
    -Trigger $trigger `
    -Settings $settings `
    -Principal $principal | Out-Null

Write-Host ""
Write-Host "[OK] Tache planifiee installee : $taskName" -ForegroundColor Green
Write-Host "  Script   : $script"
Write-Host "  Frequence: toutes les 15 minutes"
Write-Host "  Logs     : $logFile"
Write-Host ""

# Test : execution immediate pour verifier
Write-Host "Lancement immediat pour test..." -ForegroundColor Cyan
Start-ScheduledTask -TaskName $taskName
Start-Sleep -Seconds 3
$task = Get-ScheduledTask -TaskName $taskName | Get-ScheduledTaskInfo
Write-Host "  Dernier resultat : $($task.LastTaskResult) (0 = OK)"
Write-Host "  Prochaine exec   : $($task.NextRunTime)"
Write-Host ""
Write-Host "Pour desinstaller : Unregister-ScheduledTask -TaskName '$taskName' -Confirm:`$false"
