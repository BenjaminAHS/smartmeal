import unicodedata
import numpy as np
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ---------- Normalisation basique ----------
def normalize_name(name):
    if not isinstance(name, str):
        name = str(name)

    name = name.lower().strip()
    name = ''.join(
        c for c in unicodedata.normalize("NFD", name)
        if unicodedata.category(c) != "Mn"
    )

    # pluriels simples
    if name.endswith("s") and len(name) > 3:
        name = name[:-1]

    return name


# ---------- Embeddings ----------
def embed(text: str):
    """Retourne l’embedding vectorisé d’un texte."""
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return np.array(response.data[0].embedding)


def cosine_similarity(a, b):
    """Sim = cos(angle(a, b))"""
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


# ---------- Matching principal ----------
def compute_missing_items(menu_ingredients, fridge_items, threshold=0.80):
    """
    Compare menu vs frigo avec embeddings :
    - matching intelligent (cosine similarity)
    - matching flexible (pluriels, accents, variations)
    """

    present = []
    missing = []

    # Normalisation des aliments du frigo
    fridge_clean = []
    for item in fridge_items:
        name = item["name"] if isinstance(item, dict) else str(item)
        fridge_clean.append(normalize_name(name))

    # Embedding de chaque ingrédient du frigo
    fridge_vectors = {
        name: embed(name)
        for name in fridge_clean
    }

    # Matching pour chaque ingrédient du menu
    for ing in menu_ingredients:

        raw_name = ing.get("name", "")
        if isinstance(raw_name, dict):
            raw_name = next(iter(raw_name.values()))

        ing_name_clean = normalize_name(raw_name)

        # Embedding du nom d’ingrédient du menu
        ing_vec = embed(ing_name_clean)

        # Comparaison avec tous les aliments du frigo
        best_sim = 0
        best_match = None

        for fridge_name, fr_vec in fridge_vectors.items():
            sim = cosine_similarity(ing_vec, fr_vec)

            if sim > best_sim:
                best_sim = sim
                best_match = fridge_name

        # Décision
        if best_sim >= threshold:
            present.append(ing)
        else:
            missing.append(ing)

    return present, missing
