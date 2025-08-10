document.addEventListener('DOMContentLoaded', function() {
    const SignUpButton = document.getElementById('SignUpButton');
    const SignUpButton = document.getElementById('SignInButton');
    const responseArea = document.getElementById('responseArea');

    sendButton.addEventListener('click', function() {
        const data = {
            name: nameInput.value.trim()
        };

        // Отправка данных на сервер
        fetch('/process', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(data => {
            // Обработка ответа от сервера
            responseArea.innerHTML = `
                <p><strong>Сообщение:</strong> ${data.message}</p>
                <p><strong>Полученные данные:</strong> ${JSON.stringify(data.received_data)}</p>
            `;
        })
        .catch(error => {
            console.error('Ошибка:', error);
            responseArea.textContent = 'Произошла ошибка при отправке данных';
        });
    });
});