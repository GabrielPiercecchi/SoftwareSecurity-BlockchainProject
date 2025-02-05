document.addEventListener('DOMContentLoaded', function() {
    var productLinks = document.querySelectorAll('.product-link');
    if (productLinks) {
        productLinks.forEach(function(link) {
            link.addEventListener('click', function() {
                var productId = link.getAttribute('data-product-id');
                window.location.href = "/product/" + productId;
            });
        });
    }
});