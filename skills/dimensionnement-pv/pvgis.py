"""Production d'une installation photovoltaïque avec PVGIS (Commission européenne).

Usage :
  python pvgis.py --lat 45.19 --lon 5.72 --kwc 6 --inclinaison 30 --azimut 0
  python pvgis.py --lat 45.19 --lon 5.72 --kwc 6 --optimal
  python pvgis.py ... --conso 6500 --prix 0.2516 --rachat 0.04 --cout 9000

Azimut PVGIS : 0 = plein sud, -90 = est, 90 = ouest, 180 = nord.
Pertes système par défaut 14 % (câbles, onduleur, salissure).

Les coordonnées n'ont pas besoin d'être précises : celles du centre de la
commune suffisent à PVGIS. Ne jamais écrire l'adresse exacte d'un particulier
dans un dépôt ou une page publiée.
"""
import argparse, json, sys, urllib.parse, urllib.request

API = "https://re.jrc.ec.europa.eu/api/v5_3/PVcalc"
MOIS = ["janv", "févr", "mars", "avr", "mai", "juin", "juil", "août", "sept", "oct", "nov", "déc"]


def main():
    a = argparse.ArgumentParser()
    a.add_argument("--lat", type=float, required=True)
    a.add_argument("--lon", type=float, required=True)
    a.add_argument("--kwc", type=float, required=True, help="puissance crête en kWc")
    a.add_argument("--inclinaison", type=float, default=30)
    a.add_argument("--azimut", type=float, default=0)
    a.add_argument("--optimal", action="store_true", help="laisser PVGIS choisir inclinaison et azimut")
    a.add_argument("--pertes", type=float, default=14)
    a.add_argument("--conso", type=float, help="consommation annuelle du foyer en kWh")
    a.add_argument("--autoconso", type=float, default=None, help="taux d'autoconsommation estimé (0-1)")
    a.add_argument("--prix", type=float, default=0.2516, help="prix du kWh acheté, €")
    a.add_argument("--rachat", type=float, default=0.04, help="tarif de rachat du surplus, €/kWh")
    a.add_argument("--cout", type=float, help="coût total de l'installation, €")
    o = a.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")

    p = {"lat": o.lat, "lon": o.lon, "peakpower": o.kwc, "loss": o.pertes, "outputformat": "json"}
    if o.optimal:
        p["optimalangles"] = 1
    else:
        p["angle"], p["aspect"] = o.inclinaison, o.azimut
    req = urllib.request.Request(f"{API}?{urllib.parse.urlencode(p)}", headers={"User-Agent": "agent-local"})
    with urllib.request.urlopen(req, timeout=60) as r:
        d = json.load(r)

    fixe = d["inputs"]["mounting_system"]["fixed"]
    tot = d["outputs"]["totals"]["fixed"]
    mois = d["outputs"]["monthly"]["fixed"]
    an = tot["E_y"]
    print(f"Lieu {o.lat:.2f}, {o.lon:.2f} · {o.kwc} kWc · inclinaison {fixe['slope']['value']}° · azimut {fixe['azimuth']['value']}° · pertes {o.pertes} %")
    n = lambda x: f"{x:,.0f}".replace(",", " ")  # séparateur de milliers à la française
    print(f"Production : {n(an)} kWh/an, soit {n(an / o.kwc)} kWh/kWc (variation d'une année à l'autre ± {n(tot['SD_y'])} kWh)")
    print("Par mois (kWh) : " + " · ".join(f"{MOIS[m['month'] - 1]} {m['E_m']:.0f}" for m in mois))

    if o.conso:
        # Sans batterie, un foyer présent en journée autoconsomme 30 à 50 % de sa production.
        taux = o.autoconso if o.autoconso is not None else (0.5 if an < 0.6 * o.conso else 0.35)
        auto = an * taux
        gain = auto * o.prix + (an - auto) * o.rachat
        print(f"\nAutoconsommation supposée {taux:.0%} : {n(auto)} kWh évités ({auto / o.conso:.0%} de la consommation)")
        print(f"Gain annuel ≈ {n(gain)} € (achat évité {n(auto * o.prix)} € + surplus vendu {n((an - auto) * o.rachat)} €)")
        if o.cout:
            print(f"Retour sur investissement ≈ {o.cout / gain:.1f} ans (hors hausse du prix de l'électricité, hors entretien)")


if __name__ == "__main__":
    main()
