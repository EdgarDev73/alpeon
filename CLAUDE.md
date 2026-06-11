# ALPÉON — Règles projet (à respecter ABSOLUMENT)

## ⛔ RÈGLE N°1 — NE JAMAIS appeler l'OAuth Guesty manuellement

Guesty rate-limite l'OAuth **très agressivement** par `client_id`. Un seul burst
d'appels (`POST https://booking.guesty.com/oauth2/token`) suffit à bloquer (429)
**toute l'application OAuth**, y compris le cron — ce qui force à recréer une
nouvelle application Guesty. **C'est la cause historique des pannes quotidiennes
du site et de la perte de credentials.**

Concrètement, pendant le développement :
- ❌ NE JAMAIS faire `curl .../oauth2/token` pour "tester" les credentials.
- ❌ NE JAMAIS faire de boucle de retry sur `/api/refresh-token` (chaque échec 429
     allonge le cooldown Guesty).
- ❌ NE JAMAIS écrire de script qui itère des appels OAuth.
- ✅ Pour vérifier que le site marche : tester `/api/properties` et
     `/api/properties/<id>/calendar` (endpoints publics, PAS d'OAuth déclenché).
- ✅ Si le token est expiré : laisser le **cron** `/api/refresh-token` (toutes les 6h)
     faire le seul appel OAuth. Au pire, le déclencher **UNE** fois et attendre —
     jamais en boucle.

## Architecture token (self-healing, sans thundering herd)

- Le token OAuth Guesty dure **24h**.
- **SEUL** `/api/refresh-token` (cron `0 */6 * * *`) fait de l'OAuth → 4 appels/jour,
  jamais rate-limité.
- Les Lambdas API (`properties`, `calendar`, `quotes`) ne font **JAMAIS** d'OAuth.
  `getToken()` dans `api/_lib/guesty.js` retourne le token disponible
  (mémoire → /tmp → env var baked-in) **sans jamais le rafraîchir**.
- Sur 401, `guestyFetch` vide juste son cache et remonte l'erreur ; l'appelant sert
  son cache stale / fallback. **Aucun OAuth déclenché.**
- Le cron : OAuth → met à jour l'env var `GUESTY_ACCESS_TOKEN` (toutes les entrées :
  production + preview/dev) → déclenche un **Deploy Hook** Vercel
  (`VERCEL_DEPLOY_HOOK`) qui rebuild → les nouveaux Lambdas ont le token frais
  baked-in. Tant qu'≥1 redéploiement/24h réussit, le token baked n'expire jamais.

## Env vars Vercel (clés, pas les valeurs)

- `GUESTY_CLIENT_ID`, `GUESTY_CLIENT_SECRET` — credentials OAuth (cron uniquement)
- `GUESTY_ACCESS_TOKEN` — token baked, mis à jour par le cron (2 entrées : prod + preview/dev)
- `VRL_API_TOKEN` — pour PATCH des env vars Vercel
- `VERCEL_DEPLOY_HOOK` — URL de redéploiement (méthode fiable, préférée à l'API)
- `REFRESH_SECRET` — protège `/api/refresh-token?secret=...`
- `VERCEL_PROJECT_ID` = `prj_lkINpF7Y4ucOpVPDyEdAwJLefCaf`
- Fichier local de référence (NON commité, gitignored) : `.env.vercel`

## Guesty Booking Engine — divers

- Pagination **par curseur** (`pagination.cursor.next`), PAS `page: N`.
  ⚠️ `pagination.total` peut valoir la taille de page (pas le total global) — ne PAS
  s'en servir pour arrêter la boucle ; suivre le curseur jusqu'à `null`.
- Le **fallback** `assets/data/properties-fallback.json` est servi quand Guesty est
  injoignable. Format accepté : `[...]` ou `{ "properties": [...] }`. À regénérer
  quand le catalogue change (actuellement 32 biens).
- Le site communique "**100+ biens gérés**" (chiffre marketing, ≠ nb réel de listings).

## Déploiement

- Site **HTML statique pur** (pas de framework) + API serverless Node dans `/api/`.
- Modifs en masse sur le HTML : scripts Python dans `_scripts/`.
- Déployé sur Vercel ; push sur `main` → déploiement auto.
