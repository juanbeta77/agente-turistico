
import os
import json
import openai
from dotenv import load_dotenv

load_dotenv()

OPENAI_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
OPENAI_TEMP = float(os.getenv("OPENAI_TEMPERATURE", "0.7"))
OPENAI_MAX_TOKENS = int(os.getenv("OPENAI_MAX_TOKENS", "800"))

openai.api_key = OPENAI_KEY
DISCLAIMER = "\n\n⚠️ Esta es una recomendación generada por IA."

def handler(request, context):
    try:
        data = json.loads(request.body)
        question = data.get("question", "").strip()
        if not question:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Debes enviar 'question' en el body"})
            }

        prompt = f"""
        Actúa como un planificador de viajes.
        Usuario: {question}
        Genera:
        - Clima esperado
        - Costos aproximados
        - Lugares para visitar
        - Itinerario diario
        Usa viñetas y separa bien por secciones.
        """

        response = openai.ChatCompletion.create(
            model=OPENAI_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=OPENAI_TEMP,
            max_tokens=OPENAI_MAX_TOKENS
        )
        answer = response["choices"][0]["message"]["content"].strip()
        return {
            "statusCode": 200,
            "body": json.dumps({"answer": answer + DISCLAIMER})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
