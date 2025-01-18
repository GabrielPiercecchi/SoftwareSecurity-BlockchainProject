document.addEventListener('DOMContentLoaded', function() {
    const flashMessagesElement = document.getElementById('flash-messages');
    if (flashMessagesElement) {
        const messages = JSON.parse(flashMessagesElement.textContent);
        messages.forEach(function(message) {
            alert(message);
        });
    }
});
document.getElementById('manage-employer-registration-button').addEventListener('click', function() {
    window.location.href = "/manage_employer_registration/{{ employer.id }}";
});