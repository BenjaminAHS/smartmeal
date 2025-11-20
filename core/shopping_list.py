import unicodedata

def clean_simple(text):
    """
    Nettoyage ultra-basique : minuscules et sans accents.
    On ne retire PAS les 's' ici pour ne pas casser les mots comme 'Maïs'.
    """
    if isinstance(text, dict):
        text = text.get("name", "")
    
    if not isinstance(text, str):
        return ""

    # 1. Minuscules
    text = text.lower().strip()

    # 2. Enlever les accents (ex: Pâte -> pate, Bœuf -> boeuf)
    text = ''.join(
        c for c in unicodedata.normalize('NFD', text)
        if unicodedata.category(c) != 'Mn'
    )
    
    return text

def is_match(menu_item, fridge_item):
    """
    Vérifie si deux ingrédients correspondent, peu importe le pluriel.
    """
    m = clean_simple(menu_item)
    f = clean_simple(fridge_item)

    if not m or not f:
        return False

    # 1. Correspondance exacte (ex: "lait" == "lait")
    if m == f:
        return True

    # 2. Le menu est au singulier, le frigo au pluriel (ex: "oeuf" vs "oeufs")
    if m + "s" == f or m + "x" == f:
        return True
    
    # 3. Le menu est au pluriel, le frigo au singulier (ex: "carottes" vs "carotte")
    if m == f + "s" or m == f + "x":
        return True

    # 4. Sécurité anti-bug : Si le mot du menu est contenu ENTIÈREMENT dans celui du frigo
    # Ex: Menu demande "Pomme", frigo a "Pommes gala" -> Match
    # Attention : on vérifie la longueur pour éviter que "riz" matche "chorizo"
    if m in f and len(m) > 3:
        return True

    return False

def compute_missing_items(menu_ingredients, fridge_items):
    """
    Compare chaque ingrédient du menu avec tout le frigo.
    """
    present = []
    missing = []

    # Sécurité si les listes sont vides
    if not fridge_items: fridge_items = []
    if not menu_ingredients: menu_ingredients = []

    for ing_needed in menu_ingredients:
        found = False
        
        # On teste l'ingrédient demandé contre TOUT ce qu'il y a dans le frigo
        for fridge_item in fridge_items:
            if is_match(ing_needed, fridge_item):
                found = True
                # On met à jour la quantité possédée si besoin (optionnel)
                break 
        
        if found:
            present.append(ing_needed)
        else:
            missing.append(ing_needed)

    return present, missing