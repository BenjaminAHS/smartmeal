
def compute_missing_items(menu_ingredients, fridge_items):
    """
    This function compares the ingredients required by the weekly menu with the food items detected in the user’s fridge.
    It identifies which ingredients are already available and which ones still need to be purchased based on name matching.
    The output consists of two lists: present items with their quantities, and missing items to buy.
    """
    present = []
    missing = []

    # Préparer les noms du frigo
    fridge_names = {str(item["name"]).lower().strip() for item in fridge_items}

    for ing in menu_ingredients:

        # Forcer le nom en string propre
        raw_name = ing.get("name", "")

        # si c'est un dict → on prend la première valeur textuelle trouvée
        if isinstance(raw_name, dict):
            # ex: {"ingredient": "crème"}
            raw_name = next(iter(raw_name.values()), "")
        
        # si c'est une liste → on prend le premier élément
        if isinstance(raw_name, list) and raw_name:
            raw_name = raw_name[0]

        name = str(raw_name).lower().strip()

        # Comparaison uniquement sur le nom
        if name in fridge_names:
            present.append(ing)
        else:
            missing.append(ing)

    return present, missing


