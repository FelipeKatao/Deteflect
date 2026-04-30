var modal = document.getElementById("loginModal");
var loginBtn = document.getElementById("loginBtn");
var closeBtn = document.getElementById("closeModal");
var usernameInput = document.getElementById("username");
var passwordInput = document.getElementById("password");

// Show modal on page load
window.onload = async function() {
    const result = await ReadConfig()
    if (result["security_enabled"] == true){
        modal.style.display = "block";
    }
};

loginBtn.addEventListener("click", async function() {
    var username = usernameInput.value;
    var password = passwordInput.value;
    
    if (username === "" || password === "") {
        alert("Por favor, preencha todos os campos!");
        return;
    }
    var Login = await LoginSession(password,username)
    if (Login["success"] == true){
        modal.style.display = "none";
    }
    else{
        alert("Login ou senha incorretos")
    }
});

passwordInput.addEventListener("keyup", function(event) {
    if (event.key === "Enter") {
        loginBtn.click();
    }
});

usernameInput.addEventListener("keyup", function(event) {
    if (event.key === "Enter") {
        passwordInput.focus();
    }
});


async function ReadConfig(){
const response = await fetch('http://127.0.0.1:5000/config/get',{method: 'GET'});
    const data = await response.json();
    console.log(data)
    return data
}

async function LoginSession(senha,login){
const response = await fetch(`http://127.0.0.1:5000/config/security/${senha}/${login}`,{method: 'POST'});
    const data = await response.json();
    return data
}   
