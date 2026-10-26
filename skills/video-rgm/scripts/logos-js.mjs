#!/usr/bin/env node
// Construit assets/logos.js à partir des SVG de assets/logos/.
// Pourquoi : un logo chargé en <img src="....svg"> n'est pas toujours prêt quand
// HyperFrames capture l'image, et la tuile sort vide dans le MP4. Les tracés
// intégrés dans la page s'affichent dès le montage React, sans chargement.
//   node logos-js.mjs <dossier-projet>
import fs from "node:fs";
import path from "node:path";

const projet = process.argv[2] || ".";
const dossier = path.join(projet, "assets", "logos");
const logos = {};
for (const f of fs.existsSync(dossier) ? fs.readdirSync(dossier) : []) {
  if (!f.endsWith(".svg")) continue;
  const svg = fs.readFileSync(path.join(dossier, f), "utf8");
  const d = [...svg.matchAll(/<path[^>]*\sd="([^"]+)"/g)].map((m) => m[1]);
  const couleur = (svg.match(/<svg[^>]*\sfill="([^"]+)"/) || [])[1] || "#0d1116";
  if (d.length) logos[f.slice(0, -4)] = { d, couleur };
}
fs.writeFileSync(
  path.join(projet, "assets", "logos.js"),
  "// Tracés des logos (Simple Icons, CC0), générés par logos-js.mjs.\nwindow.RGM_LOGOS=" + JSON.stringify(logos) + ";\n",
);
console.log("assets/logos.js : " + Object.keys(logos).length + " logos");
