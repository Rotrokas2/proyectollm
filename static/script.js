// script.js
const formChat = document.getElementById("form-chat");
const promptInput = document.getElementById("prompt");
const chatWindow = document.getElementById("chat-window");

// Función para agregar un mensaje al chat
function agregarMensaje(role, texto) {
  const msgDiv = document.createElement("div");
  msgDiv.classList.add("message", role);

  const roleSpan = document.createElement("div");
  roleSpan.classList.add("role");
  roleSpan.textContent = role === "user" ? "Tú:" : "Asistente:";

  const contentP = document.createElement("p");
  contentP.textContent = texto;

  msgDiv.appendChild(roleSpan);
  msgDiv.appendChild(contentP);
  chatWindow.appendChild(msgDiv);

  // Hacer scroll automático hacia abajo
  chatWindow.scrollTop = chatWindow.scrollHeight;
}

formChat.addEventListener("submit", async (e) => {
  e.preventDefault();
  const prompt = promptInput.value.trim();
  if (!prompt) return;

  // 1) Mostrar el mensaje del usuario
  agregarMensaje("user", prompt);
  promptInput.value = "";
  promptInput.disabled = true;

  // 2) Hacer la petición al endpoint /chat
  try {
    const respuesta = await fetch("/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ prompt: prompt }),
    });

    if (!respuesta.ok) {
      throw new Error(`Error ${respuesta.status}`);
    }

    const data = await respuesta.json();
    // 3) Mostrar la respuesta del asistente
    agregarMensaje("assistant", data.response);
  } catch (error) {
    console.error("Error al llamar a /chat:", error);
    agregarMensaje("assistant", "Lo siento, ocurrió un error al procesar tu petición.");
  } finally {
    promptInput.disabled = false;
    promptInput.focus();
  }
});
