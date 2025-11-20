# shopping_list.py
def normalize_name(name):
    """
    Force un nom à être une string en minuscules propre.
    Gère robustement les cas où 'name' serait un dictionnaire ou None.
    """
    # Si par erreur on passe l'objet ingrédient entier (dict), on prend son 'name'
    if isinstance(name, dict):
        name = name.get("name", "")

    # Si ce n'est pas une string (ex: None, int, float), on convertit ou retourne vide
    if not isinstance(name, str):
        return str(name).lower().strip() if name is not None else ""

    return name.lower().strip()


def compute_missing_items(menu_ingredients, fridge_items):
    """
    Compare les ingrédients du menu avec ceux du frigo.
    
    menu_ingredients : liste de dicts [{'name': '...', 'quantity': ...}, ...]
    fridge_items : liste de dicts [{'name': '...'}] OU liste de strings ['pomme', ...]
    """

    present = []
    missing = []

    # 🔥 1. Normaliser les noms du frigo dans un Set pour recherche rapide
    fridge_clean = set()

    for item in fridge_items:
        # Gestion flexible : item peut être une string ou un dict
        val_to_normalize = item
        if isinstance(item, dict):
            val_to_normalize = item.get("name", "")
        
        normalized = normalize_name(val_to_normalize)
        if normalized:
            fridge_clean.add(normalized)

    # 🔥 2. Comparaison
    for ing in menu_ingredients:
        # ing est censé être un dictionnaire venant de extract_ingredients
        # On utilise .get() par sécurité
        ing_name = normalize_name(ing.get("name", ""))

        if ing_name in fridge_clean:
            present.append(ing)
        else:
            missing.append(ing)

    return present, missing