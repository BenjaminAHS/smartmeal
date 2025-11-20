def compute_missing_items(menu_ingredients, fridge_items):
    present = []
    missing = []

    # 🔥 Sécurité : si fridge_items est un dict → transformer en liste
    if isinstance(fridge_items, dict):
        fridge_items = [fridge_items]

    # 🔥 Sécurité : si fridge_items contient autre chose → le filtrer
    clean_fridge = []
    for item in fridge_items:
        if isinstance(item, dict) and "name" in item:
            clean_fridge.append(item)
        else:
            # si item est juste une string → on le convertit aussi
            clean_fridge.append({
                "name": str(item),
                "quantity": None,
                "unit": None
            })

    # Préparer les noms normalisés du frigo
    fridge_names = {
        str(obj["name"]).lower().strip()
        for obj in clean_fridge
    }

    # Comparaison menu ↔ frigo
    for ing in menu_ingredients:

        raw_name = ing.get("name", "")

        # 🔥 Normalisation anti-bug : dict → string
        if isinstance(raw_name, dict):
            raw_name = next(iter(raw_name.values()), "")

        # liste → on garde le premier
        if isinstance(raw_name, list):
            raw_name = raw_name[0] if raw_name else ""

        name = str(raw_name).lower().strip()

        if name in fridge_names:
            present.append(ing)
        else:
            missing.append(ing)

    return present, missing
