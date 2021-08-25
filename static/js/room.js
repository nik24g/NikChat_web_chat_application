const roomName = JSON.parse(document.getElementById('room-name').textContent);
const chatSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/chat/'
    + roomName
    + '/'
);
function updateScroll() {
    var element = document.getElementById("chat-log");
    element.scrollTop = element.scrollHeight;
}
var block_to_insert;
var container_block;

var user = "{{request.user.first_name}} {{request.user.last_name}} : ";
chatSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    const sms = data.message;

    block_to_insert = document.createElement('div');
    if (sms == check) {
        block_to_insert.className = 'right';
        block_to_insert.innerHTML = sms.split(":")[1];
    }
    else {
        block_to_insert.className = 'left';
        block_to_insert.innerHTML = sms
    }

    // document.querySelector('#chat-log').value += (data.message + '\n');

    container_block = document.getElementById('chat-log');
    container_block.appendChild(block_to_insert);
    updateScroll();
    // document.getElementById("chat-log").innerHTML += sms;
};

chatSocket.onclose = function (e) {
    console.error('Chat socket closed unexpectedly');
};

document.querySelector('#chat-message-input').focus();
document.querySelector('#chat-message-input').onkeyup = function (e) {
    if (e.keyCode === 13) {  // enter, return
        document.querySelector('#chat-message-submit').click();
    }
};
var check;
document.querySelector('#chat-message-submit').onclick = function (e) {
    const messageInputDom = document.querySelector('#chat-message-input');
    const message = user + messageInputDom.value;
    check = message;
    chatSocket.send(JSON.stringify({
        'message': message
    }));
    messageInputDom.value = '';
};