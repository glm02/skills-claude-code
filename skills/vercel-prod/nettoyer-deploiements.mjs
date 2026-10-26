#!/usr/bin/env node
// Supprime les plus anciens déploiements d'un projet Vercel quand le stockage sature.
//
//   node nettoyer-deploiements.mjs --projet atout-travaux            # simulation
//   node nettoyer-deploiements.mjs --projet atout-travaux --garder 30 --appliquer
//
// Pourquoi : en octobre 2026 le stockage des déploiements d'Atout Travaux était
// plein et un nettoyage mal ciblé a touché autre chose que les vieux
// déploiements. Ici on ne supprime que les plus anciens, jamais la production
// en cours, jamais ceux des dernières 48 h, et rien sans --appliquer.
// Le jeton est celui de la CLI Vercel (lancer `vercel whoami` avant pour le
// rafraîchir) ; il n'est jamais affiché.
import { readFileSync } from "node:fs";
import { join } from "node:path";

const args = process.argv.slice(2);
const opt = (n, d) => { const i = args.indexOf(`--${n}`); return i < 0 ? d : args[i + 1]; };
const projet = opt("projet");
const garder = Number(opt("garder", 20));
const appliquer = args.includes("--appliquer");
if (!projet) { console.error("Usage : --projet <nom> [--garder 20] [--appliquer]"); process.exit(1); }

const data = join(process.env.APPDATA ?? join(process.env.HOME, ".local/share"), "com.vercel.cli", "Data");
const { token } = JSON.parse(readFileSync(join(data, "auth.json"), "utf8"));
const { currentTeam } = JSON.parse(readFileSync(join(data, "config.json"), "utf8"));
const equipe = currentTeam ? `teamId=${currentTeam}` : "";

async function api(chemin, methode = "GET") {
  const sep = chemin.includes("?") ? "&" : "?";
  const r = await fetch(`https://api.vercel.com${chemin}${equipe ? sep + equipe : ""}`, {
    method: methode, headers: { Authorization: `Bearer ${token}` },
  });
  if (!r.ok) throw new Error(`${methode} ${chemin.split("?")[0]} → HTTP ${r.status}`);
  return r.json();
}

const p = await api(`/v9/projects/${encodeURIComponent(projet)}`);
const prodActuelle = p.targets?.production?.id;

let tous = [], avant;
do {
  const page = await api(`/v6/deployments?projectId=${p.id}&limit=100${avant ? `&until=${avant}` : ""}`);
  tous.push(...page.deployments);
  avant = page.pagination?.next;
} while (avant);

tous.sort((a, b) => b.created - a.created); // du plus récent au plus ancien
const limite48h = Date.now() - 48 * 3600 * 1000;
const proteges = new Set(tous.slice(0, garder).map(d => d.uid));
if (prodActuelle) proteges.add(prodActuelle);
const aSupprimer = tous.filter(d => !proteges.has(d.uid) && d.created < limite48h).reverse(); // plus anciens d'abord

const jour = t => new Date(t).toISOString().slice(0, 10);
console.log(`${projet} : ${tous.length} déploiements, production actuelle ${prodActuelle ?? "inconnue"}`);
console.log(`Gardés : ${tous.length - aSupprimer.length} · À supprimer : ${aSupprimer.length}` +
  (aSupprimer.length ? ` (du ${jour(aSupprimer[0].created)} au ${jour(aSupprimer.at(-1).created)})` : ""));

if (!appliquer) { console.log("Simulation : rien supprimé. Relancer avec --appliquer."); process.exit(0); }
let ok = 0;
for (const d of aSupprimer) {
  try { await api(`/v13/deployments/${d.uid}`, "DELETE"); ok++; }
  catch (e) { console.error(`Échec ${d.uid} : ${e.message}`); }
}
console.log(`${ok}/${aSupprimer.length} supprimés.`);
