# FactuSerein — site vitrine

Site statique public de FactuSerein. Il présente l'offre, les pages sectorielles, les tarifs et un formulaire de contact.

Le formulaire de la page d'accueil est uniquement un contact : il envoie le nom, l'adresse email et le message à l'API backend. Il ne lance pas de questionnaire et ne produit pas de diagnostic automatique.

## Développement local

Le site ne nécessite pas de compilation :

```powershell
python -m http.server 8080
```

Puis ouvrir `http://localhost:8080`.

## Déploiement actuel

- Bucket S3 : `fs-front-826224348203` en `eu-west-3`
- Distribution CloudFront : `E1MT8TEKETHVQ2`
- URL de contrôle : `https://d2po7vfowy39cq.cloudfront.net/`
- Domaine canonique choisi : `https://factuserein.fr/` (sans `www`, à rattacher ensuite à CloudFront)
- Script de déploiement complet : `../factuserein-backend/scripts/deploy-fronts.ps1`

Le script publie le site, le dashboard et l'installeur desktop. Pour une publication locale, fournir explicitement le chemin de l'installeur :

```powershell
& ..\factuserein-backend\scripts\deploy-fronts.ps1 `
  -InstallerPath ..\factuserein-client\src-tauri\target\release\bundle\nsis\FactuSerein_0.2.4_x64-setup.exe
```

En attendant la distribution `app` du lot 2, l'installeur et
`updates/latest.json` sont aussi publiés dans le bucket front et servis par
CloudFront. La page de téléchargement lit le SHA-256 depuis ce manifeste signé.

## GitHub Actions

`.github/workflows/deploy.yml` :

- vérifie le JavaScript, le HTML, les liens locaux, les images, les métadonnées SEO et le JSON-LD sur les pull requests ;
- ne déploie que `main` (push ou lancement manuel depuis `main`) vers S3 ;
- invalide CloudFront après publication.

Le contrôle statique est exécuté par `scripts/validate_site.py`, sans dépendance externe : il vérifie les canoniques, les titres/descriptions, les balises `h1`, les liens et ressources locales, les attributs `alt`, le sitemap, `robots.txt`, le JSON-LD et le JavaScript inline/externe.

Le workflow utilise GitHub OIDC avec le rôle `arn:aws:iam::826224348203:role/FactuSereinGitHubActionsDeploy`, déclaré directement dans le workflow. L'ARN n'est pas un secret ; les credentials AWS restent temporaires et ne sont jamais stockés dans GitHub. La trust policy AWS doit limiter ce rôle à ce dépôt, à `main` et aux actions S3/CloudFront nécessaires ; elle doit être vérifiée côté AWS avant la production.

## Images et design

Les images premium sont dans `assets/img/`. Toute nouvelle image doit être optimisée pour le web, référencée avec un texte `alt` utile et vérifiée sur mobile.

## Périmètre légal public

- `legal/mentions-legales.html` expose uniquement les informations publiques retenues pour le site et signale les éléments à valider avant la mise en ligne commerciale ;
- `legal/rgpd.html` décrit séparément le formulaire de contact et le service applicatif, sans affirmer une localisation, une certification ou un transfert non vérifié ;
- `legal/cgv.html` est une synthèse B2B publique. La version contractuelle complète doit être affichée dans l'application avant souscription et validée juridiquement ;
- les documents internes de `kit-commercial/`, `docs/` et les scripts de validation sont exclus de la publication S3 par la CI.

## Roadmap

1. Vérifier le premier déploiement automatique GitHub avec le rôle OIDC déjà créé.
2. Configurer le domaine CloudFront personnalisé et le redirigé `www` lorsque le domaine sera acheté.
3. Faire relire et compléter les documents légaux avant toute souscription commerciale.
4. Ne pas présenter le formulaire comme un diagnostic : il s'agit uniquement d'un contact email.
