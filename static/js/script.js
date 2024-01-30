window.addEventListener('load', function () {
    document.body.classList.add('loaded');
});



function handleButtonClick(page) {
    const data = {
        page: page
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
            // Show an alert if the click action was successfully saved
            alert('Buy action has been saved.');
        } else {
            // Show an alert if there was an error saving the click action
            alert('Failed to save buy action.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred. Please try again later.');
    });
}
