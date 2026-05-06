var modal = document.getElementById("loginModal");
var loginBtn = document.getElementById("loginBtn");
var closeBtn = document.getElementById("closeModal");
var usernameInput = document.getElementById("username");
var passwordInput = document.getElementById("password");

// Show modal on page load
window.onload = async function() {
    console.log(ReadSecury())
    const result = await ReadSecury()
    if (result == 1){
        modal.style.display = "block";
    }
};

loginBtn.addEventListener("click", function() {
    var username = usernameInput.value;
    var password = passwordInput.value;
    
    if (username === "" || password === "") {
        alert("Por favor, preencha todos os campos!");
        return;
    }
    
    modal.style.display = "none";
    
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


async function ReadSecury(){
const response = await fetch('http://127.0.0.1:5000/secury/check',{method: 'POST'});
    const data = await response.json();
    console.log(data["Response"])
    return data["Response"]
}