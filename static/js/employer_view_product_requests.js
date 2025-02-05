document.addEventListener('DOMContentLoaded', function() {
    var productRequestButtons = document.querySelectorAll('.product-request-button');
    if (productRequestButtons) {
        productRequestButtons.forEach(function(button) {
            button.addEventListener('click', function() {
                var productId = button.getAttribute('data-product-id');
                window.location.href = "/employer/menage_product_requests/view_other_products/create_product_requests/" + productId;
            });
        });
    }
});