
from app import app

from flask import Flask, request, jsonify
import os
import openai
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

OPENAI_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
OPENAI_TEMP = float(os.getenv("OPENAI_TEMPERATURE", 0.7))
OPENAI_MAX_TOKENS = int(os.getenv("OPENAI_MAX_TOKENS", 800))

openai.api_key = OPENAI_KEY

DISCLAIMER = "\n\n⚠️ Esta es una recomendación generada por IA. Verifica información antes de usarla."

def call_openai(prompt: str):
    if not OPENAI_KEY:
        return "⚠️ No se encontró OPENAI_API_KEY."
    try:
        response = openai.ChatCompletion.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "Eres un asistente experto en viajes."},
                {"role": "user", "content": prompt}
            ],
            temperature=OPENAI_TEMP,
            max_tokens=OPENAI_MAX_TOKENS
        )
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"⚠️ Error al generar respuesta con IA: {str(e)}"

@app.route("/api/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = data.get("question", "").strip()
    if not question:
        return jsonify({"error": "Debes enviar 'question'"}), 400

    prompt = f"""
    Actúa como un planificador de viajes.
    Usuario: {question}
    Genera:
    - Clima esperado
    - Costos aproximados
    - Lugares para visitar
    - Itinerario diario
    """
    answer = call_openai(prompt)
    return jsonify({"answer": answer + DISCLAIMER})

