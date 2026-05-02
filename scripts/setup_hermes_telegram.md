# 🤖 Setup Hermes Telegram Bot — Guide pas-à-pas

> Permettre à Omar de piloter Hermes (et indirectement WULIX) depuis son téléphone via Telegram.

---

## Pourquoi ?

- ✅ Tu peux commander Hermes en mobilité (train, café, RDV client)
- ✅ Pas besoin que le HUD AISATOU soit ouvert
- ✅ Notifications push directes sur ton tel
- ✅ Hermes peut t'envoyer ses rapports (idées d'apps, veille) directement
- ✅ Bonus : Hermes peut déléguer des actions à AISATOU via API HTTP

---

## Étape 1 — Créer le bot Telegram (5 min)

1. Sur ton téléphone, ouvre Telegram et cherche **@BotFather**
2. Envoie `/newbot`
3. Nom du bot : `WULIX Hermes` (ou ce que tu veux)
4. Username : `wulix_hermes_bot` (doit finir par `_bot` et être unique)
5. BotFather te donne un **token** du genre :
   ```
   1234567890:AAEhBP_aabbccddeeffgghhiijjkkllmm-NN
   ```
6. **Note ce token** — on en a besoin juste après

### Bonus : récupérer ton chat_id
Pour que Hermes sache à qui envoyer les messages :
1. Démarre une conversation avec ton bot (clique le lien de BotFather)
2. Envoie `/start` au bot
3. Sur ton PC, ouvre dans le navigateur :
   ```
   https://api.telegram.org/bot<TON_TOKEN>/getUpdates
   ```
4. Cherche le `"chat":{"id":XXXXX...` — c'est ton **chat_id**

---

## Étape 2 — Configurer Hermes (3 min)

Dans un terminal Windows, lance :

```powershell
wsl -d Ubuntu -- /usr/local/bin/hermes gateway setup
```

L'assistant va te poser des questions. Réponds :
- Plateforme : **Telegram**
- Token : colle ton token BotFather
- Default chat_id : colle ton chat_id

> Si l'assistant demande autre chose (Discord, Slack, etc.), tu peux skip avec `n` ou `skip`.

---

## Étape 3 — Tester

```powershell
wsl -d Ubuntu -- /usr/local/bin/hermes gateway status
```

Tu devrais voir `Telegram: ✓ configured`.

Sur ton tel, envoie un message à ton bot, par exemple :
```
Quelle heure est-il à Paris ?
```

Hermes devrait répondre dans la conversation Telegram dans les 5-10s.

---

## Étape 4 — Rediriger les cron jobs vers Telegram (optionnel)

Pour recevoir les rapports KOFI / idées d'apps directement sur Telegram :

```powershell
wsl -d Ubuntu -- bash -c "hermes cron edit wulix-idees-apps --deliver telegram"
wsl -d Ubuntu -- bash -c "hermes cron edit wulix-veille-hebdo --deliver telegram"
```

Maintenant chaque matin à 6h tu recevras le rapport directement sur Telegram. Plus besoin d'ouvrir le PC.

---

## Commandes utiles à connaître

Une fois le bot configuré, tu peux envoyer des commandes naturelles :

| Sur Telegram | Ce que ça fait |
|---|---|
| `Quelle heure est-il ?` | Réponse simple |
| `Liste mes cron jobs` | Hermes liste tes routines |
| `Lance la routine wulix-idees-apps maintenant` | Force l'exécution immédiate |
| `Refactore ce code: [colle le code]` | Hermes refactore et te renvoie |
| `Génère un diagramme d'architecture pour FastAPI` | Skill `architecture-diagram` |

---

## Sécurité

⚠️ **Ne partage JAMAIS ton token bot publiquement.**

- Le token donne le contrôle total du bot
- Si compromis : `/revoke` sur BotFather → nouveau token
- Le token est stocké dans `~/.hermes/.env` côté WSL

---

## Désinstaller / changer de bot

```powershell
wsl -d Ubuntu -- /usr/local/bin/hermes gateway setup
# Et choisis "remove telegram" dans l'assistant
```

---

## Si ça ne marche pas

1. **Bot ne répond pas** : vérifie que `hermes gateway status` montre `running`
   - Si non : `wsl -d Ubuntu -- hermes gateway start`
2. **Token invalide** : refais l'étape 1 (BotFather → `/revoke` → nouveau token)
3. **chat_id introuvable** : envoie un message au bot AVANT de visiter `/getUpdates`
4. **Erreur Telegram** : `wsl -d Ubuntu -- journalctl --user -u hermes-gateway -f` pour voir les logs

---

## Aller plus loin : Discord / Slack / Signal

Hermes supporte aussi ces plateformes. Même process : `hermes gateway setup` puis choisir la plateforme. Pour WULIX, Telegram est le plus pratique (tu l'as déjà).
