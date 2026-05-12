const messages = document.getElementById("messages");
const input = document.getElementById("input");
const sendButton = document.getElementById("send");

const chatHistory = document.getElementById("chatHistory");

const newChatBtn = document.getElementById("newChatBtn");

const chatTitle = document.getElementById("chatTitle");

const statusElement = document.getElementById("status");

/* ================= CHAT DATA ================= */

let chats = [];

let currentChatId = null;

let loading = false;

let inactivityTimer;

/* ================= INIT ================= */

createNewChat();

updateStatusOnline();

/* ================= EVENTS ================= */

sendButton.addEventListener("click", sendMessage);

input.addEventListener("keyup", (event) => {

    updateStatusOnline();

    resetInactivityTimer();

    if(event.key === "Enter"){

        sendMessage();

    }

});

newChatBtn.addEventListener("click", () => {

    createNewChat();

});

/* ================= LOGIN ================= */

document
.getElementById("loginBtn")
.addEventListener("click", () => {

    document.getElementById("loginModal").style.display = "none";

});

/* ================= CHAT SYSTEM ================= */

function createNewChat(){

    const id = Date.now();

    const chat = {

        id,
        title:"Nova conversa",
        messages:[]
    };

    chats.unshift(chat);

    currentChatId = id;

    renderChatHistory();

    loadChat(id);

}

function renderChatHistory(){

    chatHistory.innerHTML = "";

    chats.forEach(chat => {

        const item = document.createElement("div");

        item.classList.add("history-item");

        if(chat.id === currentChatId){

            item.classList.add("active");

        }

        item.innerHTML = `

            <div class="chat-name">
                ${chat.title}
            </div>

            <div class="chat-actions">

                <button onclick="renameChat(${chat.id})">
                    ✏️
                </button>

                <button onclick="deleteChat(${chat.id})">
                    🗑️
                </button>

            </div>

        `;

        item.addEventListener("click", (e) => {

            if(
                e.target.tagName !== "BUTTON"
            ){

                loadChat(chat.id);

            }

        });

        chatHistory.appendChild(item);

    });

}

function loadChat(id){

    currentChatId = id;

    const chat = chats.find(c => c.id === id);

    if(!chat) return;

    document.getElementById("chat_title").textContent = chat.title;

    messages.innerHTML = "";

    if(chat.messages.length === 0){

        messages.innerHTML = `

            <div class="welcome">

                <h1>
                    Como posso ajudar você hoje?
                </h1>

                <p>
                    Faça perguntas ou interaja com o sistema.
                </p>

            </div>

        `;

    }else{

        chat.messages.forEach(msg => {

            createMessageElement(
                msg.content,
                msg.type
            );

        });

    }

    renderChatHistory();

}

function renameChat(id){

    const chat = chats.find(c => c.id === id);

    if(!chat) return;

    const newName = prompt(
        "Novo nome do chat:",
        chat.title
    );

    if(newName){

        chat.title = newName;

        if(currentChatId === id){

            document.getElementById("chat_title").textContent = newName;

        }

        renderChatHistory();

    }

}

function deleteChat(id){

    chats = chats.filter(chat => chat.id !== id);

    if(chats.length === 0){

        createNewChat();

        return;

    }

    if(currentChatId === id){

        currentChatId = chats[0].id;

    }

    renderChatHistory();

    loadChat(currentChatId);

}

/* ================= SEND MESSAGE ================= */

async function sendMessage(){

    if(loading) return;

    const text = input.value.trim();

    if(!text) return;

    removeWelcome();

    addMessage(text, "user");

    input.value = "";

    loading = true;

    updateStatusOnline();

    createTyping();

    try{

        const response = await fetchAPI(text);

        removeTyping();

        addMessage(response, "bot");

    }catch(error){

        removeTyping();

        addMessage(
            "Erro ao conectar com API.",
            "bot"
        );

        console.error(error);

    }

    loading = false;

}

/* ================= MESSAGE SYSTEM ================= */

function addMessage(content, type){

    const chat = chats.find(
        c => c.id === currentChatId
    );

    if(!chat) return;

    chat.messages.push({
        content,
        type
    });

    if(
        chat.title === "Nova conversa"
        &&
        type === "user"
    ){

        chat.title = content.slice(0, 25);

        document.getElementById("chat_title").textContent = chat.title;
        renderChatHistory();

    }

    createMessageElement(content, type);

}

function createMessageElement(content, type){

    const message = document.createElement("div");

    message.classList.add(
        "message",
        type
    );

    message.innerHTML = content;

    messages.appendChild(message);

    scrollBottom();

}

/* ================= TYPING ================= */

function createTyping(){

    const typing = document.createElement("div");

    typing.classList.add(
        "message",
        "bot"
    );

    typing.id = "typing";

    typing.innerHTML = "Digitando...";

    messages.appendChild(typing);

    scrollBottom();

}

function removeTyping(){

    const typing = document.getElementById("typing");

    if(typing){

        typing.remove();

    }

}

/* ================= WELCOME ================= */

function removeWelcome(){

    const welcome = document.querySelector(".welcome");

    if(welcome){

        welcome.remove();

    }

}

/* ================= STATUS ================= */

function updateStatusOnline(){

    statusElement.innerHTML = "● Online";

    statusElement.classList.remove("away");

    statusElement.classList.add("online");

}

function updateStatusAway(){

    statusElement.innerHTML = "● Ausente";

    statusElement.classList.remove("online");

    statusElement.classList.add("away");

}

function resetInactivityTimer(){

    clearTimeout(inactivityTimer);

    inactivityTimer = setTimeout(() => {

        updateStatusAway();

    }, 60000);

}

resetInactivityTimer();

/* ================= SCROLL ================= */

function scrollBottom(){

    messages.scrollTop =
    messages.scrollHeight;

}

/* ================= API ================= */

async function fetchAPI(message){

    const response = await fetch(

        `http://127.0.0.1:5000/sendmensage/API/${encodeURIComponent(message)}`

    );

    const data = await response.json();

    let formattedData = "";

    Object.keys(
        data.Response.dados
    ).forEach((key) => {

        formattedData += `

            <strong>${key}</strong>:
            ${data.Response.dados[key]}
            <br>

        `;

    });

    return `

        <strong>Ação:</strong>
        ${data.Response.acao}
        <br><br>

        ${formattedData}

        <br>

        <strong>Sentimento:</strong>
        ${data.Response.sentimento}

    `;

}