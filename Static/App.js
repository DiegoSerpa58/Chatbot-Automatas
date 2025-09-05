const chatBox = document.getElementById("chat-box");
const input = document.getElementById("user-input");
const sendBtn = document.getElementById("send-btn");

let userName = null;
let waitingForContinue = false; // flag para saber si estamos en "y/n"

// Función para agregar mensajes al chat
function addMessage(text, sender="bot") {
  const div = document.createElement("div");
  div.className = sender;
  div.textContent = text;
  chatBox.appendChild(div);
  chatBox.scrollTop = chatBox.scrollHeight;
}
// Mensaje inicial
async function sendMessage() {
  const msg = input.value.trim();
  if (!msg) return;
  addMessage(msg, "user");

  // Si estamos esperando la respuesta de continuar (y/n)
  if (waitingForContinue) {
    if (msg.toLowerCase() === "y") {
      addMessage("👉 Great! Type your next sentence.");
      waitingForContinue = false;
    } else if (msg.toLowerCase() === "n") {
      addMessage("👋 Thanks for practicing! See you next time.");
      input.disabled = true;
      sendBtn.disabled = true;
    } else {
      addMessage("⚠️ Please type 'y' for yes or 'n' for no.");
    }
    input.value = "";
    return;
  }

  // Si aún no se sabe el nombre
  if (!userName) {
    if (!isValidName(msg)) {
      addMessage("⚠️ Please enter a valid name (start with uppercase, letters only, no spaces or special characters).");
      input.value = "";
      return;
    }
    userName = msg;
    addMessage(`Nice to meet you, ${userName}! Please type a sentence in English using the verb TO BE (present or past).`);
  } else {
    // Validar la oración en el backend
    const res = await fetch("/validate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ sentence: msg })
    });
    const data = await res.json();
    addMessage(data.result);

    // Solo preguntar si quiere continuar si la sentencia es correcta
    if (data.result.startsWith("✅")) {
      addMessage("❓ Do you want to continue? (y/n)");
      waitingForContinue = true;
    }
  }

  input.value = "";
}

// Función para validar nombre (solo letras, sin espacios ni caracteres especiales, y empieza con mayúscula)
function isValidName(name) {
  return /^[A-Z][a-zA-Z]*$/.test(name);
}

sendBtn.addEventListener("click", sendMessage);
input.addEventListener("keypress", e => {
  if (e.key === "Enter") sendMessage();
});
