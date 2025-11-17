def compute_missing_items(menu_ingredients, fridge_items):
    """
    Compare les ingrédients du menu et les aliments du frigo.
    Retourne :
      - présents (avec quantités trouvées)
      - manquants (avec quantités à acheter)
    """
    fridge_set = {f.lower().strip() for f in fridge_items}
    present, missing = [], []

    for ing in menu_ingredients:
        name = ing["name"]
        qty = ing["quantity"]
        unit = ing["unit"]

        # Si un aliment du frigo correspond au nom de l'ingrédient
        if any(f in name for f in fridge_set):
            present.append(ing)
        else:
            missing.append(ing)

    return present, missing
