document.addEventListener('DOMContentLoaded', function() {
    var productRequestButton = document.getElementById('product-request-button');
    if (productRequestButton) {
        productRequestButton.addEventListener('click', function() {
            var productId = productRequestButton.getAttribute('data-product-id');
            window.location.href = "/employer/menage_product_requests/view_other_products/create_product_requests/" + productId;
        });
    }
});