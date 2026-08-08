/* ============================================================
   FactuConforme — script commun
   ============================================================ */
(function () {
  "use strict";

  // Menu mobile
  var toggle = document.querySelector(".menu-toggle");
  var nav = document.querySelector(".main-nav");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      nav.classList.toggle("ouvert");
    });
  }

  // Année du footer
  var annee = document.querySelectorAll(".js-annee");
  annee.forEach(function (el) {
    el.textContent = new Date().getFullYear();
  });

  // Compte à rebours simple vers l'échéance de réception (01/09/2026)
  var cible = new Date("2026-09-01T00:00:00+02:00");
  var elJours = document.getElementById("js-jours");
  if (elJours) {
    function maj() {
      var diff = cible - new Date();
      if (diff <= 0) {
        elJours.textContent = "Échéance passée — nous sommes toujours là pour vous mettre en conformité";
        return;
      }
      var jours = Math.ceil(diff / 86400000);
      elJours.textContent =
        "Obligation de réception des factures électroniques : 1er septembre 2026 — plus que " + jours + " jours";
    }
    maj();
  }

  // FAQ : un seul panneau ouvert
  document.querySelectorAll(".faq details").forEach(function (d) {
    d.addEventListener("toggle", function () {
      if (d.open) {
        document.querySelectorAll(".faq details[open]").forEach(function (autre) {
          if (autre !== d) autre.removeAttribute("open");
        });
      }
    });
  });

  // Zone de dépôt factice (page validateur) : indique le format, désactive l'envoi réel
  var zone = document.getElementById("js-zone-depot");
  var input = document.getElementById("js-fichier");
  var statut = document.getElementById("js-statut-upload");
  if (zone && input) {
    zone.addEventListener("click", function () { input.click(); });
    zone.addEventListener("dragover", function (e) { e.preventDefault(); });
    zone.addEventListener("drop", function (e) {
      e.preventDefault();
      if (e.dataTransfer.files.length) {
        input.files = e.dataTransfer.files;
        afficherFichier(e.dataTransfer.files[0]);
      }
    });
    input.addEventListener("change", function () {
      if (input.files.length) afficherFichier(input.files[0]);
    });
    function afficherFichier(f) {
      if (!statut) return;
      statut.innerHTML =
        'Fichier reçu : <strong>' + f.name + '</strong> (' + Math.round(f.size / 1024) + ' Ko). ' +
        '<br>Le validateur en ligne sera branché ici dès sa sortie. ' +
        'Laissez votre email ci-dessous pour être prévenu — et pour vérifier dès maintenant ' +
        'si votre logiciel est conforme, utilisez le bouton "Vérifier ma conformité".';
    }
  }
})();
