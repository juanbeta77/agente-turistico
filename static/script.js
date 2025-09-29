const form = document.querySelector("form");
const input = document.querySelector("#question");
const output = document.querySelector("#answer");

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const pregunta = input.value.trim();
  if (!pregunta) {
    output.textContent = "⚠️ Por favor escribe una pregunta.";
    return;
  }

  output.textContent = "⏳ Generando respuesta...";

  try {
    const res = await fetch("/api/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question: pregunta }),
    });

    const data = await res.json();
    output.textContent = data.answer || "⚠️ El servidor no devolvió respuesta.";
  } catch (err) {
    output.textContent = `⚠️ Error de conexión: ${err.message}`;
  }
});
