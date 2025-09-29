const form = document.querySelector("#travel-form");
const input = document.querySelector("#question");
const chatBox = document.querySelector("#chat-box");

function addMessage(text, sender) {
  const div = document.createElement("div");
  div.className = `message ${sender}`;
  div.textContent = text;
  chatBox.appendChild(div);
  chatBox.scrollTop = chatBox.scrollHeight;
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const question = input.value.trim();
  if (!question) return;

  addMessage(question, "user");
  input.value = "";

  const loading = document.createElement("div");
  loading.className = "message bot";
  loading.textContent = "⏳ Generando respuesta...";
  chatBox.appendChild(loading);
  chatBox.scrollTop = chatBox.scrollHeight;

  try {
    const res = await fetch("/api/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question })
    });

    if (!res.ok) {
      loading.textContent = `⚠️ Error del servidor (${res.status})`;
      return;
    }

    const data = await res.json();
    loading.textContent = data.answer || "⚠️ No se recibió respuesta del servidor.";
  } catch (err) {
    loading.textContent = `⚠️ Error de conexión: ${err.message}`;
  }
});
