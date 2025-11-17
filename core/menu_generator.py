import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_meal_plan(regime: str, budget: int, temps: int, personnes: int, 
                       type_menu: str, aliments_eviter: str,
                       lunchbox_count: int, microwave: bool) -> str:
    """
    Génère un menu hebdomadaire structuré à l'aide de GPT-4o-mini en prenant en compte une multitudes de paramètres choisis par l'user.
    """
    prompt = f"""
    Tu dois répondre STRICTEMENT en renvoyant UN UNIQUE JSON VALIDE.
    Tu es un expert en nutrition et en planification de repas.
    Tu vas créer un menu hebdomadaire pour une personne suivant les contraintes données.
    ────────────────────────────────────────────
    CONTRAINTES DE REPAS
    ────────────────────────────────────────────

    • Style : {type_menu}
    • Régime : {regime}
    • Aliments interdits : {aliments_eviter if aliments_eviter else "aucun"}
    • Temps max : {temps} minutes
    • Budget max : {budget}€
    • Micro-ondes : {"oui" if microwave else "non"}

    Les instructions doivent être une liste de 5 à 8 étapes numérotées :
    [
    "1. ...",
    "2. ...",
    ...
    ]

    ────────────────────────────────────────────
    EXEMPLE EXACT DE FORMAT À IMITER
    ────────────────────────────────────────────

    {{
    "menu": [
        {{
        "jour": "Lundi",
        "repas": [
            {{
            "moment": "midi",
            "plat": "Salade de quinoa",
            "ingredients": [
                {{"name": "quinoa", "quantity": 100, "unit": "g"}}
            ],
            "instructions": [
                "1. Cuire le quinoa.",
                "2. Couper les légumes.",
                "3. Mélanger."
            ]
            }},
            {{
            "moment": "soir",
            "plat": "Wraps de poulet",
            "lunchbox": true,
            "ingredients": [
                {{"name": "poulet", "quantity": 200, "unit": "g"}}
            ],
            "instructions": [
                "1. Cuire le poulet.",
                "2. Couper les légumes.",
                "3. Mélanger."
            ]
            }}
        ]
        }}
    ]
    }}

    ────────────────────────────────────────────
    RÉPONDS MAINTENANT UNIQUEMENT AVEC LE JSON FINAL.
    PAS DE TEXTE AVANT, PAS DE TEXTE APRÈS.
    PAS DE COMMENTAIRE.
    PAS DE PHRASE.
    """





    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.8,
    )

    return completion.choices[0].message.content

