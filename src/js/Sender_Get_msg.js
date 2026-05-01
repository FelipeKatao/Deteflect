
// Este arquivo agora usa o ChatManager para gerenciar múltiplos chats
// As funcionalidades foram movidas para ChatsGenerate.js

// Variáveis globais para compatibilidade (usadas pelo ChatManager)
var Isprimeiro = true
var Loading = false
var msgUser = ""

// Função para enviar mensagem (usada pelo ChatManager)
function sendMessageToAPI(msg, chatId) {
    ReadAPI(msg).then(inputData => {
        const msgInput = document.getElementById("msg_input_" + chatId);
        if (!msgInput) return;
        
        const msgElement = document.createElement("div");
        msgElement.classList.add("msg_receiver");
        msgElement.innerHTML = inputData;
        msgInput.appendChild(msgElement);
        
        // Habilitar input novamente
        const input = document.getElementById("input_" + chatId);
        if (input) {
            input.disabled = false;
        }
        
        Loading = false;
    });
}

// Função ReadAPI mantida para compatibilidade
async function ReadAPI(msg){
    const response = await fetch('http://127.0.0.1:5000/sendmensage/API/' + msg);
    const data = await response.json();
    return data["Response"]
}

