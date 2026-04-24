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

