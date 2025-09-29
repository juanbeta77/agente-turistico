import json
import os
import openai

openai.api_key = os.environ.get("OPENAI_API_KEY")

DISCLAIMER = "\n\n⚠️ Esta es una recomendación generada por IA. Verifica información antes de usarla."

def handler(request, context):
    try:
        body = json.loads(request.body.decode("utf-8"))
        question = body.get("question", "").strip()
        if not question:
            return {"statusCode": 400, "body": json.dumps({"answer": "⚠️ Debes enviar 'question'"})}

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
            model=os.environ.get("OPENAI_MODEL", "gpt-4o-mini"),
            messages=[
                {"role": "system", "content": "Eres un asistente experto en viajes. Sé claro y útil."},
                {"role": "user", "content": prompt}
            ],
            temperature=float(os.environ.get("OPENAI_TEMPERATURE", 0.7)),
            max_tokens=int(os.environ.get("OPENAI_MAX_TOKENS", 800))
        )
        answer = response["choices"][0]["message"]["content"].strip()
        return {"statusCode": 200, "body": json.dumps({"answer": answer + DISCLAIMER})}
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"answer": f"⚠️ Error: {str(e)}"})}
