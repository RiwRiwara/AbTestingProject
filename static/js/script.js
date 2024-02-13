window.addEventListener('load', function () {
    document.body.classList.add('loaded');
});



function handleButtonClick(page, button) {
    const data = {
        page: page,
        button: button
    };

    fetch('api/save-click-action', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (response.ok) {
            alert(button+' action has been saved.');
        } else {
            alert('Failed to '+button+'buy action.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred. Please try again later.');
    });
}
