#!/usr/bin/env node
// Captures téléphone + ordinateur d'une ou plusieurs pages, et détection des
// défauts de mise en page qui reviennent le plus sur les sites de Rafaël.
//
//   node captures.mjs <dossier-sortie> <url> [url ...]
//
// Pour chaque page et chaque largeur (390 px téléphone, 1440 px ordinateur) :
// une capture pleine page, puis un rapport JSON des défauts :
//   - débordement horizontal (la page défile de côté sur téléphone) ;
//   - éléments plus larges que l'écran ;
//   - textes qui se chevauchent (deux blocs de texte visibles qui se couvrent) ;
//   - cibles tactiles trop petites (< 40 px) sur téléphone ;
//   - images cassées.
// Les apparitions au défilement sont forcées visibles avant la capture.
import { chromium } from "playwright";
import { mkdirSync, writeFileSync } from "node:fs";
import { join } from "node:path";

const [sortie, ...urls] = process.argv.slice(2);
if (!sortie || !urls.length) {
  console.error("Usage : node captures.mjs <dossier-sortie> <url> [url ...]");
  process.exit(1);
}
mkdirSync(sortie, { recursive: true });

const LARGEURS = [["mobile", 390, 844], ["ordi", 1440, 900]];
// Un navigateur déjà installé (Chrome, sinon Brave) : rien à télécharger.
const BRAVE = "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe";
const navigateur = await chromium.launch({ channel: "chrome" })
  .catch(() => chromium.launch({ executablePath: BRAVE }))
  .catch(() => chromium.launch());
const rapport = [];

