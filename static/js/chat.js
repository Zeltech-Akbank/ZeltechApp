$(document).ready(function() {
    var socket = io.connect('http://' + document.domain + ':' + location.port);

    $('#sendButton').on('click', function() {
        sendMessage();
    });

    $('#input').on('keydown', function(event) {
        if (event.which == 13) {
            sendMessage();
        }
    });

    function sendMessage() {
        let message = $('#input').val();
        if (message) {
            socket.emit('user_message', message);
            appendMessage(message, "user");
            $('#input').val('');
        }
    }

    socket.on('bot_response', function(data) {
        appendMessage(data, "bot");
    });

    function appendMessage(message, type) {
        let messageClass = (type == "user") ? "user-message" : "bot-message";
        let messageHTML = `<li><div class="${messageClass}">${message}</div></li>`;
        $('#messages').append(messageHTML);
        $("#messages").scrollTop($("#messages")[0].scrollHeight);
    }
});
