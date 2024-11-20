document.getElementById('registerForm').addEventListener('submit', async function(event) {
    event.preventDefault();
    const name = document.getElementById('registerName').value;
    const email = document.getElementById('registerEmail').value;
    const password = document.getElementById('registerPassword').value;
    const password2 = document.getElementById('registerPassword2').value;

    const response = await fetch('/ip/v1/signin', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            name: name,
            email: email,
            password: password,
            password2: password2
        })
    });

    const result = await response.json();
    document.getElementById('registerMessage').textContent = result.message;
    
    if (response.status === 200) {
        uuid = result.user_uuid
        token = result.token
        window.location.href = `/validate?uuid=${encodeURIComponent(uuid)}&token=${encodeURIComponent(token)}`;
    }
});