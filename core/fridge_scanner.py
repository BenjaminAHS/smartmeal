import os
from openai import OpenAI
from PIL import Image
import base64
from io import BytesIO

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def detect_food_items(image: Image.Image) -> list[str]:
    """
    Analyse une image de frigo/placard et renvoie une liste d'aliments détectés.
    """
     # Convertir en RGB si nécessaire (évite l’erreur RGBA → JPEG)
    if image.mode in ("RGBA", "P"):
        image = image.convert("RGB")
    # Convertir l'image en base64
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    img_b64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

    prompt = """
    Tu es un assistant culinaire. 
    Voici une photo du contenu d’un frigo ou placard.
    Liste uniquement les aliments ou produits visibles.
    Réponds sous forme de liste Python simple, sans explications.
    Exemple :
    ["tomates", "œufs", "beurre", "riz", "yaourt"]
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "Tu es un assistant qui identifie les aliments visibles sur une photo de frigo ou de placard."
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": (
                            "Liste uniquement les aliments visibles, sans explication, "
                            "au format : ['aliment1', 'aliment2', ...]"
                        ),
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{img_b64}"
                        },
                    },
                ],
            },
        ],
        temperature=0.2,
    )

    text_output = response.choices[0].message.content.strip()

    # Sécuriser la conversion de texte en liste Python
    try:
        items = eval(text_output)
        if isinstance(items, list):
            return items
        return [text_output]
    except Exception:
        return [text_output]