async function fetchUserInfo() {
    const response = await fetch('/ip/v1/me', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    });

    const result = await response.json();
    const userInfoDiv = document.getElementById('userInfo');

    if (response.status === 200) {
        userInfoDiv.innerHTML = `
            <p><strong>ID:</strong> ${result.id}</p>
            <p><strong>UUID:</strong> ${result.uuid}</p>
            <p><strong>Name:</strong> ${result.name}</p>
            <p><strong>Email:</strong> ${result.email}</p>
            <p><strong>Created At:</strong> ${result.created_at}</p>
            <p><strong>Updated At:</strong> ${result.updated_at}</p>
        `;
    } else {
        console.log(result.message);
        window.location.href = `/`;
    }
}

async function logout() {
    const response = await fetch('/ip/v1/logout', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    });
    
    const result = await response.json();

    if (response.status === 200) {
        window.location.href = '/';
    } else {
        console.log(result.message);
        userInfoDiv.textContent = result.message;
    }
}

document.getElementById('logoutButton').addEventListener('click', logout);

// Call the fetchUserInfo function on page load
window.onload = fetchUserInfo;