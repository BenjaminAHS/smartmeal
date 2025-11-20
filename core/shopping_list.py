import unicodedata

def normalize(s: str):
    """Nettoyage avancé : minuscule, sans accents, sans pluriel."""
    s = s.lower().strip()
    s = ''.join(c for c in unicodedata.normalize('NFD', s)
                if unicodedata.category(c) != 'Mn')
    if s.endswith('s'):
        s = s[:-1]
    return s


def compute_missing_items(menu_ingredients, fridge_items):
    """
    Compare les ingrédients nécessaires au menu avec les aliments du frigo.
    Gère :
    - fridge_items = strings
    - fridge_items = liste mixte strings/dicts
    - comparaison intelligente (sans accents, sans pluriels)
    """

    present = []
    missing = []

    # On transforme tout le frigo en list de strings nettoyés
    fridge_clean = []

    for item in fridge_items:
        if isinstance(item, dict) and "name" in item:
            fridge_clean.append(normalize(item["name"]))
        else:
            fridge_clean.append(normalize(str(item)))

    # On compare chaque ingrédient du menu
    for ing in menu_ingredients:
        ing_name = normalize(ing["name"])

        # Match si un élément du frigo contient ou égale le nom
        if any(ing_name in f or f in ing_name for f in fridge_clean):
            present.append(ing)
        else:
            missing.append(ing)

    return present, missing
