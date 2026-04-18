# ─── Installation démarrage automatique AISATOU ──────────────────────────────
# Lance AISATOU HUD au démarrage de Windows (sans fenêtre console visible)

$ProjectDir = "C:\Users\USER\.claude\projects\projet jarvis"
$PythonExe  = "C:\Users\USER\AppData\Local\Programs\Python\Python311\pythonw.exe"
$Script     = "$ProjectDir\aisatou_hud.py"
$TaskName   = "AISATOU_HUD_Autostart"

# Vérifier que pythonw.exe existe
if (-not (Test-Path $PythonExe)) {
    # Fallback: chercher pythonw dans le PATH
    $PythonExe = (Get-Command pythonw.exe -ErrorAction SilentlyContinue)?.Source
    if (-not $PythonExe) {
        $PythonExe = (Get-Command python.exe -ErrorAction SilentlyContinue)?.Source
    }
}

Write-Host "Python: $PythonExe"
Write-Host "Script: $Script"

# Supprimer l'ancienne tâche si elle existe
Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false -ErrorAction SilentlyContinue

# Créer la tâche planifiée
$Action  = New-ScheduledTaskAction -Execute $PythonExe -Argument "`"$Script`"" -WorkingDirectory $ProjectDir
$Trigger = New-ScheduledTaskTrigger -AtLogOn
$Settings = New-ScheduledTaskSettingsSet `
    -ExecutionTimeLimit ([TimeSpan]::Zero) `
    -RestartCount 3 `
    -RestartInterval ([TimeSpan]::FromMinutes(1)) `
    -StartWhenAvailable `
    -DontStopIfGoingOnBatteries `
    -AllowStartIfOnBatteries

$Principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive -RunLevel Highest

Register-ScheduledTask `
    -TaskName $TaskName `
    -Action $Action `
    -Trigger $Trigger `
    -Settings $Settings `
    -Principal $Principal `
    -Description "Lance AISATOU HUD automatiquement au démarrage de Windows" `
    -Force

Write-Host ""
Write-Host "✓ Tâche '$TaskName' créée avec succès !"
Write-Host "  AISATOU démarrera automatiquement à la prochaine connexion."
Write-Host ""
Write-Host "Pour désactiver : Unregister-ScheduledTask -TaskName '$TaskName' -Confirm:`$false"
