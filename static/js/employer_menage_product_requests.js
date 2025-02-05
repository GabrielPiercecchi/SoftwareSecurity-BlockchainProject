document.addEventListener('DOMContentLoaded', function() {
    var productRequestButton = document.getElementById('product-request-button');
    if (productRequestButton) {
        productRequestButton.addEventListener('click', function() {
            window.location.href = "/employer/menage_product_requests/view_other_products/";
        });
    }
});