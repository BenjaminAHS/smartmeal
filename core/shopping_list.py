# shopping_list.py
import unicodedata
import re

# -------------------------
# Normalisation intelligente
# -------------------------

def normalize_name(name):
    """Normalise un nom d’ingrédient pour permettre le matching."""
    if not isinstance(name, str):
        return ""

    name = name.lower().strip()

    # enlever accents
    name = ''.join(
        c for c in unicodedata.normalize('NFD', name)
        if unicodedata.category(c) != 'Mn'
    )

    # pluriel → singulier basique
    if name.endswith("s") and len(name) > 3:
        name = name[:-1]

    # supprimer espaces multiples
    name = re.sub(r"\s+", " ", name)

    return name


# -------------------------
# Matching menu <-> frigo
# -------------------------

def compute_missing_items(menu_ingredients, fridge_items):
    """
    menu_ingredients = [
        {"name": "carotte", "quantity": 250, "unit": "g"},
        ...
    ]

    fridge_items =
        soit ["carotte", "lait"]
        soit [{"name": "carotte"}, {"name":"lait"}]
        soit mélange des deux
    """

    present = []
    missing = []

    fridge_clean = []

    # 🔥 On convertit TOUT en string propre
    for item in fridge_items:

        # cas dict : {"name": "..."}
        if isinstance(item, dict):
            name = item.get("name", "")
            fridge_clean.append(normalize_name(name))

        # cas string simple
        elif isinstance(item, str):
            fridge_clean.append(normalize_name(item))

        # cas inattendu → on ignore
        else:
            continue

    # -------------------------
    # Matching
    # -------------------------
    for ing in menu_ingredients:
        ing_name = normalize_name(ing["name"])

        if ing_name in fridge_clean:
            present.append(ing)
        else:
            missing.append(ing)

    return present, missing
