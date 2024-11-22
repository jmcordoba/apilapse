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

    document.getElementById('validateTokenMessage').style.color = 'green';
    document.getElementById('validateTokenMessage').textContent = 'Validating your account...';

    const response = await fetch(`/ip/v1/validate?uuid=${encodeURIComponent(uuid)}&token=${encodeURIComponent(token)}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    });

    if (response.status === 200) {
        
        // Add a delay of 3 seconds before redirecting
        setTimeout(() => {
            window.location.href = '/login?message=Your account has been activated successfully. Please login to continue.';
        }, 3000);

    } else {

        const result = await response.json();
        
        document.getElementById('validateTokenMessage').textContent = result.message;
        document.getElementById('validateTokenMessage').style.color = 'red';
        
        // Add a delay of 3 seconds before redirecting
        setTimeout(() => {
            window.location.href = '/signin';
        }, 3000);
    }
}

// Call the validateToken function on page load
window.onload = validateToken;