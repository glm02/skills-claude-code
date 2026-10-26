// Bibliothèque de composants React pour les vidéos HyperFrames de RGM Dev.
//
// Chargée après React 18, ReactDOM 18, htm et GSAP (UMD). Chaque composant ne
// fait que du rendu : l'animation passe par les fonctions `RGM.anim.*`, qui
// ajoutent des tweens à la timeline GSAP de la composition. Ainsi chaque image
// reste une fonction du temps, comme HyperFrames l'exige.
//
// Usage :
//   RGM.monter("hote-id", RGM.html`<${RGM.Telephone} ...>`);   // rendu synchrone
//   RGM.anim.conversation(tl, "#tel", 2.0);                     // animation

(function () {
  const html = htm.bind(React.createElement);

  // ---------- Outils ----------

  function monter(id, element) {
    const racine = ReactDOM.createRoot(document.getElementById(id));
    ReactDOM.flushSync(() => racine.render(element));
  }

  // Hasard reproductible : même rendu à chaque fois.
  function alea(graine) {
    let a = graine | 0;
    return function () {
      a = (a + 0x6d2b79f5) | 0;
      let t = Math.imul(a ^ (a >>> 15), 1 | a);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }

  const Coche = ({ taille = 26 }) => html`
    <svg viewBox="0 0 24 24" width=${taille} height=${taille} fill="none" stroke="#fff" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>`;

  const Fleche = ({ taille = 44 }) => html`
    <svg viewBox="0 0 24 24" width=${taille} height=${taille} fill="none" stroke="#fff" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>`;

  // ---------- Logos ----------

  // Tracé intégré (assets/logos.js) : un <img> SVG peut ne pas être chargé à la
  // capture et laisser la tuile vide. L'<img> ne reste qu'en secours.
  function logoSvg(slug, t) {
    const l = (window.RGM_LOGOS || {})[slug];
    if (!l) return html`<img src=${"assets/logos/" + slug + ".svg"} alt="" style=${{ width: t, height: t }} />`;
    return html`<svg viewBox="0 0 24 24" width=${t} height=${t} fill=${l.couleur} aria-hidden="true">${l.d.map((d, i) => html`<path key=${i} d=${d} />`)}</svg>`;
  }

  // Un vrai logo (Simple Icons) dans sa tuile blanche. `slug` = nom du fichier dans assets/logos/.
  function Logo({ slug, taille = 120, id, classe = "", etiquette }) {
    return html`
      <div className=${"rgm-logo " + classe} id=${id} style=${{ width: taille, height: taille, borderRadius: taille * 0.28 }}>
        ${logoSvg(slug, taille * 0.54)}
        ${etiquette ? html`<span className="rgm-logo-etiquette">${etiquette}</span>` : null}
      </div>`;
  }

  // Le logo RGM Dev (assets/logo.svg) en tuile bleue.
  function LogoRGM({ taille = 160, id, classe = "" }) {
    return html`<img className=${"rgm-logo-rgm " + classe} id=${id} src="assets/logo.svg" alt="" style=${{ width: taille, height: taille, borderRadius: taille * 0.22 }} />`;
  }

  // Logos disposés en cercle autour d'un centre ; RGM.anim.orbite les fait tourner.
  function OrbiteLogos({ id, logos, rayon = 330, taille = 120, centre }) {
    return html`
      <div className="rgm-orbite" id=${id} data-rayon=${rayon}>
        <div className="rgm-orbite-anneau" style=${{ width: rayon * 2, height: rayon * 2, marginLeft: -rayon, marginTop: -rayon }}></div>
        ${logos.map((slug, i) => html`
          <div key=${slug} className="rgm-orbite-item" data-i=${i} data-n=${logos.length}>
            <${Logo} slug=${slug} taille=${taille} />
          </div>`)}
        <div className="rgm-orbite-centre">${centre}</div>
      </div>`;
  }

  // Bandeau de logos qui défile (RGM.anim.defilement).
  function BandeLogos({ id, logos, taille = 110 }) {
    const serie = logos.concat(logos);
    return html`
      <div className="rgm-bande" id=${id}>
        <div className="rgm-bande-piste">${serie.map((s, i) => html`<${Logo} key=${i} slug=${s} taille=${taille} />`)}</div>
      </div>`;
  }

  // ---------- Flux d'automatisation façon n8n ----------

  // entrees / sorties : [{ slug, label }]. Le centre est l'agent.
  // RGM.anim.flux trace les liens puis fait circuler des paquets.
  function FluxAgent({ id, entrees, sorties, largeur = 940, hauteur = 760, nomAgent = "Agent IA" }) {
    const x0 = 110, x1 = largeur / 2, x2 = largeur - 110;
    const ys = (n) => Array.from({ length: n }, (_, i) => (hauteur / (n + 1)) * (i + 1));
    const ye = ys(entrees.length), yso = ys(sorties.length), yc = hauteur / 2;
    const courbe = (xa, ya, xb, yb) => {
      const dx = (xb - xa) * 0.5;
      return "M" + xa + "," + ya + " C" + (xa + dx) + "," + ya + " " + (xb - dx) + "," + yb + " " + xb + "," + yb;
    };
    const liens = [
      ...entrees.map((e, i) => ({ d: courbe(x0 + 60, ye[i], x1 - 100, yc), sens: "in", i })),
      ...sorties.map((s, i) => ({ d: courbe(x1 + 100, yc, x2 - 60, yso[i]), sens: "out", i })),
    ];
    const noeud = (n, x, y, cle) => html`
      <div key=${cle} className="rgm-flux-noeud" data-cle=${cle} style=${{ left: x - 60, top: y - 60 }}>
        <${Logo} slug=${n.slug} taille=${120} />
        <span className="rgm-flux-label">${n.label}</span>
      </div>`;
    return html`
      <div className="rgm-flux" id=${id} style=${{ width: largeur, height: hauteur }}>
        <svg className="rgm-flux-svg" width=${largeur} height=${hauteur} viewBox=${"0 0 " + largeur + " " + hauteur}>
          ${liens.map((l, k) => html`<path key=${"f" + k} className="rgm-flux-fond" d=${l.d} />`)}
          ${liens.map((l, k) => html`<path key=${"l" + k} className=${"rgm-flux-lien rgm-" + l.sens} d=${l.d} />`)}
          ${liens.map((l, k) => html`<circle key=${"p" + k} className=${"rgm-flux-paquet rgm-p-" + l.sens} r="11" cx="0" cy="0" style=${{ opacity: 0 }} />`)}
        </svg>
        ${entrees.map((n, i) => noeud(n, x0, ye[i], "e" + i))}
        ${sorties.map((n, i) => noeud(n, x2, yso[i], "s" + i))}
        <div className="rgm-flux-agent" style=${{ left: x1 - 100, top: yc - 100 }}>
          <div className="rgm-flux-halo"></div>
          <img src="assets/logo.svg" alt="" />
          <span className="rgm-flux-label">${nomAgent}</span>
        </div>
      </div>`;
  }

  // ---------- Téléphone et messagerie ----------

  // messages : [{ de: "client" | "agent", texte, html? }]. RGM.anim.conversation les joue.
  function Telephone({ id, heure = "23:47", nom = "Votre agent IA", statut = "en ligne · 24 h/24", app, messages = [], carte }) {
    return html`
      <div className="rgm-tel" id=${id}>
        <div className="rgm-tel-statut"><span className="rgm-tel-heure">${heure}</span><i className="rgm-tel-ilot"></i><span>100 %</span></div>
        <div className="rgm-tel-entete">
          ${app ? html`<${Logo} slug=${app} taille=${76} />` : html`<img src="assets/logo.svg" alt="" className="rgm-tel-avatar" />`}
          <div><div className="rgm-tel-nom">${nom}</div><div className="rgm-tel-etat"><i></i>${statut}</div></div>
        </div>
        <div className="rgm-tel-fil">
          ${messages.map((m, i) => html`
            <div key=${i} className=${"rgm-msg rgm-" + m.de} data-i=${i}>
              ${m.de === "agent" ? html`<div className="rgm-frappe"><i></i><i></i><i></i></div>` : null}
              <div className="rgm-bulle" dangerouslySetInnerHTML=${{ __html: m.html || m.texte }}></div>
            </div>`)}
          ${carte ? html`<div className="rgm-tel-carte">${carte}</div>` : null}
        </div>
      </div>`;
  }

  // Notification façon iOS, avec le vrai logo de l'application.
  function Notification({ id, slug, app, titre, texte, quand = "maintenant" }) {
    return html`
      <div className="rgm-notif" id=${id}>
        ${slug ? html`<${Logo} slug=${slug} taille=${88} />` : html`<img src="assets/logo.svg" alt="" className="rgm-notif-rgm" />`}
        <div className="rgm-notif-corps">
          <div className="rgm-notif-l1"><span className="rgm-notif-app">${app}</span><span className="rgm-notif-quand">${quand}</span></div>
          <div className="rgm-notif-titre">${titre}</div>
          <div className="rgm-notif-texte">${texte}</div>
        </div>
      </div>`;
  }

  // ---------- Code ----------

  function jetons(source) {
    const motif = /("[^"]*")|\b(const|await|async|return|import|from)\b|(\w+)(?=\()|(\w+)(?=:)|([{}()[\],;.:=])/g;
    const sortie = [];
    let dernier = 0, m;
    while ((m = motif.exec(source))) {
      if (m.index > dernier) sortie.push([source.slice(dernier, m.index), ""]);
      sortie.push([m[0], m[1] ? "str" : m[2] ? "kw" : m[3] ? "fn" : m[4] ? "prop" : "punc"]);
      dernier = m.index + m[0].length;
    }
    if (dernier < source.length) sortie.push([source.slice(dernier), ""]);
    return sortie;
  }

  // Éditeur sombre ; RGM.anim.frappe tape le code caractère par caractère.
  function Editeur({ id, fichier = "agent.ts", code }) {
    let i = 0;
    const cars = [];
    for (const [texte, classe] of jetons(code)) {
      for (const c of texte) { cars.push(html`<span key=${i++} className=${"rgm-ch" + (classe ? " rgm-t-" + classe : "")}>${c}</span>`); }
    }
    return html`
      <div className="rgm-editeur" id=${id}>
        <div className="rgm-editeur-barre"><i></i><i></i><i></i><span>${fichier}</span></div>
        <pre className="rgm-code">${cars}<span className="rgm-curseur"></span></pre>
      </div>`;
  }

  // Terminal : lignes qui s'affichent une à une (RGM.anim.lignes).
  function Terminal({ id, lignes }) {
    return html`
      <div className="rgm-terminal" id=${id}>
        <div className="rgm-editeur-barre"><i></i><i></i><i></i><span>terminal</span></div>
        <div className="rgm-terminal-corps">
          ${lignes.map((l, i) => html`<div key=${i} className=${"rgm-ligne" + (l.ok ? " rgm-ok" : "")}>${l.ok ? "✓ " : "$ "}${l.texte}</div>`)}
        </div>
      </div>`;
  }

  // ---------- Cartes ----------

  // Cadre au liseré lumineux tournant (border-beam du site) ; RGM.anim.faisceau le fait tourner.
  function Faisceau({ id, largeur, hauteur, children, sombre = false }) {
    return html`
      <div className="rgm-faisceau" id=${id} style=${{ width: largeur, height: hauteur }}>
        <div className=${"rgm-faisceau-int" + (sombre ? " rgm-sombre" : "")}>${children}</div>
      </div>`;
  }

  // Carte d'offre : reprendre les vraies valeurs de src/lib/contenu-defaut.ts.
  function CarteOffre({ nom, prixMin, prixMax, delai, inclus }) {
    return html`
      <div className="rgm-offre">
        <span className="rgm-badge">${nom}</span>
        <div className="rgm-prix"><span className="rgm-prix-min" data-valeur=${prixMin}>${prixMin.toLocaleString("fr-FR")}</span> – ${prixMax.toLocaleString("fr-FR")} €</div>
        <div className="rgm-delai">${delai}</div>
        <hr />
        <ul>${inclus.map((t, i) => html`<li key=${i} className="rgm-inclus"><span className="rgm-ok"><${Coche} /></span>${t}</li>`)}</ul>
      </div>`;
  }

  // Grand chiffre animé (RGM.anim.compteur).
  function Compteur({ id, valeur, suffixe = "", legende }) {
    return html`
      <div className="rgm-compteur" id=${id}>
        <div className="rgm-compteur-val"><span className="rgm-compteur-n" data-valeur=${valeur}>0</span><small>${suffixe}</small></div>
        ${legende ? html`<div className="rgm-compteur-legende">${legende}</div>` : null}
      </div>`;
  }

  // Liste de tâches qui se cochent (RGM.anim.cocher).
  function ListeTaches({ id, taches }) {
    return html`
      <div className="rgm-taches" id=${id}>
        ${taches.map((t, i) => html`
          <div key=${i} className="rgm-tache">
            <span className="rgm-case"><span className="rgm-coche"><${Coche} taille=${32} /></span></span>
            ${t.slug ? html`<${Logo} slug=${t.slug} taille=${64} />` : null}
            <span className="rgm-tache-lib">${t.texte}<i className="rgm-rature"></i></span>
            ${t.duree ? html`<span className="rgm-tache-duree">${t.duree}</span>` : null}
          </div>`)}
      </div>`;
  }

  // ---------- Texte ----------

  // Titre découpé en mots (RGM.anim.mots). Les mots entre *étoiles* passent en bleu.
  function Titre({ id, texte, taille = 96, classe = "" }) {
    const lignes = texte.split("\n");
    return html`
      <div className=${"rgm-titre " + classe} id=${id} style=${{ fontSize: taille }}>
        ${lignes.map((l, i) => html`
          <span key=${i} className="rgm-titre-ligne">
            ${l.split(" ").map((m, j) => {
              const bleu = /^\*.*\*[.,!?]?$/.test(m);
              return html`<span key=${j} className=${"rgm-mot" + (bleu ? " rgm-bleu" : "")}>${m.replace(/\*/g, "")}</span>`;
            }).reduce((acc, el, k) => (k ? acc.concat([" ", el]) : [el]), [])}
          </span>`)}
      </div>`;
  }

  // Sous-titres à partir des mots horodatés d'ElevenLabs (scripts/voix-elevenlabs.mjs → mots.json).
  // groupes : [[{ mot, debut, fin }, ...], ...] ; RGM.anim.sousTitres les synchronise.
  function SousTitres({ id, groupes }) {
    return html`
      <div className="rgm-st" id=${id}>
        ${groupes.map((g, i) => html`
          <div key=${i} className="rgm-st-groupe" data-debut=${g[0].debut} data-fin=${g[g.length - 1].fin}>
            ${g.map((m, j) => html`<span key=${j} className="rgm-st-mot" data-debut=${m.debut}>${m.mot} </span>`)}
          </div>`)}
      </div>`;
  }

  function Bouton({ id, texte = "Demander un devis" }) {
    return html`<div className="rgm-bouton" id=${id}>${texte} <${Fleche} /></div>`;
  }

  function Toast({ id, texte, slug }) {
    return html`
      <div className="rgm-toast" id=${id}>
        ${slug ? html`<${Logo} slug=${slug} taille=${56} />` : html`<span className="rgm-toast-point"><i className="rgm-ping"></i><i></i></span>`}
        ${texte}
      </div>`;
  }

  // ---------- Animations (ajoutées à la timeline GSAP) ----------

  const anim = {
    // Mots d'un titre : montée + flou, l'un après l'autre.
    mots(tl, sel, t, { pas = 0.08, duree = 0.45 } = {}) {
      tl.from(sel + " .rgm-mot", { yPercent: 70, opacity: 0, filter: "blur(10px)", duration: duree, ease: "power3.out", stagger: pas }, t);
    },

    // Code tapé ; renvoie la fin de la frappe.
    frappe(tl, sel, t, duree) {
      const racine = document.querySelector(sel);
      const cars = Array.from(racine.querySelectorAll(".rgm-ch"));
      const curseur = racine.querySelector(".rgm-curseur");
      const pos = cars.map((c) => [c.offsetLeft + c.offsetWidth, c.offsetTop + 8]);
      const p = { n: 0 };
      const peindre = () => {
        const n = Math.floor(p.n);
        for (let k = 0; k < cars.length; k++) cars[k].style.opacity = k < n ? 1 : 0;
        const q = n ? pos[n - 1] : [40, 48];
        curseur.style.transform = "translate(" + q[0] + "px," + q[1] + "px)";
      };
      tl.to(p, { n: cars.length, duration: duree, ease: "none", onUpdate: peindre }, t);
      peindre(); // état initial, posé tout de suite (un tl.call ne se déclenche pas toujours en seek)
      return t + duree;
    },

    // Lignes de terminal une à une.
    lignes(tl, sel, t, pas = 0.45) {
      tl.from(sel + " .rgm-ligne", { opacity: 0, x: -20, duration: 0.2, ease: "power2.out", stagger: pas }, t);
    },

    // Conversation : messages client, indicateur de frappe, réponses de l'agent.
    // temps : instants d'apparition de chaque message (en secondes).
    conversation(tl, sel, temps, { frappe = 0.8 } = {}) {
      const msgs = document.querySelectorAll(sel + " .rgm-msg");
      msgs.forEach((m, i) => {
        const t = temps[i];
        const agent = m.classList.contains("rgm-agent");
        if (!agent) {
          tl.from(m, { y: 30, opacity: 0, scale: 0.94, transformOrigin: "right bottom", duration: 0.35, ease: "power3.out" }, t);
        } else {
          tl.from(m, { opacity: 0, duration: 0.2 }, t - frappe);
          tl.from(m.querySelectorAll(".rgm-frappe i"), { y: -8, duration: 0.2, ease: "sine.inOut", yoyo: true, repeat: Math.max(1, Math.floor(frappe / 0.4)), stagger: 0.1 }, t - frappe + 0.05);
          tl.to(m.querySelector(".rgm-frappe"), { opacity: 0, duration: 0.12 }, t);
          tl.from(m.querySelector(".rgm-bulle"), { opacity: 0, y: 16, duration: 0.3, ease: "power3.out" }, t);
        }
      });
      const carte = document.querySelector(sel + " .rgm-tel-carte");
      if (carte && temps[msgs.length] != null) {
        tl.from(carte, { y: 40, opacity: 0, scale: 0.9, duration: 0.45, ease: "back.out(1.8)" }, temps[msgs.length]);
      }
    },

    // Notifications empilées : chaque nouvelle pousse les précédentes vers le bas.
    pile(tl, ids, temps, ecart = 186) {
      ids.forEach((id, k) => {
        tl.fromTo(id, { y: -180, scale: 0.9, opacity: 0, filter: "blur(8px)" },
          { y: 0, scale: 1, opacity: 1, filter: "blur(0px)", duration: 0.5, ease: "back.out(1.4)" }, temps[k]);
        for (let j = 0; j < k; j++) tl.to(ids[j], { y: (k - j) * ecart, duration: 0.45, ease: "power3.out" }, temps[k]);
      });
    },

    // Orbite : les logos tournent autour du centre, de début à fin.
    orbite(tl, sel, debut, fin, tours = 0.35, { entree = true } = {}) {
      const racine = document.querySelector(sel);
      const r = Number(racine.dataset.rayon);
      const items = Array.from(racine.querySelectorAll(".rgm-orbite-item"));
      const p = { a: 0 };
      const placer = () => {
        items.forEach((it) => {
          const i = Number(it.dataset.i), n = Number(it.dataset.n);
          const ang = (i / n) * Math.PI * 2 + p.a * Math.PI * 2 - Math.PI / 2;
          it.style.transform = "translate(" + (Math.cos(ang) * r).toFixed(1) + "px," + (Math.sin(ang) * r).toFixed(1) + "px)";
        });
      };
      tl.to(p, { a: tours, duration: fin - debut, ease: "none", onUpdate: placer }, debut);
      placer(); // état initial, posé tout de suite (un tl.call ne se déclenche pas toujours en seek)
      if (entree) {
        tl.from(sel + " .rgm-orbite-item .rgm-logo", { scale: 0, opacity: 0, rotation: -40, duration: 0.5, ease: "back.out(2)", stagger: 0.08 }, debut);
        tl.from(sel + " .rgm-orbite-anneau", { scale: 0.3, opacity: 0, duration: 0.6, ease: "expo.out" }, debut);
      }
    },

    // Bandeau de logos qui défile vers la gauche.
    defilement(tl, sel, debut, fin, vitesse = 160) {
      const piste = document.querySelector(sel + " .rgm-bande-piste");
      tl.fromTo(piste, { x: 0 }, { x: -vitesse * (fin - debut), duration: fin - debut, ease: "none" }, debut);
    },

    // Flux : nœuds qui apparaissent, liens qui se tracent, paquets qui circulent.
    flux(tl, sel, t, { cycles = 2, dureeCycle = 1.1 } = {}) {
      const racine = document.querySelector(sel);
      const noeuds = racine.querySelectorAll(".rgm-flux-noeud");
      tl.from(racine.querySelector(".rgm-flux-agent"), { scale: 0, opacity: 0, duration: 0.55, ease: "back.out(1.8)" }, t);
      tl.from(noeuds, { scale: 0, opacity: 0, duration: 0.45, ease: "back.out(2)", stagger: 0.08 }, t + 0.2);
      const liens = Array.from(racine.querySelectorAll(".rgm-flux-lien"));
      liens.forEach((l) => {
        const L = l.getTotalLength();
        l.style.strokeDasharray = L;
        const tl0 = t + (l.classList.contains("rgm-in") ? 0.5 : 0.9);
        // Le bout arrondi du trait ferait un point avant le tracé : on l allume au départ.
        tl.fromTo(l, { opacity: 0 }, { opacity: 1, duration: 0.05 }, tl0);
        tl.fromTo(l, { strokeDashoffset: L }, { strokeDashoffset: 0, duration: 0.5, ease: "power2.inOut" }, tl0);
      });
      const paquets = Array.from(racine.querySelectorAll(".rgm-flux-paquet"));
      const debutPaquets = t + 1.4;
      paquets.forEach((c, k) => {
        const chemin = liens[k];
        const L = chemin.getTotalLength();
        const sortie = chemin.classList.contains("rgm-out");
        const p = { u: 0 };
        const placer = () => {
          const u = p.u % 1;
          const visible = p.u > 0 && p.u < cycles;
          const pt = chemin.getPointAtLength(u * L);
          // Caché par l opacité : un paquet rangé hors cadre resterait visible (le SVG déborde).
          c.setAttribute("cx", pt.x);
          c.setAttribute("cy", pt.y);
          c.style.opacity = visible ? 1 : 0;
        };
        // Les entrées partent d'abord, les sorties une demi-boucle plus tard : l'agent « traite » entre les deux.
        tl.to(p, { u: cycles, duration: cycles * dureeCycle, ease: "none", onUpdate: placer }, debutPaquets + (sortie ? dureeCycle * 0.5 : 0));
        placer(); // état initial, posé tout de suite (un tl.call ne se déclenche pas toujours en seek)
      });
      tl.fromTo(racine.querySelector(".rgm-flux-halo"), { scale: 0.9, opacity: 0.5 },
        { scale: 1.25, opacity: 1, duration: dureeCycle / 2, ease: "sine.inOut", yoyo: true, repeat: Math.max(1, cycles * 2 - 1) }, debutPaquets);
      return debutPaquets + cycles * dureeCycle + dureeCycle * 0.5;
    },

    // Liseré lumineux qui tourne.
    faisceau(tl, sel, debut, duree, tours = 3) {
      tl.fromTo(sel, { "--angle": "0deg" }, { "--angle": 360 * tours + "deg", duration: duree, ease: "none" }, debut);
    },

    // Chiffre qui monte ; `pas` arrondit (100 pour des prix).
    compteur(tl, sel, t, duree = 1.0, pas = 1) {
      const el = document.querySelector(sel);
      const cible = Number(el.dataset.valeur);
      const p = { v: 0 };
      const peindre = () => { el.textContent = (Math.round(p.v / pas) * pas).toLocaleString("fr-FR").replace(/ | /g, " "); };
      tl.to(p, { v: cible, duration: duree, ease: "power2.out", onUpdate: peindre }, t);
      peindre(); // état initial, posé tout de suite (un tl.call ne se déclenche pas toujours en seek)
    },

    // Tâches cochées une à une (coche, rature, fond bleu pâle).
    cocher(tl, sel, temps) {
      const taches = document.querySelectorAll(sel + " .rgm-tache");
      tl.set(sel + " .rgm-coche", { scale: 0 }, 0);
      tl.set(sel + " .rgm-rature", { scaleX: 0 }, 0);
      taches.forEach((ta, i) => {
        tl.to(ta.querySelector(".rgm-coche"), { scale: 1, duration: 0.35, ease: "back.out(2.4)" }, temps[i]);
        tl.to(ta.querySelector(".rgm-rature"), { scaleX: 1, duration: 0.3, ease: "power2.inOut" }, temps[i] + 0.1);
        tl.to(ta, { backgroundColor: "#f3f8ff", borderColor: "#e2efff", duration: 0.3 }, temps[i] + 0.1);
      });
    },

    // Sous-titres : chaque groupe s'affiche sur sa fenêtre, le mot prononcé passe en bleu.
    sousTitres(tl, sel) {
      document.querySelectorAll(sel + " .rgm-st-groupe").forEach((g) => {
        const d = Number(g.dataset.debut), f = Number(g.dataset.fin);
        tl.fromTo(g, { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.15, ease: "power2.out" }, d);
        tl.to(g, { opacity: 0, duration: 0.12 }, f + 0.05);
        g.querySelectorAll(".rgm-st-mot").forEach((m) => {
          tl.fromTo(m, { color: "#0d1116" }, { color: "#0066dd", duration: 0.08 }, Number(m.dataset.debut));
        });
      });
    },

    // Appui sur un bouton.
    appui(tl, sel, t) {
      tl.to(sel, { scale: 0.93, duration: 0.1, ease: "power2.out" }, t);
      tl.to(sel, { scale: 1, duration: 0.3, ease: "back.out(3)" }, t + 0.1);
    },

    // Pulsation « ping » (badge en ligne, toast).
    ping(tl, sel, t, fois = 2) {
      tl.fromTo(sel, { scale: 1, opacity: 0.8 }, { scale: 2.6, opacity: 0, duration: 0.7, ease: "power1.out", repeat: fois - 1 }, t);
    },

    // Fond qui respire avec la musique (window.AUDIO_RMS, 30 valeurs par seconde).
    audioReactif(tl, duree, appliquer) {
      const rms = window.AUDIO_RMS || [], basse = window.AUDIO_BASSE || [];
      const p = { t: 0 };
      tl.to(p, {
        t: duree, duration: duree, ease: "none",
        onUpdate() {
          const f = Math.min(rms.length - 1, Math.round(p.t * 30));
          appliquer(p.t, rms[f] || 0, basse[f] || 0);
        },
      }, 0);
    },
  };

  // Regroupe des mots horodatés en sous-titres de 3 à 5 mots, coupés sur la ponctuation.
  function grouperMots(mots, max = 4) {
    const groupes = [];
    let g = [];
    mots.forEach((m) => {
      g.push(m);
      if (g.length >= max || /[.,!?;:]$/.test(m.mot)) { groupes.push(g); g = []; }
    });
    if (g.length) groupes.push(g);
    return groupes;
  }

  window.RGM = {
    html, monter, alea, grouperMots, anim,
    Logo, LogoRGM, OrbiteLogos, BandeLogos, FluxAgent,
    Telephone, Notification, Editeur, Terminal,
    Faisceau, CarteOffre, Compteur, ListeTaches,
    Titre, SousTitres, Bouton, Toast, Coche, Fleche,
  };
})();
