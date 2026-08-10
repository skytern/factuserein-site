# FactuSerein Front Reassurance Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reposition the public website for anxious, time-poor TPE owners with a simple human-first PDF-only message.

**Architecture:** Keep the existing static HTML/CSS/JS architecture. Update public copy and the homepage hero without adding a frontend framework or external logo dependency. Preserve existing routes and sector pages.

**Tech Stack:** Static HTML, existing `assets/css/style.css`, existing `assets/js/main.js`, Python static-server validation.

## Global Constraints

- Public input format is **PDF only**.
- Remove public references to Excel, Word, Excel conversion, XML, Factur-X, UBL and CII from commercial messaging.
- Use « format électronique conforme aux règles françaises » and « vérification avant transmission ».
- Do not use an administration logo or imply government certification.
- Use the owner brand badge « Prêt pour la facturation électronique ».
- Position the service as human support from Aix-en-Provence, using `contact@factuserein.fr`; do not invent a phone number.
- Keep SEO terms in headings and sector guides: facturation électronique TPE, métier, logiciel et Aix-en-Provence.

---

### Task 1: Replace technical and obsolete public copy

**Files:**
- Modify: `index.html`
- Modify: `comment-ca-marche.html`
- Modify: `tarifs.html`
- Modify: `secteurs/btp.html`
- Modify: `secteurs/sante.html`
- Modify: `secteurs/restauration.html`
- Modify: `outils/validateur.html`

- [ ] Replace the homepage hero paragraph with: `Vous déposez vos factures PDF. Nous vous accompagnons jusqu'à leur transmission conforme, avec un interlocuteur humain basé à Aix-en-Provence.`
- [ ] Replace the homepage hero title with: `Vos factures électroniques, sans changer vos habitudes.`
- [ ] Replace the hero primary CTA with `Être accompagné` and keep the secondary CTA `Voir les tarifs`.
- [ ] Replace the first problem card with `Vous avez peur de mal faire` and text explaining that FactuSerein checks the information before transmission.
- [ ] Replace every public sentence containing Excel, Word, `.xlsx`, `.xls` or conversion from those formats with PDF-only wording.
- [ ] Replace visible Factur-X, UBL and CII references with `format électronique conforme aux règles françaises`.
- [ ] Replace technical validator headings with `Vérifier une facture électronique` and `Contrôle des informations avant transmission`.
- [ ] Keep sector software names only where they support SEO intent; describe the action as `déposer vos PDF sans changer votre logiciel`.
- [ ] Remove the public claim `SUPER PDP` from generic footer copy; use `Transmission via une plateforme agréée partenaire` until a reseller agreement is finalized.

### Task 2: Simplify the visual direction

**Files:**
- Modify: `index.html`
- Modify: `assets/css/style.css`

- [ ] Replace the fake technical split-view hero illustration with a calm trust card containing: green check icon, `Accompagnement humain`, `PDF uniquement`, and `Depuis Aix-en-Provence`.
- [ ] Change the hero background to a light green/blue gradient and hero text to the existing dark blue text color.
- [ ] Keep one strong green CTA and one neutral secondary CTA.
- [ ] Add a trust strip under the hero: `PDF uniquement` · `Vérification avant envoi` · `Un interlocuteur humain`.
- [ ] Keep the existing responsive layout and mobile menu.
- [ ] Do not add an external image or unofficial government logo.

### Task 3: Verify content and rendering

**Files:**
- Test: all HTML files under `factuserein-site`

- [ ] Run a text scan excluding legal/archive documents and confirm no public page contains `Excel`, `Word`, `Factur-X`, `UBL` or `CII` in the commercial sections.
- [ ] Run the existing internal-link scan across all HTML pages.
- [ ] Serve the site with `python -m http.server 8080 --directory factuserein-site`.
- [ ] Verify HTTP 200 for `index.html`, `tarifs.html`, `comment-ca-marche.html`, all three sector pages and `outils/validateur.html`.
- [ ] Verify the homepage contains `FactuSerein`, `PDF`, `Aix-en-Provence` and `facturation électronique`.

### Task 4: Version the front change

**Files:**
- Commit all intended files in `factuserein-site` only.

- [ ] Inspect `git diff` and ensure no generated files or secrets are staged.
- [ ] Commit with message: `refactor: simplify FactuSerein front for TPE PDF-only offer`.
- [ ] Push `main` to `skytern/factuserein-site`.
