function addMessage(role, text) {
    const messages = document.getElementById('messages')
    const div = document.createElement('div')
    div.classList.add('message', role)
    div.innerHTML = marked.parse(text)
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
    loadChats()
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
    
    /////////////////////////////// para mudar o nome do chat qnd for a primeira msg
    if (data.is_first_message) {
        loadChats()
    }

    })



async function loadChats() {
    const response = await fetch('/chats')
    const data = await response.json()
    
    const sidebar = document.getElementById('sidebar-list')
    sidebar.innerHTML = ''
    
    data.forEach(conversa => {
        const div = document.createElement('div')
        div.textContent = conversa.title
        div.classList.add('chat-item')

        div.onclick = async () => {
            currentChatId = conversa._id

            const response = await fetch(`/chat/${currentChatId}/history`)
            const data = await response.json()

            const messages = document.getElementById('messages')
            messages.innerHTML = ''

            data.message.forEach(msg => {
                const role = msg.role === 'user' ? 'user' : 'bot'
                addMessage(role, msg.content)
            })
        }

        sidebar.appendChild(div)

    })
}


loadChats()