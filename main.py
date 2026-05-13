import streamlit as st
import numpy as np
from math import sqrt

# =====================================
# CONFIG
# =====================================
st.set_page_config(page_title="Agri Robot", layout="centered")

st.title("🤖 Agri Robot Intelligent")
st.write("Robot agricole basé sur Recherche Opérationnelle")

# =====================================
# CHAMP AGRICOLE
# =====================================
# 0 = normal
# 1 = manque d'eau
# 2 = mauvaises herbes

field = np.array([
    [0, 0, 1, 0, 0],
    [0, 2, 0, 0, 1],
    [0, 0, 0, 2, 0],
    [1, 0, 0, 0, 0],
    [0, 0, 2, 0, 1]
])

# =====================================
# DISTANCE
# =====================================
def distance(a, b):
    return sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)

# =====================================
# DETECTION ZONES CRITIQUES
# =====================================
critical_zones = []

for i in range(field.shape[0]):
    for j in range(field.shape[1]):
        if field[i][j] != 0:
            critical_zones.append((i, j))

# =====================================
# OPTIMISATION (RO - TSP GREEDY)
# =====================================
optimized_path = []

if critical_zones:
    current = critical_zones[0]
    optimized_path.append(current)
    remaining = critical_zones.copy()
    remaining.remove(current)

    while remaining:
        next_zone = min(remaining, key=lambda z: distance(current, z))
        optimized_path.append(next_zone)
        remaining.remove(next_zone)
        current = next_zone

# =====================================
# ACTION DU ROBOT
# =====================================
def action(zone):
    x, y = zone

    if field[x][y] == 1:
        return "💧 Irrigation"

    elif field[x][y] == 2:
        return "🌿 Désherbage"

    return "✔ Rien"

# =====================================
# AFFICHAGE
# =====================================
st.subheader("📍 Zones critiques")
st.write(critical_zones)

st.subheader("🛣️ Trajet optimisé (RO)")
st.write(optimized_path)

st.subheader("🤖 Exécution du robot")

for zone in optimized_path:
    st.write(f"Robot → {zone} | Action : {action(zone)}")

# =====================================
# STATISTIQUES
# =====================================
st.subheader("📊 Statistiques")

water = np.sum(field == 1)
weed = np.sum(field == 2)

st.write("Zones manque d’eau :", water)
st.write("Zones mauvaises herbes :", weed)
st.write("Total zones critiques :", len(critical_zones))

# =====================================
# OBJECTIF
# =====================================
st.subheader("🎯 Objectif RO")

st.write("""
- Minimiser distance
- Minimiser énergie
- Irrigation ciblée
- Désherbage localisé
""")