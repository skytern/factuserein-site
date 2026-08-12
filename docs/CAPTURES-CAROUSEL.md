# Captures du carousel de l'application

Le carousel de `outils/telecharger.html` présente des captures réelles de l'interface Windows. Les données affichées doivent rester fictives ou anonymisées.

`app-screenshot-tauri-settings.png` est une capture de la vraie fenêtre Tauri
Windows, sans chemin utilisateur ni donnée personnelle. Les captures de
validation sont prises sur l'interface de contrôle du service avec des
factures synthétiques.

## Ajouter une capture

1. Déposer l'image PNG dans `assets/img/` avec un nom explicite, par exemple `app-screenshot-validation-history.png`.
2. Ajouter une balise `<figure class="app-slide" data-slide aria-hidden="true">` dans le carousel.
3. Ajouter un bouton `.carousel-dot` avec l'index suivant.
4. Renseigner un `alt` descriptif et une légende courte orientée bénéfice.

Le JavaScript du site détecte automatiquement le nombre de slides et gère les flèches, les pastilles et le clavier.

## Vues utiles pour les personas

- Dirigeant de TPE : statut du dossier, prochaine action et résultat compréhensible.
- Gestionnaire administratif : PDF à gauche, champs extraits et contrôles à droite.
- Comptable : totaux HT/TVA/TTC, lignes et divergences clairement visibles.
- Lecture facture : le lecteur PDF intégré conserve le zoom natif ; le bouton
  `Plein écran` permet d'agrandir le document sans quitter la validation.
- Utilisateur face à une anomalie : champs à compléter en rouge, explication et relance IA.
- Utilisateur avec un scan : badge de vérification renforcée et indication de contrôle.
- Responsable client : historique d'une facture, entreprise reconnue et coordonnées mises à jour.

Éviter les données de production, les adresses personnelles et les identifiants secrets dans les captures publiées.
