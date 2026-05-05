var ChatManager = {
    chatCount: 0,
    activeChatId: null,
    chats: {},

    init: function() {
        this.createNewChat("ChatBot01");
        this.setupToggleSidebar();
    },

    setupToggleSidebar: function() {
        const toggleBtn = document.getElementById("toggleSidebarBtn");
        const sidebar = document.getElementById("sidebar");
        
        if (toggleBtn && sidebar) {
            toggleBtn.addEventListener("click", function(e) {
                e.stopPropagation();
                sidebar.classList.toggle("collapsed");
                toggleBtn.classList.toggle("collapsed");
                
                // Ajustar margin do body
                if (sidebar.classList.contains("collapsed")) {
                    document.body.style.marginLeft = "0";
                } else {
                    document.body.style.marginLeft = "200px";
                }
            });
        }
    },

    // Criar novo chat
    createNewChat: function(name) {
        this.chatCount++;
        const chatId = "chat_" + this.chatCount;
        
        if (!name) {
            name = "ChatBot" + String(this.chatCount).padStart(2, '0');
        }

        // Criar elemento do chat no menu lateral
        this.createSidebarItem(chatId, name);

        // Criar elemento da página do chat
        this.createChatPage(chatId, name);

        // Ativar o novo chat
        this.switchToChat(chatId);

        return chatId;
    },

    // Criar item na barra lateral
    createSidebarItem: function(chatId, name) {
        const sidebar = document.getElementById("chatList");
        if (!sidebar) return;

        const chatItem = document.createElement("div");
        chatItem.className = "chat-item";
        chatItem.id = "item_" + chatId;
        
        // Clique no item = trocar de conversa
        chatItem.onclick = function() {
            ChatManager.switchToChat(chatId);
        };

        // Nome do chat (clicável para renomear)
        const chatName = document.createElement("span");
        chatName.className = "chat-name";
        chatName.id = "name_" + chatId;
        chatName.textContent = name;
        chatName.title = "Clique para renomear";
        chatName.onclick = function(e) {
            e.stopPropagation();
            ChatManager.promptRenameChat(chatId);
        };

        // Botão de menu (três pontinhos)
        const menuBtn = document.createElement("button");
        menuBtn.className = "chat-menu-btn";
        menuBtn.textContent = "...";
        menuBtn.title = "Opções";
        menuBtn.onclick = function(e) {
            e.stopPropagation();
            ChatManager.toggleDropdown(chatId);
        };

        // Menu dropdown
        const dropdown = document.createElement("div");
        dropdown.className = "chat-dropdown";
        dropdown.id = "dropdown_" + chatId;
        
        // Opção Renomear
        const renameItem = document.createElement("div");
        renameItem.className = "chat-dropdown-item";
        renameItem.textContent = "Renomear";
        renameItem.onclick = function(e) {
            e.stopPropagation();
            ChatManager.hideAllDropdowns();
            ChatManager.promptRenameChat(chatId);
        };
        
        // Opção Deletar
        const deleteItem = document.createElement("div");
        deleteItem.className = "chat-dropdown-item delete";
        deleteItem.textContent = "Deletar chat";
        deleteItem.onclick = function(e) {
            e.stopPropagation();
            ChatManager.hideAllDropdowns();
            ChatManager.deleteChat(chatId);
        };
        
        dropdown.appendChild(renameItem);
        dropdown.appendChild(deleteItem);
        
        chatItem.appendChild(chatName);
        chatItem.appendChild(menuBtn);
        chatItem.appendChild(dropdown);
        sidebar.appendChild(chatItem);
    },

    // Alternar menu dropdown
    toggleDropdown: function(chatId) {
        const dropdown = document.getElementById("dropdown_" + chatId);
        const isShown = dropdown.classList.contains("show");
        
        // Fechar todos os dropdowns
        this.hideAllDropdowns();
        
        // Se não estava mostrado, mostrar este
        if (!isShown) {
            dropdown.classList.add("show");
        }
    },

    // Fechar todos os dropdowns
    hideAllDropdowns: function() {
        const dropdowns = document.querySelectorAll(".chat-dropdown");
        dropdowns.forEach(d => d.classList.remove("show"));
    },

    // Criar página do chat
    createChatPage: function(chatId, name) {
        // Remover página inicial se existir
        const initialPage = document.querySelector('.page');
        if (initialPage && !this.chatCount > 1) {
            initialPage.id = "chat_page_1";
        }

        const newPage = document.createElement("div");
        newPage.className = "page";
        newPage.id = chatId;
        newPage.style.display = "none";

        newPage.innerHTML = `
            <nav class="nav">
                <ul>
                    <li class="bold">Deteflect</li>
                    <li class='content'>${name}</li>
                </ul>
            </nav>
            <div class='msgs' id='msg_input_${chatId}'>
                <div id="welcome_${chatId}" class="welcome">
                    <h1>Welcome to Deteflect Framework</h1>
                    <h3>How can I help you?</h3>
                </div>
            </div>
            <div class='input_sender'>
                <input type="text" name="input" id="input_${chatId}" class="chat-input" data-chat-id="${chatId}">
                <button type="submit" id="send_${chatId}" class="chat-send-btn" data-chat-id="${chatId}">Send</button>
            </div>
        `;

        document.body.insertBefore(newPage, document.querySelector("footer"));

        // Armazenar referência
        this.chats[chatId] = {
            name: name,
            isFirst: true
        };

        // Configurar eventos do novo chat
        this.setupChatEvents(chatId);
    },

    // Configurar eventos do chat
    setupChatEvents: function(chatId) {
        const input = document.getElementById("input_" + chatId);
        const sendBtn = document.getElementById("send_" + chatId);

        if (input && sendBtn) {
            // Evento de clique no botão enviar
            sendBtn.addEventListener("click", function() {
                const chatId = this.getAttribute("data-chat-id");
                ChatManager.sendMessage(chatId);
            });

            // Evento de Enter no input
            input.addEventListener("keyup", function(event) {
                if (event.key === "Enter") {
                    event.preventDefault();
                    const chatId = this.getAttribute("data-chat-id");
                    ChatManager.sendMessage(chatId);
                }
            });
        }
    },

    // Enviar mensagem
    sendMessage: function(chatId) {
        const input = document.getElementById("input_" + chatId);
        const msgInput = document.getElementById("msg_input_" + chatId);
        
        if (!input || !msgInput) return;

        const messageText = input.value.trim();
        if (messageText === "") return;

        const chatData = this.chats[chatId];
        if (!chatData) return;

        // Esconder mensagem de boas-vindas na primeira mensagem
        if (chatData.isFirst) {
            const welcome = document.getElementById("welcome_" + chatId);
            if (welcome) {
                welcome.classList.add("bye");
                setTimeout(() => {
                    welcome.remove();
                }, 1000);
            }
            chatData.isFirst = false;
        }

        // Criar mensagem do usuário
        const msgElement = document.createElement("div");
        msgElement.className = "msg_sender";
        msgElement.textContent = messageText;
        msgInput.appendChild(msgElement);

        // Limpar input
        input.value = "";

        // Enviar para API e obter resposta
        this.callAPI(messageText, chatId);
    },

    // Chamar API
    callAPI: async function(msg, chatId) {
        const msgInput = document.getElementById("msg_input_" + chatId);
        
        try {
            const response = await fetch('http://127.0.0.1:5000/sendmensage/API/' + msg);
            const data = await response.json();
            const responseText = data;

            // Criar mensagem de resposta
            const msgElement = document.createElement("div");
            msgElement.className = "msg_receiver";

            console.log(responseText["Config"]["FormResponse"]["Form_format_rule"])
            if(responseText["Config"]["FormResponse"] == 'true'){
                let Campos = responseText["Field"].replace('[','').replace(']','').split(',');
                let Fields_campos =""
                Campos.forEach(element => {
                    element = element.replace('[','').replace(']','').replace("'",'').replace("'","").replace(" ","")
                    Fields_campos += `<label for="${element}">${element}</label><input type="text" name="${element}"><br>`
                });


                let ChatText = `SendForm('dddd','base',${chatId})`
                let ElementResponse = `
                
                <div>
                Here is the form to carry out the manipulation of the mentioned data
                </div>
                <br>
                <iframe id="hiddenFrame" name="hiddenFrame" style="display: none;"></iframe>
                <form id='form_data' class='formDataPrompt' target="hiddenFrame">
                  ${Fields_campos}
                  <button id='send_forms' onclick=${ChatText}  type="submit">Send</button>
                </form>
                `
                msgElement.innerHTML = ElementResponse
            }
            else{
                msgElement.innerHTML = responseText["Response"];
            }
            msgInput.appendChild(msgElement);

            // Scroll para baixo
            msgInput.scrollTop = msgInput.scrollHeight;
        } catch (error) {
            console.error("Erro ao chamar API:", error);
        }
    },
    
    // Trocar para outro chat
    switchToChat: function(chatId) {
        // Fechar todos os dropdowns antes de trocar
        this.hideAllDropdowns();
        
        // Ocultar todos os chats
        const pages = document.querySelectorAll('.page');
        pages.forEach(page => {
            page.style.display = "none";
        });

        // Mostrar chat selecionado
        const selectedPage = document.getElementById(chatId);
        if (selectedPage) {
            selectedPage.style.display = "block";
        }

        // Atualizar item selecionado na barra lateral
        const items = document.querySelectorAll('.chat-item');
        items.forEach(item => {
            item.classList.remove('active');
        });

        const activeItem = document.getElementById("item_" + chatId);
        if (activeItem) {
            activeItem.classList.add('active');
        }

        this.activeChatId = chatId;
    },

    // Renomear chat
    promptRenameChat: function(chatId) {
        const currentName = this.chats[chatId]?.name || "Chat";
        const newName = prompt("Digite o novo nome do chat:", currentName);
        
        if (newName && newName.trim() !== "") {
            this.renameChat(chatId, newName.trim());
        }
    },

    renameChat: function(chatId, newName) {
        // Atualizar nome na barra lateral
        const nameElement = document.getElementById("name_" + chatId);
        if (nameElement) {
            nameElement.textContent = newName;
        }

        // Atualizar nome no cabeçalho do chat
        const page = document.getElementById(chatId);
        if (page) {
            const navContent = page.querySelector('.content');
            if (navContent) {
                navContent.textContent = newName;
            }
        }

        // Atualizar dados
        if (this.chats[chatId]) {
            this.chats[chatId].name = newName;
        }
    },

    // Deletar chat
    deleteChat: function(chatId) {
        // Não permitir excluir se for o único chat
        if (Object.keys(this.chats).length <= 1) {
            alert("Não é possível excluir o último chat!");
            return;
        }

        // Confirmar exclusão
        if (!confirm("Tem certeza que deseja excluir este chat?")) {
            return;
        }

        // Remover item da barra lateral
        const sidebarItem = document.getElementById("item_" + chatId);
        if (sidebarItem) {
            sidebarItem.remove();
        }

        // Remover página do chat
        const chatPage = document.getElementById(chatId);
        if (chatPage) {
            chatPage.remove();
        }

        // Remover dos dados
        delete this.chats[chatId];

        // Se era o chat ativo, trocar para outro
        if (this.activeChatId === chatId) {
            const firstChatId = Object.keys(this.chats)[0];
            if (firstChatId) {
                this.switchToChat(firstChatId);
            }
        }
    },

    // Obter chat ativo
    getActiveChat: function() {
        return this.activeChatId;
    }
};

