// DOM 로딩 이후 호출
document.addEventListener('DOMContentLoaded', () => {
    const chatInput = document.getElementById('user-input');
    const formInput = document.getElementById('user-input-form');
    const resultDiv = document.getElementById('result');

    formInput.addEventListener('submit', async (ev) => {
        ev.preventDefault();

        const chatMessage = chatInput.value.trim();
        if (!chatMessage) return; //
        // console.log(chatMessage)    // 실무에서 FE는 필수로 디버그 코드 제거

         // 사용자 메시지 화면에 추가 (오른쪽 말풍선)
        const userReply = document.createElement('div');
        userReply.classList.add('message', 'user-message');
        userReply.innerText = chatMessage;
        resultDiv.appendChild(userReply);

        // 입력창 비우기 및 스크롤 하단 이동
        chatInput.value = '';
        resultDiv.scrollTop = resultDiv.scrollHeight;
        
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ chatMessage })
        });

        const data = await response.json();    // promise
        console.log(data)

        const chatbotReply = document.createElement('div');
        chatbotReply.classList.add('message', 'bot-message');
        chatbotReply.innerText = data.reply;
        resultDiv.appendChild(chatbotReply);

        
    })
})
