#!/usr/bin/env node
// Voix off et bruitages ElevenLabs pour les vidéos RGM.
//
// La clé n'apparaît jamais : elle est lue dans $ELEVENLABS_API_KEY ou dans
// ~/.secrets/elevenlabs.env (posé par poser-secret/scripts/poser-elevenlabs.ps1).
//
//   node voix-elevenlabs.mjs --test                       vérifie la clé (code HTTP seulement)
//   node voix-elevenlabs.mjs --liste                      liste les voix du compte
//   node voix-elevenlabs.mjs --texte script.txt --sortie assets/voix [--voix ID]
//        → voix.mp3 + mots.json ([{ mot, debut, fin }]) pour les sous-titres
//   node voix-elevenlabs.mjs --effet "whoosh rapide" --duree 1.2 --sortie assets/sfx/whoosh.mp3
//
// La voix par défaut est gardée dans config.json à côté du skill (un identifiant
// de voix n'est pas un secret).

import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

const ICI = path.dirname(fileURLToPath(import.meta.url));
const CONFIG = path.join(ICI, "..", "config.json");
const API = "https://api.elevenlabs.io/v1";

function arg(nom, defaut) {
  const i = process.argv.indexOf("--" + nom);
  if (i === -1) return defaut;
  const v = process.argv[i + 1];
  return v === undefined || v.startsWith("--") ? true : v;
}

function cle() {
  if (process.env.ELEVENLABS_API_KEY) return process.env.ELEVENLABS_API_KEY.trim();
  const f = path.join(os.homedir(), ".secrets", "elevenlabs.env");
  if (fs.existsSync(f)) {
    const ligne = fs.readFileSync(f, "utf8").split(/\r?\n/).find((l) => l.startsWith("ELEVENLABS_API_KEY="));
    if (ligne) return ligne.slice("ELEVENLABS_API_KEY=".length).trim();
  }
  console.error("Pas de clé ElevenLabs. Lancer : powershell -ExecutionPolicy Bypass -File ~/.claude/skills/poser-secret/scripts/poser-elevenlabs.ps1");
  process.exit(2);
}

function lireConfig() {
  try { return JSON.parse(fs.readFileSync(CONFIG, "utf8")); } catch { return {}; }
}

async function appel(chemin, options = {}) {
  const r = await fetch(API + chemin, { ...options, headers: { "xi-api-key": cle(), ...(options.headers || {}) } });
  if (!r.ok) {
    let detail = "";
    try { detail = JSON.stringify((await r.json()).detail).slice(0, 300); } catch {}
    console.error("ElevenLabs a répondu HTTP " + r.status + " " + detail);
    process.exit(1);
  }
  return r;
}

// Caractères horodatés → mots horodatés.
function versMots(al) {
  const mots = [];
  let cour = null;
  al.characters.forEach((c, i) => {
    if (/\s/.test(c)) { if (cour) { mots.push(cour); cour = null; } return; }
    if (!cour) cour = { mot: "", debut: al.character_start_times_seconds[i], fin: 0 };
    cour.mot += c;
    cour.fin = al.character_end_times_seconds[i];
  });
  if (cour) mots.push(cour);
  return mots.map((m) => ({ mot: m.mot, debut: +m.debut.toFixed(3), fin: +m.fin.toFixed(3) }));
}

async function main() {
  if (arg("test")) {
    const r = await appel("/voices");
    console.log("Clé ElevenLabs OK (HTTP " + r.status + ")");
    return;
  }

  if (arg("liste")) {
    const { voices } = await (await appel("/voices")).json();
    for (const v of voices) {
      const l = v.labels || {};
      console.log(v.voice_id + "  " + v.name.padEnd(28) + " " + [l.gender, l.accent, l.language, l.age, l.use_case].filter(Boolean).join(", "));
    }
    return;
  }

  const effet = arg("effet");
  if (effet) {
    const sortie = arg("sortie", "effet.mp3");
    const corps = { text: effet, prompt_influence: 0.4 };
    const duree = arg("duree");
    if (duree) corps.duration_seconds = Number(duree);
    const r = await appel("/sound-generation", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(corps) });
    fs.mkdirSync(path.dirname(path.resolve(sortie)), { recursive: true });
    fs.writeFileSync(sortie, Buffer.from(await r.arrayBuffer()));
    console.log("Effet écrit : " + sortie);
    return;
  }

  const fichierTexte = arg("texte");
  if (!fichierTexte) { console.error("Usage : --test | --liste | --texte script.txt --sortie dossier [--voix ID] | --effet \"...\""); process.exit(2); }
  const texte = fs.readFileSync(fichierTexte, "utf8").trim();
  const config = lireConfig();
  const voix = arg("voix") || config.voix;
  if (!voix || voix === true) { console.error("Aucune voix choisie : lancer --liste puis passer --voix ID (elle sera gardée comme voix par défaut)."); process.exit(2); }
  const modele = arg("modele", config.modele || "eleven_multilingual_v2");

  const r = await appel("/text-to-speech/" + voix + "/with-timestamps?output_format=mp3_44100_128", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      text: texte,
      model_id: modele,
      ...(/flash|turbo|v3/.test(modele) ? { language_code: "fr" } : {}),
      voice_settings: { stability: 0.45, similarity_boost: 0.8, style: 0.25, use_speaker_boost: true },
    }),
  });
  const json = await r.json();
  const dossier = arg("sortie", ".");
  fs.mkdirSync(dossier, { recursive: true });
  fs.writeFileSync(path.join(dossier, "voix.mp3"), Buffer.from(json.audio_base64, "base64"));
  const mots = versMots(json.normalized_alignment || json.alignment);
  fs.writeFileSync(path.join(dossier, "mots.json"), JSON.stringify(mots, null, 1));
  if (arg("voix")) fs.writeFileSync(CONFIG, JSON.stringify({ ...config, voix, modele }, null, 2));
  const fin = mots.length ? mots[mots.length - 1].fin : 0;
  console.log("Voix écrite : " + path.join(dossier, "voix.mp3") + " (" + fin.toFixed(2) + " s, " + mots.length + " mots)");
}

main().catch((e) => { console.error(e.message); process.exit(1); });
