document.addEventListener('DOMContentLoaded', function() {
    const flashMessagesElement = document.getElementById('flash-messages');
    if (flashMessagesElement) {
        const messages = JSON.parse(flashMessagesElement.textContent);
        messages.forEach(function(message) {
            alert(message);
        });
    }

    const manageOrganizationRegistrationButton = document.getElementById('manage-organization-registration-button');
    if (manageOrganizationRegistrationButton) {
        manageOrganizationRegistrationButton.addEventListener('click', function() {
            window.location.href = "/manage_organization_registration/{{ organization.id }}";
        });
    }
});