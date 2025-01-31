document.addEventListener('DOMContentLoaded', function() {
    var viewOrganizationInactiveButton = document.getElementById('view-organization-inactive-button');
    if (viewOrganizationInactiveButton) {
        viewOrganizationInactiveButton.addEventListener('click', function() {
            window.location.href = "/oracle/view_organization_inactive";
        });
    }

    var viewEmployerInactiveButton = document.getElementById('view-employer-inactive-button');
    if (viewEmployerInactiveButton) {
        viewEmployerInactiveButton.addEventListener('click', function() {
            window.location.href = "/oracle/view_employer_inactive";
        });
    }

    var coinTransferButton = document.getElementById('coin-transfer-button');
    if (coinTransferButton) {
        coinTransferButton.addEventListener('click', function() {
            window.location.href = "/oracle_view_organizations/";
        });
    }

    var viewLogFileButton = document.getElementById('view-log-file-button');
    if (viewLogFileButton) {
        viewLogFileButton.addEventListener('click', function() {
            window.location.href = "/oracle/view_log_file/";
        });
    }
});