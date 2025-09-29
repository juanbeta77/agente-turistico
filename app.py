import os
from flask import Flask, request, jsonify, send_from_directory
from dotenv import load_dotenv
import openai

# Cargar variables de entorno
load_dotenv()
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
OPENAI_TEMP = float(os.getenv("OPENAI_TEMPERATURE", "0.7"))
OPENAI_MAX_TOKENS = int(os.getenv("OPENAI_MAX_TOKENS", "800"))

openai.api_key = OPENAI_KEY

app = Flask(__name__, static_folder="static", static_url_path="")

DISCLAIMER = "\n\n⚠️ Esta es una recomendación generada por IA. Verifica información antes de usarla."

def call_openai(prompt: str):
    """Función central para llamar a OpenAI y obtener respuesta de IA."""
    if not OPENAI_KEY:
        return "⚠️ No se encontró OPENAI_API_KEY. Configúrala en .env para usar la IA."
    try:
        response = openai.ChatCompletion.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "Eres un asistente experto en viajes. Sé útil, claro y breve."},
                {"role": "user", "content": prompt}
            ],
            temperature=OPENAI_TEMP,
            max_tokens=OPENAI_MAX_TOKENS
        )
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print("Error con OpenAI:", e)
        return "⚠️ Error al generar respuesta con IA."

@app.route("/api/ask", methods=["POST"])
def ask():
    try:
        data = request.get_json(force=True)  # fuerza parseo JSON
    except Exception as e:
        return jsonify({"error": "JSON inválido o mal formado.", "details": str(e)}), 400

    if not data or "question" not in data:
        return jsonify({"error": "Debes enviar 'question' en el body"}), 400

    question = data.get("question", "").strip()
    if not question:
        return jsonify({"error": "El campo 'question' no puede estar vacío."}), 400

    # Construir prompt
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

    result = call_openai(prompt)
    return jsonify({"answer": result + DISCLAIMER})

@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
