const form = document.getElementById("form");
const input = document.getElementById("q");
const resultDiv = document.getElementById("resultado");

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const question = input.value.trim();
  if (!question) return alert("Por favor ingresa una pregunta");

  resultDiv.textContent = "⏳ Generando itinerario...";
  try {
    const res = await fetch("/api/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question })
    });
    const data = await res.json();
    if (data.error) {
      resultDiv.textContent = "⚠️ " + data.error;
    } else {
      resultDiv.textContent = data.answer;
    }
  } catch (err) {
    resultDiv.textContent = "⚠️ Error en la solicitud: " + err;
  }
});
