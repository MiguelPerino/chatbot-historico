function addMessage(role, text) {
    const messages = document.getElementById('messages')
    const div = document.createElement('div')
    div.classList.add('message', role)
    div.textContent = text
    messages.appendChild(div)
    messages.scrollTop = messages.scrollHeight
}


let currentChatId = null

document.getElementById('btn-new-chat').addEventListener('click', async () => {
    const response = await fetch('/chat/create', {
        method: 'POST'
    })
    const data = await response.json()
    currentChatId = data.id
    console.log('conversa criada:', currentChatId)
})


// Pegar o texto do input-message
// Verificar se currentChatId não é null
// Chamar POST /chat/<id>/message com o texto
// Printar a resposta no console

document.getElementById('btn-send').addEventListener('click', async () => {
    const message = document.getElementById('input-message').value

    if (!currentChatId) {
        alert('Cria uma conversa primeiro')
        return
    }

    addMessage('user', message)
    document.getElementById('input-message').value = ''

    const response = await fetch (`/chat/${currentChatId}/message`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: message })
    })


    const data = await response.json()
    addMessage('bot', data.response)
    
    })

