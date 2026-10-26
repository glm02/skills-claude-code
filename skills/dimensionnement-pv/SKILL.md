---
name: dimensionnement-pv
description: Dimensionner une installation photovoltaïque résidentielle — production (PVGIS), nombre de panneaux, chaînes et onduleur, câbles et protections (UTE C15-712-1, NF C 15-100), rentabilité, démarches. À utiliser pour « combien ça va produire », « quel onduleur », « section de câble DC », « c'est rentable ? », un projet solaire de maison ou un exercice de cours sur le PV.
---

# Dimensionnement photovoltaïque

## Outil : production et rentabilité

```
python ~/.claude/skills/dimensionnement-pv/pvgis.py --lat <lat> --lon <lon> --kwc 6 --inclinaison 30 --azimut 0 --conso 6500 --cout 9000
```
Azimut : 0 sud, −90 est, 90 ouest. `--optimal` laisse PVGIS choisir l'angle.
Les coordonnées du centre de la commune suffisent.

## Étapes

1. **Besoin** : consommation annuelle (facture ou compte Enedis), présence
   en journée, chauffage électrique ou non, projet de véhicule électrique.
2. **Surface → puissance** : nombre de panneaux posables (skill
   `blender-solaire`, ou surface utile ÷ surface d'un panneau, marges de
   30 cm). En autoconsommation avec vente du surplus, viser une production
   proche de la consommation de jour, souvent 3 à 6 kWc pour une maison.
3. **Production** avec l'outil, pour chaque pan envisagé ; comparer est /
   ouest / sud et portrait / paysage.
4. **Onduleur et chaînes** (valeurs de la fiche technique du panneau) :
   - Voc à la température minimale (−10 °C) :
     Voc(−10) = Voc × (1 + (−10 − 25) × βVoc) ; n × Voc(−10) < tension max
     d'entrée de l'onduleur ;
   - Vmp à 70 °C : n × Vmp(70) > tension minimale de la plage MPPT ;
   - courant : Isc du panneau × nombre de chaînes en parallèle ≤ courant max
     MPPT ; deux pans d'orientations différentes = deux MPPT distincts ;
   - rapport puissance crête / puissance AC de l'onduleur entre 1,0 et 1,3.
   Micro-onduleurs : un par panneau ou par paire, utiles en cas d'ombrage.
5. **Câbles et protections** :
   - DC : câble solaire, Iz ≥ 1,25 × Isc, chute de tension ≤ 1 à 3 % ;
     ΔU = 2 × ρ × L × I / S, avec ρ = 0,023 Ω·mm²/m pour le cuivre chaud ;
   - interrupteur-sectionneur DC, parafoudre DC selon la longueur de câble et
     la densité de foudroiement, fusibles de chaîne au-delà de 2 chaînes en
     parallèle ;
   - AC : disjoncteur dédié au tableau, différentiel 30 mA de type adapté à
     l'onduleur, chute ≤ 1 % jusqu'au point de livraison, mise à la terre
     des cadres.
6. **Rentabilité** : gain annuel et retour sur investissement donnés par
   l'outil. Le tarif de rachat du surplus et la prime à l'autoconsommation
   changent chaque trimestre : vérifier les valeurs du jour (CRE,
   photovoltaique.info) et citer la date.
7. **Démarches** : déclaration préalable en mairie (Cerfa 16702), demande de
   raccordement Enedis (autoconsommation avec vente du surplus), attestation
   Consuel, contrat d'achat du surplus (EDF OA). Pour la prime et le tarif
   d'achat, l'installateur doit être certifié RGE QualiPV.

Fini quand la production, le nombre de panneaux, l'onduleur vérifié sur
les trois conditions de l'étape 4, les sections de câbles et le retour sur
investissement sont chiffrés, chacun avec sa source ou son calcul.

## Pour un cours (BUT GEII)

Montrer chaque calcul avec la formule, les valeurs et l'unité, et vérifier
l'ordre de grandeur (en France, 1 000 à 1 450 kWh/kWc/an selon la région).
