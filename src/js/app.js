// Este script substitui o Vue e implementa a interface de chat apenas com HTML, CSS e JS.
(function () {
  function normalizeFields(fieldValue) {
    if (!fieldValue) return [];
    if (Array.isArray(fieldValue)) return fieldValue.map(String);
    return String(fieldValue)
      .replaceAll("[", "")
      .replaceAll("]", "")
      .split(",")
      .map((s) => s.replaceAll("'", "").trim())
      .filter(Boolean);
  }

  function makeId(prefix) {
    return `${prefix}_${Math.random().toString(16).slice(2)}_${Date.now()}`;
  }

  const App = {
    state: {
      chats: [],
      activeChatId: null,
      dropdownChatId: null,
      auth: {
        username: "",
        password: "",
        loading: false,
      },
    },

    els: {},

    init() {
      this.els.chatList = document.getElementById("chatList");
      this.els.activeChatName = document.getElementById("activeChatName");
      this.els.messagesViewport = document.getElementById("messagesViewport");
      this.els.composerInput = document.getElementById("composerInput");
      this.els.sendBtn = document.getElementById("sendBtn");
      this.els.newChatBtn = document.getElementById("newChatBtn");
      this.els.toggleSidebarBtn = document.getElementById("toggleSidebarBtn");
      this.els.sidebar = document.getElementById("sidebar");
      this.els.loginModal = document.getElementById("loginModal");
      this.els.loginBtn = document.getElementById("loginBtn");
      this.els.usernameInput = document.getElementById("username");
      this.els.passwordInput = document.getElementById("password");

      this.attachEvents();
      this.createNewChat();
      this.bootSecurity();
    },

    get activeChat() {
      return this.state.chats.find((chat) => chat.id === this.state.activeChatId) || null;
    },

    attachEvents() {
      if (this.els.newChatBtn) {
        this.els.newChatBtn.addEventListener("click", () => this.createNewChat());
      }

      if (this.els.toggleSidebarBtn) {
        this.els.toggleSidebarBtn.addEventListener("click", (event) => {
          event.stopPropagation();
          this.toggleSidebar();
        });
      }

      if (this.els.sendBtn) {
        this.els.sendBtn.addEventListener("click", () => this.sendMessage());
      }

      if (this.els.composerInput) {
        this.els.composerInput.addEventListener("keydown", (event) => {
          if (event.key === "Enter") {
            event.preventDefault();
            this.sendMessage();
          }
        });
      }

      if (this.els.loginBtn) {
        this.els.loginBtn.addEventListener("click", () => this.login());
      }

      if (this.els.usernameInput) {
        this.els.usernameInput.addEventListener("keydown", (event) => {
          if (event.key === "Enter") {
            event.preventDefault();
            this.els.passwordInput?.focus();
          }
        });
      }

      if (this.els.passwordInput) {
        this.els.passwordInput.addEventListener("keydown", (event) => {
          if (event.key === "Enter") {
            event.preventDefault();
            this.login();
          }
        });
      }

      document.addEventListener("click", (event) => {
        if (!event.target.closest(".chat-dropdown") && !event.target.closest(".chat-menu-btn")) {
          this.hideDropdowns();
        }
      });

      if (this.els.loginModal) {
        this.els.loginModal.addEventListener("click", (event) => {
          if (event.target === this.els.loginModal) {
            this.setLoginModal(false);
          }
        });
      }
    },

    setLoginModal(open) {
      if (!this.els.loginModal) return;
      this.els.loginModal.classList.toggle("show", open);
    },

    toggleSidebar() {
      const collapsed = !this.els.sidebar.classList.contains("collapsed");
      this.els.sidebar.classList.toggle("collapsed", collapsed);
      document.body.classList.toggle("sidebar-collapsed", collapsed);
    },

    createNewChat(name) {
      const id = makeId("chat");
      const label = name && String(name).trim()
        ? String(name).trim()
        : `ChatBot${String(this.state.chats.length + 1).padStart(2, "0")}`;

      this.state.chats.unshift({
        id,
        name: label,
        isFirst: true,
        messages: [],
      });

      this.switchToChat(id);
      this.renderChatList();
    },

    switchToChat(chatId) {
      this.state.activeChatId = chatId;
      this.state.dropdownChatId = null;
      this.renderChatList();
      this.renderActiveChat();
    },

    renderChatList() {
      if (!this.els.chatList) return;
      this.els.chatList.innerHTML = "";

      this.state.chats.forEach((chat) => {
        const item = document.createElement("div");
        item.className = `chat-item${chat.id === this.state.activeChatId ? " active" : ""}`;

        item.addEventListener("click", () => this.switchToChat(chat.id));

        const title = document.createElement("span");
        title.className = "chat-name";
        title.textContent = chat.name;
        title.title = chat.name;
        title.addEventListener("click", (event) => {
          event.stopPropagation();
          this.renameChat(chat.id);
        });

        const menuBtn = document.createElement("button");
        menuBtn.className = "chat-menu-btn";
        menuBtn.textContent = "...";
        menuBtn.title = "Opções";
        menuBtn.addEventListener("click", (event) => {
          event.stopPropagation();
          this.toggleDropdown(chat.id);
        });

        const dropdown = document.createElement("div");
        dropdown.className = `chat-dropdown${this.state.dropdownChatId === chat.id ? " show" : ""}`;

        const renameItem = document.createElement("div");
        renameItem.className = "chat-dropdown-item";
        renameItem.textContent = "Renomear";
        renameItem.addEventListener("click", (event) => {
          event.stopPropagation();
          this.hideDropdowns();
          this.renameChat(chat.id);
        });

        const deleteItem = document.createElement("div");
        deleteItem.className = "chat-dropdown-item delete";
        deleteItem.textContent = "Deletar chat";
        deleteItem.addEventListener("click", (event) => {
          event.stopPropagation();
          this.hideDropdowns();
          this.deleteChat(chat.id);
        });

        dropdown.appendChild(renameItem);
        dropdown.appendChild(deleteItem);
        item.appendChild(title);
        item.appendChild(menuBtn);
        item.appendChild(dropdown);
        this.els.chatList.appendChild(item);
      });
    },

    hideDropdowns() {
      if (this.state.dropdownChatId !== null) {
        this.state.dropdownChatId = null;
        this.renderChatList();
      }
    },

    toggleDropdown(chatId) {
      this.state.dropdownChatId = this.state.dropdownChatId === chatId ? null : chatId;
      this.renderChatList();
    },

    renameChat(chatId) {
      const chat = this.state.chats.find((item) => item.id === chatId);
      if (!chat) return;
      const nextName = prompt("Digite o novo nome do chat:", chat.name);
      if (nextName && nextName.trim()) {
        chat.name = nextName.trim();
        this.renderChatList();
        this.renderActiveChat();
      }
    },

    deleteChat(chatId) {
      if (this.state.chats.length <= 1) {
        alert("Não é possível excluir o último chat!");
        return;
      }
      if (!confirm("Tem certeza que deseja excluir este chat?")) return;

      const index = this.state.chats.findIndex((chat) => chat.id === chatId);
      if (index === -1) return;
      const wasActive = this.state.activeChatId === chatId;
      this.state.chats.splice(index, 1);
      if (wasActive) {
        this.state.activeChatId = this.state.chats[0]?.id || null;
      }
      this.renderChatList();
      this.renderActiveChat();
    },

    renderActiveChat() {
      const activeChat = this.activeChat;
      if (!this.els.activeChatName || !this.els.messagesViewport) return;

      this.els.activeChatName.textContent = activeChat ? activeChat.name : "Documentation";
      this.els.messagesViewport.innerHTML = "";

      if (!activeChat) return;

      if (activeChat.isFirst) {
        const welcome = document.createElement("div");
        welcome.id = "welcome";
        welcome.innerHTML = `
          <h1>Welcome to Deteflect Framework</h1>
          <h3>How can I help you?</h3>
        `;
        this.els.messagesViewport.appendChild(welcome);
      }

      activeChat.messages.forEach((message, index) => {
        const element = this.createMessageElement(message, index);
        this.els.messagesViewport.appendChild(element);
      });

      this.scrollChat();
    },

    createMessageElement(message, index) {
      if (message.role === "user") {
        const wrapper = document.createElement("div");
        wrapper.className = "msg_sender";
        wrapper.textContent = message.text;
        return wrapper;
      }

      const wrapper = document.createElement("div");
      wrapper.className = "msg_receiver";

      if (message.type === "form") {
        const description = document.createElement("div");
        description.textContent = "Here is the form to carry out the manipulation of the mentioned data";
        wrapper.appendChild(description);

        const form = document.createElement("form");
        form.className = "formDataPrompt";
        form.addEventListener("submit", (event) => {
          event.preventDefault();
          this.submitForm(index, form);
        });

        const formGrid = document.createElement("div");
        formGrid.className = "form-grid";

        message.fields.forEach((field) => {
          const row = document.createElement("div");
          row.className = "form-row";

          const label = document.createElement("label");
          label.htmlFor = `field_${message.idname || "base"}_${field}`;
          label.textContent = field;

          const input = document.createElement("input");
          input.type = "text";
          input.name = field;
          input.id = label.htmlFor;
          input.value = message.form[field] || "";
          input.disabled = Boolean(message.submitting || message.submitted);
          input.addEventListener("input", (evt) => {
            message.form[field] = evt.target.value;
          });

          row.appendChild(label);
          row.appendChild(input);
          formGrid.appendChild(row);
        });

        const actions = document.createElement("div");
        actions.className = "form-actions";

        const submitBtn = document.createElement("button");
        submitBtn.type = "submit";
        submitBtn.disabled = Boolean(message.submitting || message.submitted);
        submitBtn.textContent = message.submitted ? "Sent" : message.submitting ? "..." : "Send";

        actions.appendChild(submitBtn);
        form.appendChild(formGrid);
        form.appendChild(actions);
        wrapper.appendChild(form);
        return wrapper;
      }

      const span = document.createElement("span");
      span.innerHTML = message.html || "";
      wrapper.appendChild(span);
      return wrapper;
    },

    scrollChat() {
      if (!this.els.messagesViewport) return;
      const viewport = this.els.messagesViewport;
      const target = Math.max(viewport.scrollHeight - 80, 0);
      viewport.scrollTop = target;
    },

    animateSendButton() {
      if (!this.els.sendBtn) return;
      this.els.sendBtn.classList.add("send-margin");
      window.setTimeout(() => {
        this.els.sendBtn.classList.remove("send-margin");
      }, 250);
    },

    async sendMessage() {
      const activeChat = this.activeChat;
      const input = this.els.composerInput;
      if (!activeChat || !input) return;

      const text = input.value.trim();
      if (!text) return;

      activeChat.isFirst = false;
      activeChat.messages.push({ role: "user", text });
      input.value = "";
      this.renderActiveChat();
      this.animateSendButton();

      try {
        const data = await ApiClient.sendMessage(text);
        const wantsForm = data?.Config?.FormResponse != "true" || data?.Config?.FormResponse === true;

        if (wantsForm) {
          const fields = normalizeFields(data?.Field);
          const formData = {};
          fields.forEach((field) => {
            formData[field] = "";
          });
          activeChat.messages.push({
            role: "bot",
            type: "form",
            fields,
            form: formData,
            submitting: false,
            submitted: false,
            idname: "base",
          });
        } else {
          activeChat.messages.push({
            role: "bot",
            type: "html",
            html: String(data?.Response ?? ""),
          });
        }
      } catch (error) {
        console.error("Erro ao chamar API:", error);
        activeChat.messages.push({
          role: "bot",
          type: "html",
          html: "Erro ao chamar API. Verifique se o backend está rodando.",
        });
      } finally {
        this.renderActiveChat();
      }
    },

    async submitForm(index, formElement) {
      const activeChat = this.activeChat;
      if (!activeChat) return;
      const message = activeChat.messages[index];
      if (!message || message.submitting || message.submitted) return;

      message.fields.forEach((field) => {
        const input = formElement.querySelector(`[name="${field}"]`);
        if (input) {
          message.form[field] = input.value;
        }
      });

      message.submitting = true;
      this.renderActiveChat();

      try {
        const response = await ApiClient.sendForm(message.idname || "base", message.form || {});
        message.submitted = true;

        const resp = response?.Response;
        let html = "";
        if (Array.isArray(resp) && resp.length > 1 && typeof resp[1] === "string") {
          html = String(resp[1]).split(":").slice(1).join(":").replaceAll('"', "").trim();
        } else if (typeof resp === "string") {
          html = resp;
        } else {
          html = "Form enviado.";
        }

        activeChat.messages.push({ role: "bot", type: "html", html });
      } catch (error) {
        console.error("Erro ao enviar form:", error);
        activeChat.messages.push({
          role: "bot",
          type: "html",
          html: "Erro ao enviar o formulário.",
        });
      } finally {
        message.submitting = false;
        this.renderActiveChat();
      }
    },

    async bootSecurity() {
      try {
        const cfg = await ApiClient.readConfig();
        if (cfg && cfg.security_enabled === true) {
          this.setLoginModal(true);
        }
      } catch (error) {
        console.warn("Falha ao ler config:", error);
      }
    },

    async login() {
      const username = this.els.usernameInput?.value.trim();
      const password = this.els.passwordInput?.value || "";
      if (!username || !password) {
        alert("Por favor, preencha todos os campos!");
        return;
      }

      this.state.auth.loading = true;
      if (this.els.loginBtn) this.els.loginBtn.textContent = "...";

      try {
        const res = await ApiClient.loginSession(password, username);
        if (res && res.success === true) {
          this.setLoginModal(false);
          if (this.els.passwordInput) this.els.passwordInput.value = "";
        } else {
          alert("Login ou senha incorretos");
        }
      } catch (error) {
        console.error(error);
        alert("Não foi possível efetuar login (API offline?)");
      } finally {
        this.state.auth.loading = false;
        if (this.els.loginBtn) this.els.loginBtn.textContent = "Enter";
      }
    },
  };

  document.addEventListener("DOMContentLoaded", () => App.init());
})();

