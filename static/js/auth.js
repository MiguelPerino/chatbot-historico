let mode = 'login'

function switchTab(tab) {
    mode = tab
    document.getElementById('tab-login').classList.toggle('active', tab === 'login')
    document.getElementById('tab-register').classList.toggle('active', tab === 'register')
    document.getElementById('btn-submit').textContent = tab === 'login' ? 'Entrar' : 'Criar conta'
    document.getElementById('msg').className = 'message'
}

function showMsg(text, type) {
    const el = document.getElementById('msg')
    el.textContent = text
    el.className = `message ${type}`
}

document.getElementById('btn-submit').addEventListener('click', async () => {
    const username = document.getElementById('username').value.trim()
    const password = document.getElementById('password').value
    const btn = document.getElementById('btn-submit')

    if (!username || !password) {
        showMsg('Preencha todos os campos.', 'error')
        return
    }

    btn.disabled = true
    btn.textContent = mode === 'login' ? 'Entrando...' : 'Criando conta...'

    const url = mode === 'login' ? '/login' : '/register'
    const response = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
    })

    const data = await response.json()
    btn.disabled = false
    btn.textContent = mode === 'login' ? 'Entrar' : 'Criar conta'

    if (response.ok) {
        if (mode === 'login') {
            window.location.href = '/'
        } else {
            showMsg('Conta criada! Faça login para continuar.', 'success')
            switchTab('login')
        }
    } else {
        showMsg(data.message || 'Erro ao processar.', 'error')
    }
})

document.getElementById('password').addEventListener('keydown', e => {
    if (e.key === 'Enter') document.getElementById('btn-submit').click()
})
