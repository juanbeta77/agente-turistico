# api/index.py
import os
import json
import openai
from vercel import Response

# Configurar OpenAI
openai.api_key = os.environ.get("OPENAI_API_KEY")
OPENAI_MODEL = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
OPENAI_TEMP = float(os.environ.get("OPENAI_TEMPERATURE", 0.7))
OPENAI_MAX_TOKENS = int(os.environ.get("OPENAI_MAX_TOKENS", 800))

DISCLAIMER = "\n\n⚠️ Esta es una recomendación generada por IA. Verifica información antes de usarla."

def handler(request, context):
    try:
        # Parsear body JSON
        body = json.loads(request.body)
        question = body.get("question", "").strip()

        if not question:
            return Response(
                json.dumps({"answer": "⚠️ Debes enviar 'question'"}),
                status=400,
                headers={"Content-Type": "application/json"}
            )

        # Construir prompt para OpenAI
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

        # Llamar a OpenAI
        response = openai.ChatCompletion.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "Eres un asistente experto en viajes. Sé claro, útil y conciso."},
                {"role": "user", "content": prompt}
            ],
            temperature=OPENAI_TEMP,
            max_tokens=OPENAI_MAX_TOKENS
        )

        answer = response["choices"][0]["message"]["content"].strip()

        return Response(
            json.dumps({"answer": answer + DISCLAIMER}),
            status=200,
            headers={"Content-Type": "application/json"}
        )

    except Exception as e:
        return Response(
            json.dumps({"answer": f"⚠️ Error al generar respuesta: {str(e)}"}),
            status=500,
            headers={"Content-Type": "application/json"}
        )
