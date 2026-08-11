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
  -InstallerPath ..\factuserein-client\src-tauri\target\release\bundle\nsis\FactuSerein_0.2.1_x64-setup.exe
```

## GitHub Actions

`.github/workflows/deploy.yml` :

- vérifie le JavaScript et les fichiers essentiels sur les pull requests ;
- déploie automatiquement `main` vers S3 ;
- invalide CloudFront après publication.

Le workflow utilise GitHub OIDC avec le rôle `arn:aws:iam::826224348203:role/FactuSereinGitHubActionsDeploy`, déclaré directement dans le workflow. L'ARN n'est pas un secret ; les credentials AWS restent temporaires et ne sont jamais stockés dans GitHub. Le rôle IAM est limité au dépôt, à `main` et aux actions S3/CloudFront nécessaires.

## Images et design

Les images premium sont dans `assets/img/`. Toute nouvelle image doit être optimisée pour le web, référencée avec un texte `alt` utile et vérifiée sur mobile.

## Roadmap

1. Vérifier le premier déploiement automatique GitHub avec le rôle OIDC déjà créé.
2. Ajouter un contrôle des liens locaux et des tailles d'images dans la CI.
3. Configurer un domaine CloudFront personnalisé si nécessaire et vérifier les en-têtes de cache.
4. Ne pas présenter le formulaire comme un diagnostic tant qu'aucun questionnaire ou moteur de diagnostic n'est réellement implémenté.
