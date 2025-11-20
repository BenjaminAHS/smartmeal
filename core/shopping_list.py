import unicodedata
import re

def clean_text(text):
    """
    Nettoyage basique : minuscules, accents, espaces.
    On NE retire PAS les 's' ici pour ne pas casser 'Maïs' ou 'Ananas'.
    """
    if isinstance(text, dict):
        text = text.get("name", "")
    
    if not isinstance(text, str):
        return ""

    # 1. Minuscules
    text = text.lower().strip()

    # 2. Enlever les accents (ex: Pâte -> pate)
    text = ''.join(
        c for c in unicodedata.normalize('NFD', text)
        if unicodedata.category(c) != 'Mn'
    )
    
    # 3. Enlever mots parasites (cuit, bio, frais...)
    text = re.sub(r"\b(cuit|cuite|frais|fraiche|bio|rouge|blanc|entier)\b", "", text).strip()
    
    return text

def are_items_matching(menu_name, fridge_name):
    """
    Compare deux ingrédients de manière flexible (singulier/pluriel).
    Renvoie True si ça matche.
    """
    m = clean_text(menu_name)
    f = clean_text(fridge_name)

    if not m or not f:
        return False

    # 1. Correspondance exacte
    if m == f:
        return True

    # 2. Correspondance Menu (Singulier) vs Frigo (Pluriel)
    # Ex: menu="oeuf", frigo="oeufs"
    if m + "s" == f:
        return True
    
    # 3. Correspondance Menu (Pluriel) vs Frigo (Singulier)
    # Ex: menu="carottes", frigo="carotte"
    if m == f + "s":
        return True

    # 4. Cas spécial : pluriels en 'x' (chou/choux)
    if m + "x" == f or m == f + "x":
        return True

    return False

def compute_missing_items(menu_ingredients, fridge_items):
    """
    Compare les ingrédients.
    """
    present = []
    missing = []

    # On garde une copie propre de la liste du frigo pour itérer efficacement
    # fridge_items peut contenir des strings "oeufs" ou des dicts {"name": "oeufs"}
    fridge_list = fridge_items if fridge_items else []

    for ing_needed in menu_ingredients:
        found = False
        
        # On cherche cet ingrédient dans TOUT le frigo
        for fridge_item in fridge_list:
            if are_items_matching(ing_needed, fridge_item):
                found = True
                break # Trouvé ! Pas besoin de continuer à chercher cet ingrédient
        
        if found:
            present.append(ing_needed)
        else:
            missing.append(ing_needed)

    return present, missing