for (const url of urls) {
  for (const [nom, largeur, hauteur] of LARGEURS) {
    const page = await navigateur.newPage({
      viewport: { width: largeur, height: hauteur },
      deviceScaleFactor: 1,
      isMobile: nom === "mobile",
      hasTouch: nom === "mobile",
    });
    const erreurs = [];
    page.on("pageerror", (e) => erreurs.push(String(e.message).slice(0, 200)));
    // "load" puis une pause : les sites avec statistiques ou chat n'atteignent jamais "networkidle".
    await page.goto(url, { waitUntil: "load", timeout: 45000 }).catch((e) => erreurs.push(`chargement : ${e.message.split("\n")[0]}`));
    await page.waitForTimeout(1500);
    // Défiler jusqu'en bas déclenche le chargement paresseux et les animations d'entrée.
    await page.evaluate(async () => {
      // behavior "instant" : avec scroll-behavior: smooth, la mesure tomberait en plein défilement.
      for (let y = 0; y < document.body.scrollHeight; y += 600) { window.scrollTo({ top: y, behavior: "instant" }); await new Promise((r) => setTimeout(r, 80)); }
      window.scrollTo({ top: 0, behavior: "instant" });
      document.querySelectorAll(".reveal, [data-reveal], [data-aos], .fade-in").forEach((e) => {
        e.classList.add("visible", "is-visible", "in", "aos-animate"); e.style.opacity = "1"; e.style.transform = "none";
      });
    });
    await page.waitForTimeout(700);

    const defauts = await page.evaluate((mobile) => {
      const vw = document.documentElement.clientWidth;
      const res = { debordement: document.documentElement.scrollWidth - vw, tropLarges: [], chevauchements: [], ciblesPetites: [], imagesCassees: [] };
      const nomEl = (e) => e.tagName.toLowerCase() + (e.id ? `#${e.id}` : "") + (e.className && typeof e.className === "string" ? "." + e.className.trim().split(/\s+/).slice(0, 2).join(".") : "");
      // Visible = affiché, non transparent, et pas entièrement caché par un parent qui coupe
      // (FAQ repliée en max-height: 0, carrousel, menu fermé).
      const visible = (e) => {
        const s = getComputedStyle(e); const r = e.getBoundingClientRect();
        if (s.visibility === "hidden" || s.display === "none" || +s.opacity <= 0.05 || r.width === 0 || r.height === 0) return false;
        for (let p = e.parentElement; p && p !== document.body; p = p.parentElement) {
          const o = getComputedStyle(p);
          if (+o.opacity <= 0.05) return false;
          if (/(hidden|clip|auto|scroll)/.test(o.overflow + o.overflowY)) {
            const q = p.getBoundingClientRect();
            if (r.bottom <= q.top + 1 || r.top >= q.bottom - 1 || r.right <= q.left + 1 || r.left >= q.right - 1) return false;
          }
        }
        return true;
      };
      const flottant = (e) => { for (let p = e; p && p !== document.body; p = p.parentElement) if (/fixed|sticky/.test(getComputedStyle(p).position)) return true; return false; };
      // Un élément large dans un parent qui coupe (bandeau défilant, carrousel) est voulu.
      const coupe = (e) => { for (let p = e.parentElement; p && p !== document.body; p = p.parentElement) { const o = getComputedStyle(p); if (/(hidden|clip|auto|scroll)/.test(o.overflowX + o.overflow)) return true; } return false; };
      const signales = [];
      for (const e of document.body.querySelectorAll("*")) {
        const r = e.getBoundingClientRect();
        if (visible(e) && r.right > vw + 2 && getComputedStyle(e).position !== "fixed" && !coupe(e) && !signales.some((s) => s.contains(e)) && res.tropLarges.length < 15) {
          signales.push(e); res.tropLarges.push(`${nomEl(e)} (droite à ${Math.round(r.right)} px)`);
        }
      }
      // Blocs de texte « feuilles » : éléments qui portent eux-mêmes du texte.
      const textes = [...document.body.querySelectorAll("h1,h2,h3,h4,p,li,a,button,span,label")]
        .filter((e) => visible(e) && [...e.childNodes].some((n) => n.nodeType === 3 && n.textContent.trim().length > 1))
        // En-têtes fixes et lien d'accessibilité « Aller au contenu » : superposés par conception.
        .filter((e) => !flottant(e) && !e.closest("header, nav, .sr-only") && !/aller au contenu|skip to/i.test(e.textContent))
        .map((e) => ({ e, r: e.getBoundingClientRect() }));
      for (let i = 0; i < textes.length && res.chevauchements.length < 15; i++) {
        for (let j = i + 1; j < textes.length; j++) {
          const a = textes[i], b = textes[j];
          if (a.e.contains(b.e) || b.e.contains(a.e)) continue;
          const x = Math.min(a.r.right, b.r.right) - Math.max(a.r.left, b.r.left);
          const y = Math.min(a.r.bottom, b.r.bottom) - Math.max(a.r.top, b.r.top);
          if (x > 6 && y > 6) { res.chevauchements.push(`${nomEl(a.e)} « ${a.e.textContent.trim().slice(0, 30)} » ⟷ ${nomEl(b.e)} « ${b.e.textContent.trim().slice(0, 30)} »`); break; }
        }
      }
      if (mobile) {
        for (const e of document.querySelectorAll("a, button, input, select, [role=button]")) {
          const r = e.getBoundingClientRect();
          if (visible(e) && (r.width < 40 || r.height < 40) && r.width > 0 && res.ciblesPetites.length < 15) res.ciblesPetites.push(`${nomEl(e)} ${Math.round(r.width)}×${Math.round(r.height)}`);
        }
      }
      for (const img of document.images) if (img.complete && img.naturalWidth === 0 && img.src) res.imagesCassees.push(img.src.slice(0, 120));
      return res;
    }, nom === "mobile");

    const fichier = join(sortie, `${new URL(url).pathname.replace(/[^a-z0-9]+/gi, "-").replace(/^-|-$/g, "") || "accueil"}-${nom}.png`);
    await page.screenshot({ path: fichier, fullPage: true });
    rapport.push({ url, largeur: nom, capture: fichier, erreursJs: erreurs, ...defauts });
    await page.close();
  }
}
await navigateur.close();
writeFileSync(join(sortie, "rapport.json"), JSON.stringify(rapport, null, 2));

for (const r of rapport) {
  const n = (r.debordement > 2 ? 1 : 0) + r.tropLarges.length + r.chevauchements.length + r.imagesCassees.length + r.erreursJs.length;
  console.log(`${r.largeur.padEnd(6)} ${r.url} → ${n ? `${n} défaut(s)` : "rien d'évident"}` +
    (r.debordement > 2 ? ` · défile de côté de ${r.debordement} px` : "") +
    (r.chevauchements.length ? ` · ${r.chevauchements.length} chevauchement(s)` : "") +
    (r.ciblesPetites.length ? ` · ${r.ciblesPetites.length} cible(s) tactile(s) petite(s)` : ""));
}
console.log(`Rapport détaillé : ${join(sortie, "rapport.json")}`);
