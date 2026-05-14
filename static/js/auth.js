document.getElementById('btn-login').addEventListener('click', async () => {
    const username = document.getElementById('username').value
    const password = document.getElementById('password').value

    const response = await fetch ('/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json'},
        body: JSON.stringify({'username': username, 'password': password})
    })

    const data = await response.json()

    if (response.ok) {
        window.location.href = '/'
    } else {
        alert(data.message)
    }
})

document.getElementById('btn-register').addEventListener('click', async () => {
    const username = document.getElementById('username').value
    const password = document.getElementById('password').value

    const response = await fetch ('/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json'},
        body: JSON.stringify({'username': username, 'password': password})
    })

    const data = await response.json()

    if (response.ok) {
        window.location.href = '/'
    } else {
        alert(data.message)
    }
})