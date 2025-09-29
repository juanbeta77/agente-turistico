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
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ question: pregunta }),
    });

    if (!res.ok) {
      // Respuesta HTTP no fue 200-299
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

    // Si todo bien, mostrar la respuesta
    output.textContent = data.answer || "⚠️ El servidor no devolvió respuesta.";
  } catch (err) {
    // Error de red o fallo inesperado
    output.textContent = `⚠️ No se pudo conectar con el servidor:\n${err.message}`;
  }
});
