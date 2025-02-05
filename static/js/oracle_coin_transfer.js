document.addEventListener('DOMContentLoaded', function() {
    var coinTransferButton = document.getElementById('coin-transfer');
    if (coinTransferButton) {
        coinTransferButton.addEventListener('click', function() {
            window.location.href = "/oracle_coin_transfer/";
        });
    }
});