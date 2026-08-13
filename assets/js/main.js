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
      var ouvert = nav.classList.contains("ouvert");
      toggle.setAttribute("aria-expanded", ouvert ? "true" : "false");
      toggle.setAttribute("aria-label", ouvert ? "Fermer le menu" : "Ouvrir le menu");
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
        "Réception obligatoire à partir du 1er septembre 2026 — plus que " + jours + " jours";
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

  // Captures de l'application sur la page Télécharger
  document.querySelectorAll("[data-carousel]").forEach(function (carousel) {
    var slides = Array.prototype.slice.call(carousel.querySelectorAll("[data-slide]"));
    var dots = Array.prototype.slice.call(carousel.querySelectorAll("[data-carousel-dot]"));
    var current = 0;
    if (slides.length < 2) return;

    function afficher(index) {
      current = (index + slides.length) % slides.length;
      slides.forEach(function (slide, position) {
        var actif = position === current;
        slide.classList.toggle("is-active", actif);
        slide.setAttribute("aria-hidden", actif ? "false" : "true");
      });
      dots.forEach(function (dot, position) {
        var actif = position === current;
        dot.classList.toggle("is-active", actif);
        dot.setAttribute("aria-selected", actif ? "true" : "false");
      });
    }

    var precedent = carousel.querySelector("[data-carousel-prev]");
    var suivant = carousel.querySelector("[data-carousel-next]");
    if (precedent) precedent.addEventListener("click", function () { afficher(current - 1); });
    if (suivant) suivant.addEventListener("click", function () { afficher(current + 1); });
    dots.forEach(function (dot) {
      dot.addEventListener("click", function () { afficher(Number(dot.getAttribute("data-carousel-dot"))); });
    });
    carousel.addEventListener("keydown", function (event) {
      if (event.key === "ArrowLeft") { event.preventDefault(); afficher(current - 1); }
      if (event.key === "ArrowRight") { event.preventDefault(); afficher(current + 1); }
    });
  });
})();
