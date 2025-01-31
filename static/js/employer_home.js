document.addEventListener('DOMContentLoaded', function() {
    var updatePersonalDataButton = document.getElementById('update-personal-data-button');
    if (updatePersonalDataButton) {
        updatePersonalDataButton.addEventListener('click', function() {
            window.location.href = "/employer/employer_update_personal_data";
        });
    }

    var carrierManageProductRequestsButton = document.getElementById('carrier-manage-product-requests-button');
    if (carrierManageProductRequestsButton) {
        carrierManageProductRequestsButton.addEventListener('click', function() {
            window.location.href = "/employer/carrier_menage_product_requests";
        });
    }

    var carrierViewDeliveriesButton = document.getElementById('carrier-view-deliveries-button');
    if (carrierViewDeliveriesButton) {
        carrierViewDeliveriesButton.addEventListener('click', function() {
            window.location.href = "/employer/carrier_view_deliveries/";
        });
    }

    var viewProductsButton = document.getElementById('view-products-button');
    if (viewProductsButton) {
        viewProductsButton.addEventListener('click', function() {
            window.location.href = "/employer/view_products/";
        });
    }

    var manageProductRequestsButton = document.getElementById('manage-product-requests-button');
    if (manageProductRequestsButton) {
        manageProductRequestsButton.addEventListener('click', function() {
            window.location.href = "/employer/menage_product_requests";
        });
    }

    var viewDeliveriesButton = document.getElementById('view-deliveries-button');
    if (viewDeliveriesButton) {
        viewDeliveriesButton.addEventListener('click', function() {
            window.location.href = "/employer/view_deliveries/";
        });
    }

    var viewCoinRequestsButton = document.getElementById('view-coin-requests-button');
    if (viewCoinRequestsButton) {
        viewCoinRequestsButton.addEventListener('click', function() {
            window.location.href = "/employer/view_coin_requests/";
        });
    }

    var viewCoinTransactionsButton = document.getElementById('view-transactions-button');
    if (viewCoinTransactionsButton) {
        viewCoinTransactionsButton.addEventListener('click', function() {
            window.location.href = "/employer/view_transactions/";
        });
    }

});