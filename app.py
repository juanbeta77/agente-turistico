from flask import Flask, request, jsonify, send_from_directory
import os, re
from openai import OpenAI  # Cliente oficial de OpenAI

# Inicializar Flask y OpenAI
app = Flask(__name__, static_folder="static", static_url_path="")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

DISCLAIMER = "ℹ Nota: Esta información es generada por IA y puede no ser 100% precisa."

# -----------------------------
# Guardrails (igual que antes)
# -----------------------------
def guardrails(state):
    question = state["question"].lower().strip()

    if not question:
        return {**state, "blocked": True, "answer": "No hay ninguna pregunta de entrada."}

    palabras_prohibidas = [
        "odio","odiar","violencia","insulto","insultar","matar","robar","pegar","agredir","golpear",
        "lastimar","amenazar","dañar","abusar","secuestrar","secuestro","torturar","herir","discriminar",
        "humillar","intimidar","vengar","sabotear","maltratar","violar","corromper","estafar","traicionar",
        "despreciar","destruir","oprimir","castigar","maldecir","provocar","burlar","manipular","saquear",
        "extorsionar","asesinar"
    ]
    if any(p in question for p in palabras_prohibidas):
        return {**state, "blocked": True, "answer": "Contenido inapropiado detectado."}

    if re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}", question):
        return {**state, "blocked": True, "answer": "No puedo procesar correos electrónicos."}
    if re.search(r"\+?\d{8,}", question):
        return {**state, "blocked": True, "answer": "No puedo mostrar datos de contacto."}

    if len(question.split()) < 2:
        return {**state, "blocked": True, "answer": "Pregunta demasiado corta para recomendar algo."}

    return {**state, "blocked": False}

# -----------------------------
# Utilidad para llamar a la IA
# -----------------------------
def call_openai(prompt: str, max_tokens=300):
    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",  # puedes usar gpt-4, gpt-4o, gpt-3.5, etc.
            messages=[
                {"role": "system", "content": "Eres un asistente de viajes experto que genera información breve y clara."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens,
            temperature=0.8
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        return f"⚠️ Error al llamar a la IA: {e}"

# -----------------------------
# Agentes dinámicos usando IA
# -----------------------------
def agente_clima(state):
    prompt = f"Dime el clima actual aproximado en la ciudad mencionada en esta pregunta: {state['question']}. Sé breve (1 línea)."
    return {**state, "answer": call_openai(prompt) + f" {DISCLAIMER}"}

def agente_costos(state):
    prompt = f"Da un estimado de costo por persona para viajar a la ciudad de la pregunta: {state['question']}. Sé breve (1 línea, incluye moneda)."
    return {**state, "answer": call_openai(prompt) + f" {DISCLAIMER}"}

def agente_lugares(state):
    prompt = f"Recomienda 3 lugares turísticos importantes para visitar según la ciudad de esta pregunta: {state['question']}. Usa viñetas."
    return {**state, "answer": call_openai(prompt) + f" {DISCLAIMER}"}

def agente_itinerario(state):
    prompt = (
        f"Genera un itinerario realista de viaje en base a esta consulta: {state['question']}.\n"
        "Debe incluir actividades para mañana, tarde y noche, recomendaciones de comida y un tip logístico por día.\n"
        "Usa un formato organizado por días con viñetas."
    )
    return {**state, "answer": call_openai(prompt, max_tokens=800) + f"\n{DISCLAIMER}"}

# -----------------------------
# Clasificador simple (igual que antes)
# -----------------------------
def clasificador(state):
    if state["blocked"]:
        return state
    q = state["question"].lower()
    if "clima" in q or "temperatura" in q:
        return {**state, "categoria": "clima"}
    elif "precio" in q or "costo" in q or "presupuesto" in q or "vale" in q or "cuesta" in q:
        return {**state, "categoria": "costos"}
    elif "itinerario" in q or "plan" in q:
        return {**state, "categoria": "itinerario"}
    elif "lugar" in q or "visitar" in q or "atracción" in q:
        return {**state, "categoria": "lugares"}
    return {**state, "categoria": "ninguna", "answer": "Lo siento, no tengo información sobre esa consulta."}

# -----------------------------
# Orquestador
# -----------------------------
def run_graph(question: str):
    st = {"question": question}
    st = guardrails(st)
    if st["blocked"]:
        return st
    st = clasificador(st)
    if st.get("categoria") == "ninguna":
        return st
    if st["categoria"] == "clima":
        return agente_clima(st)
    if st["categoria"] == "costos":
        return agente_costos(st)
    if st["categoria"] == "itinerario":
        return agente_itinerario(st)
    return agente_lugares(st)

# -----------------------------
# Endpoints
# -----------------------------
@app.route("/api/ask", methods=["POST"])
def ask():
    if not request.is_json:
        return jsonify({"answer": "La solicitud debe ser JSON."}), 400
    data = request.get_json(silent=True)
    if not data or "question" not in data:
        return jsonify({"answer": "Falta el campo 'question'."}), 400
    return jsonify(run_graph(data["question"]))

@app.route("/", methods=["GET"])
def serve_index():
    return send_from_directory(app.static_folder, "index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
