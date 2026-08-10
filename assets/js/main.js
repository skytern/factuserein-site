/* ============================================================
   FactuSerein — script commun
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
})();
