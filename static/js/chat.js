function addMessage(role, text) {
    const messages = document.getElementById('messages')
    const div = document.createElement('div')
    div.classList.add('message', role)

    if (role === 'bot') {
        const name = document.createElement('span')
        name.textContent = 'MiguelBot'
        name.style.display = 'block'
        name.style.fontSize = '11px'
        name.style.color = '#888'
        name.style.marginBottom = '4px'
        div.appendChild(name)
    }

    const content = document.createElement('div')
    content.innerHTML = marked.parse(text)
    div.appendChild(content)

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

    if (!message.trim()) return

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

document.getElementById('input-message').addEventListener('keydown', (e) => {

    if (e.key === 'Enter') {
        const btn = document.getElementById('btn-send')
        btn.classList.add('clicking')
        setTimeout(() => btn.classList.remove('clicking'), (150));
        btn.click()
    }
})


document.getElementById('btn-logout').addEventListener('click', async () => {
    await fetch('/logout', { method: 'POST' })
    window.location.href = '/login'
})

async function loadChats() {
    const response = await fetch('/chats')

    if (response.redirected || !response.ok) {
        window.location.href = '/login'
        return
    }

    const data = await response.json()
    
    const sidebar = document.getElementById('sidebar-list')
    sidebar.innerHTML = ''
    
    data.forEach(conversa => {
        const div = document.createElement('div')
        div.classList.add('chat-item')

        const title = document.createElement('span')
        title.textContent = conversa.title
        title.style.overflow = 'hidden'
        title.style.textOverflow = 'ellipsis'
        title.style.whiteSpace = 'nowrap'
        div.appendChild(title)

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
        const btn = document.createElement('button')
        btn.textContent = '✕'
        btn.classList.add('btn-delete')
        btn.onclick = async (e) => {
            e.stopPropagation()  // impede de abrir a conversa ao deletar
            await fetch(`/delete/${conversa._id}`, { method: 'DELETE' })
            loadChats()
        }
        div.appendChild(btn)        

        sidebar.appendChild(div)

    })
}

loadChats()