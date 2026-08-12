# FactuSerein â€” site vitrine

Site statique public de FactuSerein. Il prÃ©sente l'offre, les pages sectorielles, les tarifs et un formulaire de contact.

Le formulaire de la page d'accueil est uniquement un contact : il envoie le nom, l'adresse email et le message Ã  l'API backend. Il ne lance pas de questionnaire et ne produit pas de diagnostic automatique.

## DÃ©veloppement local

Le site ne nÃ©cessite pas de compilation :

```powershell
python -m http.server 8080
```

Puis ouvrir `http://localhost:8080`.

## DÃ©ploiement actuel

- Bucket S3 : `fs-front-826224348203` en `eu-west-3`
- Distribution CloudFront : `E1MT8TEKETHVQ2`
- URL de contrÃ´le : `https://d2po7vfowy39cq.cloudfront.net/`
- Domaine canonique choisi : `https://factuserein.fr/` (sans `www`, Ã  rattacher ensuite Ã  CloudFront)
- Script de dÃ©ploiement complet : `../factuserein-backend/scripts/deploy-fronts.ps1`

Le script publie le site, le dashboard et l'installeur desktop. Pour une publication locale, fournir explicitement le chemin de l'installeur :

```powershell
& ..\factuserein-backend\scripts\deploy-fronts.ps1 `
  -InstallerPath ..\factuserein-client\src-tauri\target\release\bundle\nsis\FactuSerein_0.2.5_x64-setup.exe
```

En attendant la distribution `app` du lot 2, l'installeur et
`updates/latest.json` sont aussi publiÃ©s dans le bucket front et servis par
CloudFront. La page de tÃ©lÃ©chargement lit le SHA-256 depuis ce manifeste signÃ©.

## GitHub Actions

`.github/workflows/deploy.yml` :

- vÃ©rifie le JavaScript, le HTML, les liens locaux, les images, les mÃ©tadonnÃ©es SEO et le JSON-LD sur les pull requests ;
- ne dÃ©ploie que `main` (push ou lancement manuel depuis `main`) vers S3 ;
- invalide CloudFront aprÃ¨s publication.

Le contrÃ´le statique est exÃ©cutÃ© par `scripts/validate_site.py`, sans dÃ©pendance externe : il vÃ©rifie les canoniques, les titres/descriptions, les balises `h1`, les liens et ressources locales, les attributs `alt`, le sitemap, `robots.txt`, le JSON-LD et le JavaScript inline/externe.

Le workflow utilise GitHub OIDC avec le rÃ´le `arn:aws:iam::826224348203:role/FactuSereinGitHubActionsDeploy`, dÃ©clarÃ© directement dans le workflow. L'ARN n'est pas un secret ; les credentials AWS restent temporaires et ne sont jamais stockÃ©s dans GitHub. La trust policy AWS doit limiter ce rÃ´le Ã  ce dÃ©pÃ´t, Ã  `main` et aux actions S3/CloudFront nÃ©cessaires ; elle doit Ãªtre vÃ©rifiÃ©e cÃ´tÃ© AWS avant la production.

## Images et design

Les images premium sont dans `assets/img/`. Toute nouvelle image doit Ãªtre optimisÃ©e pour le web, rÃ©fÃ©rencÃ©e avec un texte `alt` utile et vÃ©rifiÃ©e sur mobile.

## PÃ©rimÃ¨tre lÃ©gal public

- `legal/mentions-legales.html` expose uniquement les informations publiques retenues pour le site et signale les Ã©lÃ©ments Ã  valider avant la mise en ligne commerciale ;
- `legal/rgpd.html` dÃ©crit sÃ©parÃ©ment le formulaire de contact et le service applicatif, sans affirmer une localisation, une certification ou un transfert non vÃ©rifiÃ© ;
- `legal/cgv.html` est une synthÃ¨se B2B publique. La version contractuelle complÃ¨te doit Ãªtre affichÃ©e dans l'application avant souscription et validÃ©e juridiquement ;
- les documents internes de `kit-commercial/`, `docs/` et les scripts de validation sont exclus de la publication S3 par la CI.

## Roadmap

1. VÃ©rifier le premier dÃ©ploiement automatique GitHub avec le rÃ´le OIDC dÃ©jÃ  crÃ©Ã©.
2. Configurer le domaine CloudFront personnalisÃ© et le redirigÃ© `www` lorsque le domaine sera achetÃ©.
3. Faire relire et complÃ©ter les documents lÃ©gaux avant toute souscription commerciale.
4. Ne pas prÃ©senter le formulaire comme un diagnostic : il s'agit uniquement d'un contact email.
