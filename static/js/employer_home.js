document.getElementById('create-product-button').addEventListener('click', function() {
    window.location.href = "{{ url_for('create_product_route') }}";
});
document.getElementById('update-product-button').addEventListener('click', function() {
    window.location.href = "{{ url_for('update_product_route') }}";
});
document.getElementById('view-products-button').addEventListener('click', function() {
    window.location.href = "{{ url_for('view_products_route') }}";
});
document.getElementById('create-product-request-button').addEventListener('click', function() {
    window.location.href = "{{ url_for('create_product_request_route') }}";
});
document.getElementById('manage-product-requests-button').addEventListener('click', function() {
    window.location.href = "{{ url_for('manage_product_requests_route') }}";
});
document.getElementById('view-deliveries-button').addEventListener('click', function() {
    window.location.href = "{{ url_for('view_deliveries_route') }}";
});
document.getElementById('create-product-button').addEventListener('click', function() {
    window.location.href = "/create_products";
});