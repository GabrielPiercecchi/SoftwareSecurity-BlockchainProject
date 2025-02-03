document.addEventListener('DOMContentLoaded', function() {
    var flashMessagesElement = document.getElementById('flash-messages');
    if (flashMessagesElement) {
        const messages = JSON.parse(flashMessagesElement.textContent);
        messages.forEach(function(message) {
            alert(message);
        });
    }

    var manageEmployerRegistrationButton = document.getElementById('manage-employer-registration-button');
    if (manageEmployerRegistrationButton) {
        manageEmployerRegistrationButton.addEventListener('click', function() {
            window.location.href = "/manage_employer_registration/{{ employer.id }}";
        });
    }
});