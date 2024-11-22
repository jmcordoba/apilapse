// Function to get query parameters
function getQueryParam(param) {
    const params = new URLSearchParams(window.location.search);
    return params.get(param);
}

document.getElementById('resetPasswordForm').addEventListener('submit', async function(event) {
    event.preventDefault();

    const token = getQueryParam('token');
    if (!token) {
        console.log('Token is not defined.');
    }

    const email = getQueryParam('email');
    if (!email) {
        console.log('Email is not defined.');
    }

    //const token = document.getElementById('token').value;
    const newPassword = document.getElementById('newPassword').value;
    const newPassword2 = document.getElementById('newPassword2').value;

    const response = await fetch('/ip/v1/reset_password', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            token: token,
            email: email,
            new_password: newPassword,
            new_password2: newPassword2
        })
    });

    const result = await response.json();

    if (response.status === 200) {

        document.getElementById('resetPasswordMessage').textContent = result.message;
        document.getElementById('resetPasswordMessage').style.color = 'green';
        
        // Add a delay of 3 seconds before redirecting
        setTimeout(() => {
            window.location.href = '/login?message=Password reset successfully. Please login to continue.';    
        }, 3000);
    }
});