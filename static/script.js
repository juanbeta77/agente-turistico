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
      body: JSON.stringify({ question: pregunta })
    });

    if (!res.ok) {
      const texto = await res.text();
      output.textContent = `⚠️ Error del servidor (${res.status}): ${texto}`;
      return;
    }

    let data;
    try {
      data = await res.json();
    } catch (err) {
      const texto = await res.text();
      output.textContent = `⚠️ Respuesta no es JSON válido:\n${texto}`;
      return;
    }

    output.textContent = data.answer || "⚠️ El servidor no devolvió respuesta.";
  } catch (err) {
    output.textContent = `⚠️ No se pudo conectar con el servidor:\n${err.message}`;
  }
});
