// Function to get query parameters
function getQueryParams() {
    const params = new URLSearchParams(window.location.search);
    return {
        uuid: params.get('uuid'),
        token: params.get('token')
    };
}

// Automatically validate the token
async function validateToken() {
    const { uuid, token } = getQueryParams();

    if (!uuid || !token) {
        document.getElementById('validateTokenMessage').textContent = 'UUID and token are required';
        return;
    }

    const response = await fetch(`/ip/v1/validate?uuid=${encodeURIComponent(uuid)}&token=${encodeURIComponent(token)}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    });

    const result = await response.json();
    document.getElementById('validateTokenMessage').textContent = result.message;

    if (response.status === 200) {
        window.location.href = '/';
    } else {
        window.location.href = '/signin';
    }
}

// Call the validateToken function on page load
window.onload = validateToken;