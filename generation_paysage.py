# Nom(s) étudiant(s) / Name(s) of student(s):
# Hamza Aqel


from solid import *
from solid.utils import *
import random
import math

# --- PARAMÈTRES GLOBAUX ---
GRID_SIZE = 80           # resolution de la grille par ile
ISLAND_AREA = 12         # taille max d’une ile (mm)(forme plus ou moins circulaire)
NUM_ISLANDS = 2          # nombre d’iles(varie entre 1 et 2 en fonction du résultat du random)
OCEAN_SIZE = 80          # taille de l’océan (mm)(forme carré)
OCEAN_HEIGHT = 2         # epaisseur de la plaque ocean
BEACH_HEIGHT = 0.1       # hauteur uniforme des cubes de plage
VEGETATION_HEIGHT = 0.2    # hauteur de la végétation
OUTPUT_FILE = "model.scad"

CUBE_SIZE = 3 * ISLAND_AREA / GRID_SIZE  # taille d’un cube terrain
BEACH_COLOR = [0.94, 0.90, 0.55] # jaune
IRREGULARITY = 0.1 # bruit

# --- FONCTION : LISSEUR DE MATRICE ---
# But : Adoucir la matrice de hauteurs
# (moins d’irrégularités brusques).
#
# Comment : Chaque cellule est remplacée par
# la moyenne de ses voisines.
#
# Pourquoi : Pour que les îles soient plus
# naturelles, plus lisses.
#
# Cette fonction a été obtenue à l'aide de AI(Chatgbt)
def smooth_matrix(matrix, iterations=2):
    size = len(matrix)
    for _ in range(iterations):
        new = [[0.0] * size for _ in range(size)]
        for i in range(size):
            for j in range(size):
                total, count = 0.0, 0
                for di in (-1, 0, 1):
                    for dj in (-1, 0, 1):
                        ni, nj = i + di, j + dj
                        if 0 <= ni < size and 0 <= nj < size:
                            total += matrix[ni][nj]
                            count += 1
                new[i][j] = total / count
        matrix = new
    return matrix

# --- FONCTION : GÉNÉRER MATRICE D'ÎLE ---
# But : Créer une matrice (2D) représentant la forme d’une île.
#
# Comment :
#
# Distance du centre => plus loin = plus bas.
#
# Un peu de bruit aléatoire sur la distance pour
# éviter un cercle parfait.
#
# Appliquer smooth_matrix pour lisser.
#
# Pourquoi : Avoir une île de forme "organique"
# (pas un cône parfait).
def generate_height_matrix(size, max_height):
    center = size // 2
    inner_radius = center * random.uniform(0.4, 0.5)
    matrix = []
    for y in range(size):
        row = []
        for x in range(size):
            dx = x - center
            dy = y - center
            dist = (dx**2 + dy**2)**0.5
            offset = random.uniform(-2, 2)
            d = dist + offset
            if d > inner_radius:
                row.append(0)
            else:
                base = (1 - dist / inner_radius) * max_height
                noise = random.uniform(-1, 1)
                h = max(0, min(max_height, base + noise))
                row.append(h)
        matrix.append(row)
    return smooth_matrix(matrix, iterations=10)

# --- FONCTION : CONVERTIR MATRICE EN ÎLE 3D ---
# But : Convertir une matrice de hauteurs en cubes colorés 3D.
#
# Comment : Selon la hauteur, choisir couleur : roche,
# terre, ou végétation.
#
# Placer des cubes au bon endroit dans l’espace.
#
# Pourquoi : Fabriquer visuellement l'île à partir des données de la matrice.
def island_from_matrix(matrix, offset_x=0, offset_y=0):
    blocks = []
    max_h = max(h for row in matrix for h in row if h > 0)

    for y, row in enumerate(matrix):
        for x, h in enumerate(row):
            if h == 0:
                continue
            if h > max_h * 0.95:
                col = [0.8, 0.8, 0.8]      # roche
            elif h > max_h * 0.2:
                col = [0.5, 0.3, 0]        # terre
            else:
                col = [0.13, 0.55, 0.13]   # végétation

            block = color(col)(
                translate([
                    offset_x + x * CUBE_SIZE,
                    offset_y + y * CUBE_SIZE,
                    OCEAN_HEIGHT
                ])(
                    cube([CUBE_SIZE, CUBE_SIZE, h])
                )
            )
            blocks.append(block)

    return union()(*blocks)

