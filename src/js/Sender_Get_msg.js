
var Isprimeiro = true
var Loading = false
var msgUser = ""
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
    msgUser = input 
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
    ReadAPI(msgUser).then(inputData =>{
        const input = inputData
        const msg = document.createElement("div");
        msg.classList.add("msg_receiver");
        msg.innerHTML = input;
        document.getElementById("msg_input").appendChild(msg);
        document.getElementById("input").value = "";
        Loading = false 
    })
}



async function ReadAPI(msg){
const response = await fetch('http://127.0.0.1:5000/sendmensage/API/' + msg);
    const data = await response.json();
    return data["Response"]
}