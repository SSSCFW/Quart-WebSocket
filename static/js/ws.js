var ws = new WebSocket('ws://' + location.host + '/ws');

ws.onmessage = function(event) {
    var data = JSON.parse(event.data);
    if (data.type == "send_message") {
        document.getElementById("text").innerText = data.message;
    }
};

function sendMessage() {
    emit("send_message", {"message": "こんにちは"});
}

function emit(type,data) {
    Object.assign(data, {type: type});
    ws.send(JSON.stringify(data));
}