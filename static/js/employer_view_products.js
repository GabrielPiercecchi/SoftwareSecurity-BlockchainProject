document.addEventListener('DOMContentLoaded', function() {
    var createProductButton = document.getElementById('create-product-button');
    if (createProductButton) {
        createProductButton.addEventListener('click', function() {
            window.location.href = "/employer/create_products";
        });
    }
});