import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# ---------- Normalisation basique ----------
def normalize_name(name):
    """Normalise un nom d’ingrédient."""
    if not isinstance(name, str):
        return ""
    return name.lower().replace("œ", "oe").replace("é", "e").strip()


# ---------- Distance sémantique via embeddings ----------
def semantic_distance(a, b):
    """Distance cosinus entre 2 textes."""
    try:
        emb = client.embeddings.create(
            model="text-embedding-3-small",
            input=[a, b]
        ).data
        import numpy as np
        v1 = np.array(emb[0].embedding)
        v2 = np.array(emb[1].embedding)

        return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
    except Exception:
        return 0  # fallback si modèle indisponible


# ---------- MATCHING ----------
def names_match(a, b):
    """Vérifie si 2 noms d’ingrédients correspondent."""
    a_n = normalize_name(a)
    b_n = normalize_name(b)

    # Match exact
    if a_n == b_n:
        return True

    # Match partiel
    if a_n in b_n or b_n in a_n:
        return True

    # Match intelligent
    score = semantic_distance(a_n, b_n)
    return score > 0.80


# ---------- FONCTION PRINCIPALE ----------
def compute_missing_items(menu_ingredients, fridge_items):
    """
    menu_ingredients = [
        {"name": "...", "quantity": 100, "unit": "g"},
        ...
    ]

    fridge_items = [
        {"name": "..."},
        ...
    ]
    """

    present = []
    missing = []

    # 🔥 NORMALISATION DU FRIGO
    fridge_clean = []
    for item in fridge_items:
        if isinstance(item, dict):
            name = normalize_name(item.get("name"))
            if name:
                fridge_clean.append(name)
        elif isinstance(item, str):
            fridge_clean.append(normalize_name(item))

    # 🔥 ENSUITE MATCHING
    for ing in menu_ingredients:
        ing_name = ing["name"]

        found = False
        for f in fridge_clean:
            if names_match(ing_name, f):
                found = True
                break

        if found:
            present.append(ing)
        else:
            missing.append(ing)

    return present, missing