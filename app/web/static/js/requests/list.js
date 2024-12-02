async function fetchRequests() {
    const response = await fetch('/requests/v1/all', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    });

    const result = await response.json();

    const requestsInfoDiv = document.getElementById('requestsInfo');

    if (response.status === 200) {
        requestsInfoDiv.innerHTML = `
            <p><strong>ID:</strong> ${result.message}</p>
        `;
        
        /*
        result.data.forEach(request => {

            requestsListDiv.innerHTML = `<div>`;

            Object.values(request).forEach(value => {
                requestsListDiv.innerHTML = `<p>`+value+`</p>`;
                console.log(value);
            });

            requestsListDiv.innerHTML = `</div>`;
        });
        */

        const requestsListDiv = document.getElementById('requestsList');
        result.data.forEach(request => {
            const requestDiv = document.createElement('div');
            requestDiv.classList.add('request');

            Object.entries(request).forEach(([key, value]) => {
                const div = document.createElement('div');
                div.innerHTML = `<strong>${key}:</strong> ${value}, `;
                requestDiv.appendChild(div);
            });

            requestsListDiv.appendChild(requestDiv);
        });

    } else {
        console.log(result.message);
        //window.location.href = `/`;
    }
}

//document.getElementById('logoutButton').addEventListener('click', logout);

// 
window.onload = fetchRequests;