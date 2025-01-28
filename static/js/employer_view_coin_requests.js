document.addEventListener('DOMContentLoaded', function() {

    var createCoinRequestButton = document.getElementById('create-coin-request-button');
    if (createCoinRequestButton) {
        createCoinRequestButton.addEventListener('click', function() {
            window.location.href = "/employer/view_coin_requests/create_coin_request/";
        });
    }

    var viewAcceptedCoinRequestButton = document.getElementById('view-accepted-coin-request-button');
    if (viewAcceptedCoinRequestButton) {
        viewAcceptedCoinRequestButton.addEventListener('click', function() {
            window.location.href = "/employer/view_coin_requests/view_accepted_coin_requests/";
        });
    }
});
