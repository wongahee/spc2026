document.addEventListener('DOMContentLoaded', () => {
    const chatInput = document.getElementById('user-input');
    const formInput = document.getElementById('user-input-form');
    const resultDiv = document.getElementById('result');

    formInput.addEventListener('submit', async (ev) => {
        ev.preventDefault();

        const chatMessage = chatInput.value.trim();
        if (!chatMessage) return;

        const userReply = document.createElement('div');
        userReply.classList.add('message', 'user-message');
        userReply.innerText = chatMessage;
        resultDiv.appendChild(userReply);

        chatInput.value = '';
        resultDiv.scrollTop = resultDiv.scrollHeight;
        
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ chatMessage })
        });

        const data = await response.json();
        console.log(data)

        const chatbotReply = document.createElement('div');
        chatbotReply.classList.add('message', 'bot-message');
        chatbotReply.innerText = data.reply;

        resultDiv.appendChild(chatbotReply);

        resultDiv.scrollTop = resultDiv.scrollHeight;
    })
})