# --- FONCTION : CRÉER PLAGE CIRCULAIRE IRRÉGULIÈRE ---
# But : Ajouter une plage circulaire autour de l’île.
#
# Comment :
#
# Entre inner_radius et outer_radius, mettre des cubes
# plats colorés en jaune.
#
# Ajouter parfois de petits cylindres verts pour
# représenter de la végétation.
#
# Pourquoi : Donner un bord naturel à l'île
# (sable + un peu de verdure).
def create_beach(
    offset_x,
    offset_y,
    grid_size,
    cube_size,
    ocean_height,
    inner_radius,
    outer_radius
):
    """
    Génère une plage irrégulière en anneau entre inner_radius et outer_radius,
    avec une hauteur qui décroît linéairement de BEACH_HEIGHT à 0.
    """
    blocks = []
    center = grid_size / 2
    #print(center)
    radius_span = outer_radius - inner_radius

    for y in range(grid_size):
        for x in range(grid_size):
            # coordonnées relatives au centre de la grille
            dx = x - center
            dy = y - center
            dist = math.hypot(dx, dy)
            d_noisy = dist + random.uniform(-IRREGULARITY, IRREGULARITY)

            # on ne s'intéresse qu'à la bande plage
            if inner_radius < d_noisy <= outer_radius:
                # calcul de la hauteur en fonction de la distance
                t = (outer_radius - d_noisy) / radius_span
                height = BEACH_HEIGHT * max(0, t)

                bx = offset_x + x * cube_size
                by = offset_y + y * cube_size
                bz = ocean_height

                # cube de plage à hauteur variable
                blocks.append(
                    color(BEACH_COLOR)(
                        translate([bx, by, bz])(
                            cube([cube_size, cube_size, height])
                        )
                    )
                )

                # végétation éventuelle posée sur cette plage
                if random.random() < 0.15:
                    veg = color([0.1, 0.8, 0.1])(
                        translate([bx, by, bz + height])(
                            cylinder(h=VEGETATION_HEIGHT, r=1/2)
                        )
                    )
                    blocks.append(veg)

    return union()(*blocks)


# --- FONCTION : CRÉER LA SCÈNE COMPLÈTE ---
# But : Assembler l'ensemble du décor (océan, texte, îles).
#
# Comment :
#
# Créer l’océan (grand cube bleu).
# Ajouter signature.
# Déterminer deux positions d'îles.
#
# Pour chaque île :
# Créer plage et île.
# Ajouter dans la scène.
#
# Pourquoi : C'est la fonction principale qui
# construit tout ce que l’on voit.
def create_scene():
    scene = []
    ocean = color([0, 0.3, 1])(
        cube([OCEAN_SIZE, OCEAN_SIZE, OCEAN_HEIGHT])
    )
    scene.append(ocean)

    # Signature sous l'ocean
    txt = linear_extrude(height=0.1)(  # extrusion pour donner une épaisseur au texte
        text("IFT2125 - FR+HA", size=5, halign="center", valign="center")
    )
    txt = mirror([1, 0, 0])(txt)  # miroir sur Y
    text_pos = translate([OCEAN_SIZE / 2, OCEAN_SIZE / 5, -2])(txt)  # positionner sous l'océan
    scene.append(text_pos)

    # --- Position de la première île : centre approximatif ---
    island_size_mm = GRID_SIZE * CUBE_SIZE
    center_x = (OCEAN_SIZE - island_size_mm) / 5
    center_y = (OCEAN_SIZE - island_size_mm) / 5
    positions = [(center_x, center_y)]

    # --- Position de la deuxième île : proche de la première ---
    max_offset = island_size_mm * 0.5
    angle = random.uniform(0, 2 * math.pi)
    dx = math.cos(angle) * max_offset
    dy = math.sin(angle) * max_offset
    second_x = center_x + dx +40
    second_y = center_y + dy +40

    # Corriger si dépasse les limites de l'océan
    second_x = min(max(0, second_x), OCEAN_SIZE - island_size_mm)
    second_y = min(max(0, second_y), OCEAN_SIZE - island_size_mm)
    positions.append((second_x, second_y))
    # print(center_x,center_y)
    # print(second_x,second_y)
    for offset_x, offset_y in positions:
        max_h = random.uniform(10, 15)
        mat = generate_height_matrix(GRID_SIZE, max_h)

        # Définir les rayons plage
        inner = GRID_SIZE * 0.3
        outer = inner + 10

        # Créer plage puis ile
        beach = create_beach(offset_x, offset_y, GRID_SIZE, CUBE_SIZE, OCEAN_HEIGHT, inner, outer)
        island = island_from_matrix(mat, offset_x, offset_y)
        scene.append(beach)
        scene.append(island)

    return union()(*scene)


# --- SCRIPT PRINCIPAL ---
# But : Point de départ du programme.
#
# Comment :
#
# Appeler create_scene().
#
# Sauvegarder le modèle .scad.
#
# Pourquoi : Générer le fichier final.
if __name__ == "__main__":
    model = create_scene()
    scad_render_to_file(model, OUTPUT_FILE)
    print(f" Généré : {OUTPUT_FILE}")
