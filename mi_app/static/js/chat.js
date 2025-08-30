$(function(){
    console.log(sala_id);

    var url = 'ws://' + window.location.host + '/ws/sala/' + sala_id + '/';
    console.log(url);

    var chatSocket = new WebSocket(url);
    let autoScroll = true;

    chatSocket.onopen = function(e){
        console.log('WEBSOCKET ABIERTO - Conexión establecida');
    };

    chatSocket.onclose = function(e){
        console.log('WEBSOCKET CERRADO - Conexión perdida');
    };

    chatSocket.onmessage = function(data){
        const datamsj = JSON.parse(data.data)
        var msj = datamsj.message
        var usuario = datamsj.usuario
        
        loadMessageHTML(msj, usuario);

        if (autoScroll) {
            setTimeout(() => {
                const chatMessages = document.querySelector('#chat-messages');
                chatMessages.scrollTop = chatMessages.scrollHeight;
            }, 100);
        }
    }

    // Detectar cuando el usuario hace scroll
    document.querySelector('#chat-messages').addEventListener('scroll', function() {
        const chatMessages = this;
        const isAtBottom = chatMessages.scrollHeight - chatMessages.scrollTop - chatMessages.clientHeight < 50;
        autoScroll = isAtBottom;
    });

    document.querySelector('#btnMessage').addEventListener('click', sendMessage);
    document.querySelector('#message').addEventListener('keypress', function(e){
        if(e.keyCode == 13){
            sendMessage();
        }
    });

    function sendMessage(){
        var messageInput = document.querySelector('#message');
        var messageText = messageInput.value.trim();
        
        if (messageText !== '' && typeof CURRENT_USER !== 'undefined'){
            chatSocket.send(JSON.stringify({
                'message': messageText,
                'usuario': CURRENT_USER
            }))
            messageInput.value = '';
            autoScroll = true; // Volver a scroll automático al enviar
        }
    }

    function loadMessageHTML(message, usuario){
        const chatMessages = document.querySelector('#chat-messages');
        const esUsuarioActual = (usuario === CURRENT_USER);
        const messageClass = esUsuarioActual ? "ts-message-sent" : "ts-message-received";
        const timestamp = new Date().toLocaleTimeString('es-ES', { 
            hour: '2-digit', 
            minute: '2-digit',
            hour12: true  // Para formato 24 horas (opcional)
        });
        
        let messageHTML = '';
        if (!esUsuarioActual) {
            messageHTML = `<div class="${messageClass}"><strong>${usuario}:</strong> ${message} <span class="message-time">${timestamp}</span></div>`;
        } else {
            messageHTML = `<div class="${messageClass}">${message} <span class="message-time">${timestamp}</span></div>`;
        }

        chatMessages.innerHTML += messageHTML;
    }

    // Scroll al final al cargar
    setTimeout(() => {
        const chatMessages = document.querySelector('#chat-messages');
        if (chatMessages) {
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }
    }, 500);
});