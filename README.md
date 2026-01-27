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
## Prérequis

- Python 3.x
- Bibliothèque **SolidPython**
- OpenSCAD (pour visualiser le fichier généré)

Installation de SolidPython :

```bash
pip install solidpython
```

---
## Résultat :

Génération du fichier :

```bash
model.scad
```

Ce fichier peut être ouvert directement dans OpenSCAD.










