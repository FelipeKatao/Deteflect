
var Isprimeiro = true
var Loading = false
document.getElementById("send").addEventListener("click", function() {
    if(Loading == true){
        return
    }
    if(Isprimeiro){
        document.getElementById("welcome").classList.add("bye")
        let a = setInterval(() => {
            document.getElementById("welcome").remove()
            ConstruirMensagem()
            clearInterval(a)
        }, 1000);
        Isprimeiro = false
    }
    else{
        ConstruirMensagem()
    }

});


document.getElementById("input").addEventListener("keyup", function(event) {
    if (event.key === "Enter") {
        event.preventDefault();
        document.getElementById("send").click();
    }
});

function ConstruirMensagem(){
    if(Loading == true){
        return
    }
    Loading = true
    const input = document.getElementById("input").value;
    document.getElementById("input").enabled = false
    const msg = document.createElement("div");
    msg.classList.add("msg_sender");
    msg.textContent = input;
    document.getElementById("msg_input").appendChild(msg);
    document.getElementById("input").value = "";
    var e = setInterval(() => {
        ConstruirMensagemResposta()
        clearInterval(e)
    },1000)
}

function ConstruirMensagemResposta(){
    const input = "Testes de mensagem"
    const msg = document.createElement("div");
    msg.classList.add("msg_receiver");
    msg.textContent = input;
    document.getElementById("msg_input").appendChild(msg);
    document.getElementById("input").value = "";
    Loading = false 
}