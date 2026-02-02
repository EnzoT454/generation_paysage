# Génération procédurale de paysage 3D (îles)

Projet Python de **génération procédurale d’un paysage 3D** composé d’un océan et de **1 à 2 îles**, exporté sous forme de fichier **OpenSCAD (.scad)**.  
Les îles sont générées à partir de matrices de hauteur lissées, avec plages irrégulières et végétation, afin d’obtenir un rendu naturel.

---

## Objectif du projet

- Générer automatiquement un **modèle 3D paramétrique**
- Simuler des **îles de forme organique**
- Appliquer des notions de :
  - matrices de hauteur
  - bruit aléatoire
  - lissage
  - modélisation 3D par primitives (cubes, cylindres)
- Exporter le résultat vers **OpenSCAD** pour visualisation ou impression 3D

---

## Description

À chaque exécution, le programme :
- génère un **océan** (plaque 3D)
- crée **une ou deux îles** placées aléatoirement
- applique un **bruit contrôlé** et un **lissage itératif** pour des formes naturelles
- ajoute une **plage circulaire irrégulière** autour de chaque île
- colore le relief selon la hauteur (roche, terre, végétation)
- exporte le résultat dans un fichier **`model.scad`**

Le rendu est **différent à chaque lancement** grâce à l’aléatoire.


---

## Fonctionnement (vue d’ensemble)

### Océan
- Grande plaque bleue
- Épaisseur fixe
- Signature textuelle extrudée sous l’océan

### Îles
- Générées via une **matrice de hauteurs 2D**
- La hauteur décroît avec la distance au centre
- Bruit aléatoire + lissage pour un rendu organique

### Plages
- Anneau circulaire entre deux rayons
- Hauteur décroissante vers l’océan
- Ajout aléatoire de végétation (petits cylindres)

### Conversion 3D
- Chaque cellule devient un **cube 3D**
- Couleur selon la hauteur :
  - roche (gris)
  - terre (brun)
  - végétation (vert)

---
## Prérequis

- Python 3.x
- Bibliothèque **SolidPython**
- OpenSCAD (pour visualiser le fichier généré)

Installation de SolidPython :

```bash
pip install solidpython
```

---
## Étapes d’exécution
### 1️⃣ Lancer la génération

Depuis la racine du projet :

```bash
python3 generation_paysage.py
```


Génération du fichier :

```bash
model.scad
```

2️⃣ Visualiser le paysage


1. Ouvrir **OpenSCAD**
2. Charger le fichier généré :
```bash
model.scad
```
3. Cliquer sur **Preview (F5)** ou **Render (F6)**










