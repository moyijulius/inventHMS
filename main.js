document.addEventListener('DOMContentLoaded', function () {
    console.log('JavaScript loaded.'); // Logs when the DOM is ready

    // This defines the confirmDischarge function and attaches it to the global window object
    window.confirmDischarge = function (url) {
        console.log('confirmDischarge function called with URL:', url);
        
        if (confirm('Are you sure you want to discharge this patient?')) {
            // Make a POST request to the provided URL to discharge the patient
            fetch(url, { method: 'POST' })
                .then(response => {
                    if (response.ok) {
                        window.location.reload();  // Refresh the page if successful
                    } else {
                        alert('Failed to discharge patient.');
                    }
                })
                .catch(error => console.error('Error discharging patient:', error));
        }
    };
});
