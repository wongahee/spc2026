// DOM 로딩 이후 호출
document.addEventListener('DOMContentLoaded', () => {
    const chatInput = document.getElementById('user-input');
    const formInput = document.getElementById('user-input-form');
    const resultDiv = document.getElementById('result');

    formInput.addEventListener('submit', async (ev) => {
        ev.preventDefault();

        const chatMessage = chatInput.value;
        // console.log(chatMessage)    // 실무에서 FE는 필수로 디버그 코드 제거

        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ chatMessage })
        });

        const data = await response.json();    // promise
        console.log(data)

        const chatbotReply = document.createElement('p')
        chatbotReply.innerText = data.reply;
        resultDiv.appendChild(chatbotReply);
    })
})