var ws = new WebSocket('ws://' + location.host + '/ws');

ws.onmessage = function(event) {
    var data = JSON.parse(event.data);
    if (data.type == "send_message") {
        document.getElementById("text").innerText += data.message;
    }
};

function sendMessage() {
    var message = document.getElementById("messageInput").value;
    emit("send_message", {"message": message+"\n"});
    document.getElementById("messageInput").value = "";
}

function emit(type,data) {
    Object.assign(data, {type: type});
    ws.send(JSON.stringify(data));
}