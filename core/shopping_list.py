# shopping_list.py

def normalize_name(candidate):
    """
    Nettoie n'importe quelle entrée pour renvoyer une string simple en minuscules.
    Accepte : str, dict, ou n'importe quoi d'autre.
    """
    # 1. Si c'est None, on renvoie vide
    if candidate is None:
        return ""

    # 2. Si c'est un dictionnaire (ex: {"name": "Tomate", "q": 1}), on extrait le nom
    if isinstance(candidate, dict):
        # On utilise .get() pour éviter une erreur si la clé "name" n'existe pas
        candidate = candidate.get("name", "")

    # 3. À ce stade, si ce n'est toujours pas une string (ex: un int), on convertit
    if not isinstance(candidate, str):
        candidate = str(candidate)

    # 4. Nettoyage final : minuscules et suppression des espaces
    return candidate.lower().strip()


def compute_missing_items(menu_ingredients, fridge_items):
    """
    Compare le menu (ce qu'il faut) avec le frigo (ce qu'on a).
    Gère le fait que fridge_items peut être une liste de strings OU de dicts.
    
    Args:
        menu_ingredients (list[dict]): Liste propre venant de extract_ingredients.
        fridge_items (list): Liste mixte (str ou dict) venant du scanner/input.
    """
    present = []
    missing = []

    # --- ÉTAPE 1 : Créer un inventaire frigo PROPRE et UNIFORME ---
    fridge_set = set()
    
    if not fridge_items:
        fridge_items = []

    for item in fridge_items:
        # On passe chaque item à la moulinette, qu'il soit string ou dict
        clean_name = normalize_name(item)
        if clean_name:
            fridge_set.add(clean_name)

    # --- ÉTAPE 2 : Vérifier chaque ingrédient du menu ---
    if not menu_ingredients:
        menu_ingredients = []

    for ing in menu_ingredients:
        # ing est un dictionnaire {"name": "...", "quantity": ...}
        # On extrait son nom normalisé pour comparer
        ing_name_clean = normalize_name(ing)

        if ing_name_clean in fridge_set:
            present.append(ing)
        else:
            missing.append(ing)

    return present, missing