// Inicializar quando o DOM estiver pronto
document.addEventListener("DOMContentLoaded", function() {
    ChatManager.init();
    
    // Adicionar evento ao botão de novo chat
    const newChatBtn = document.getElementById("newChatBtn");
    if (newChatBtn) {
        newChatBtn.addEventListener("click", function() {
            ChatManager.createNewChat();
        });
    }
    
    // Fechar dropdowns ao clicar fora
    document.addEventListener("click", function(e) {
        if (!e.target.closest(".chat-item")) {
            ChatManager.hideAllDropdowns();
        }
    });
});

async function SendForm(msg,idname, chatId) {
    document.getElementById("send_forms").remove();
       var el =  document.getElementById("form_data")
          el.id = "generic_id";
        const inputs = el.querySelectorAll("input");
        inputs.forEach(input => {
            input.disabled = true;
        });
        var form = document.getElementById('form_data');
        resultForm ={}
        const dados = new FormData(el);
         for (const [campo, valor] of dados.entries()) {
             resultForm[campo] = valor;
        }
        const response = await fetch('http://127.0.0.1:5000/forms/send?data='+idname+'',{method: 'POST',
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(resultForm)});
            const data = await response.json();
            const responseText = data["Response"];
            console.log(responseText)
        const msgInput = document.getElementById('msg_input_'+chatId.id);
        const msgElement = document.createElement("div");
        msgElement.classList+='msg_receiver'
        msgElement.className = "msg_receiver";
        if(responseText["Response"]  != '1'){
            console.log(responseText["Response"][1])
            Resp =responseText["Response"][1].split(":")[1].replace("\"","")
            msgElement.innerHTML = Resp
            msgInput.appendChild(msgElement);
        }
    }