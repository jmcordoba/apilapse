document.getElementById('forgotPasswordForm').addEventListener('submit', async function(event) {
    event.preventDefault();
    const email = document.getElementById('forgotPasswordEmail').value;

    const response = await fetch(`/ip/v1/reset_password?email=${encodeURIComponent(email)}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    });

    const result = await response.json();
    document.getElementById('forgotPasswordMessage').textContent = result.message;
    
    if (response.status === 200) {
        document.getElementById('forgotPasswordMessage').style.color = 'green';
    }
});