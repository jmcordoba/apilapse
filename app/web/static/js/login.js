// Function to get query parameters
function getQueryParams() {
    const params = new URLSearchParams(window.location.search);
    return {
        uuid: params.get('message')
    };
}

// Automatically validate the token
async function getInput() {
    const { message } = getQueryParams();

    if (message) {
        document.getElementById('welcomeMessage').textContent = message;
    }    
}

// Call the validateToken function on page load
window.onload = getInput;

document.getElementById('loginForm').addEventListener('submit', async function(event) {
    event.preventDefault();
    const email = document.getElementById('loginEmail').value;
    const password = document.getElementById('loginPassword').value;

    const response = await fetch('/ip/v1/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: new URLSearchParams({
            email: email,
            password: password
        })
    });

    const result = await response.json();
    document.getElementById('loginMessage').textContent = result.message;

    if (response.status === 200) {
        window.location.href = `/home`;
    }
});