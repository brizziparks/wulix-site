# Test toutes les routes API du HUD AISATOU
$auth = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes("aisatou:3eAeq9k!hk!H4SFK"))
$headers = @{Authorization = "Basic $auth"}
$base = "http://localhost:7777"

$routes = @(
    @{Method="GET"; Path="/health"; Desc="Health check"},
    @{Method="GET"; Path="/status"; Desc="Status global"},
    @{Method="GET"; Path="/models"; Desc="Liste modeles IA"},
    @{Method="GET"; Path="/history"; Desc="Historique conversations"},
    @{Method="GET"; Path="/agents/status"; Desc="Stats agents"},
    @{Method="GET"; Path="/agents/content"; Desc="Queue contenu"},
    @{Method="GET"; Path="/agents/prospects"; Desc="Prospects"},
    @{Method="GET"; Path="/agents/outreach"; Desc="Outreach queue"},
    @{Method="GET"; Path="/agents/revenue"; Desc="Revenus NDEYE"},
    @{Method="GET"; Path="/agents/blog"; Desc="Stats blog"},
    @{Method="GET"; Path="/agents/crowdsec"; Desc="CrowdSec NAS"},
    @{Method="GET"; Path="/agents/tasks"; Desc="Config taches agents"},
    @{Method="GET"; Path="/agents/recommendations"; Desc="Recommandations"},
    @{Method="GET"; Path="/pipeline/log"; Desc="Log pipeline"}
)

$ok = 0; $fail = 0
foreach ($r in $routes) {
    try {
        $resp = Invoke-WebRequest -Uri "$base$($r.Path)" -Method $r.Method -Headers $headers -TimeoutSec 5 -UseBasicParsing
        $status = $resp.StatusCode
        $size = $resp.Content.Length
        Write-Host ("{0,-35} {1,-20} [{2}] {3} bytes" -f $r.Path, $r.Desc, $status, $size) -ForegroundColor Green
        $ok++
    } catch {
        $err = $_.Exception.Message
        if ($err.Length -gt 60) { $err = $err.Substring(0,60) }
        Write-Host ("{0,-35} {1,-20} [FAIL] {2}" -f $r.Path, $r.Desc, $err) -ForegroundColor Red
        $fail++
    }
}

Write-Host "`n========================================"
Write-Host "Resultat: $ok OK / $fail FAIL ($($routes.Count) total)"
if ($fail -eq 0) { Write-Host "[OK] Toutes les routes repondent" -ForegroundColor Green }
else { Write-Host "[WARN] $fail routes en echec" -ForegroundColor Yellow }
