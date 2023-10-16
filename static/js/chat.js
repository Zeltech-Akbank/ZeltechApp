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

    function convertLinks(message) {
    var urlRegex = /(https?:\/\/[^\s)]+|www\.[^\s)]+|[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}(\/[^\s)]*)?)/g;

    return message.replace(urlRegex, function(url) {
        var prefixedUrl = url.match(/^https?:\/\//) ? url : 'http://' + url;
        return '<a href="' + prefixedUrl + '" target="_blank">' + url + '</a>';
    });
    }


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
        // Mesaj içindeki URL'leri tıklanabilir bağlantılara dönüştür
        let convertedMessage = convertLinks(message);
        let messageHTML = `<li><div class="${messageClass}">${convertedMessage}</div></li>`;
        $('#messages').append(messageHTML);
        $("#messages").scrollTop($("#messages")[0].scrollHeight);
    }
});
