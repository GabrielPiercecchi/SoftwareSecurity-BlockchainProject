document.addEventListener('DOMContentLoaded', function() {
    const flashMessagesElement = document.getElementById('flash-messages');
    if (flashMessagesElement) {
        const messages = JSON.parse(flashMessagesElement.textContent);
        messages.forEach(function(message) {
            alert(message);
        });
    }
});

document.getElementById('manage-organization-registration-button').addEventListener('click', function() {
    window.location.href = "/manage_organization_registration/{{ organization.id }}";
});