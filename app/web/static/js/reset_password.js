document.getElementById('resetPasswordForm').addEventListener('submit', async function(event) {
    event.preventDefault();
    const token = document.getElementById('token').value;
    const newPassword = document.getElementById('newPassword').value;
    const newPassword2 = document.getElementById('newPassword2').value;

    const response = await fetch('/ip/v1/reset_password', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            token: token,
            new_password: newPassword,
            new_password2: newPassword2
        })
    });

    const result = await response.json();
    document.getElementById('resetPasswordMessage').textContent = result.message;

    if (response.status === 200) {
        window.location.href = '/';
    }
});