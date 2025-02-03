document.addEventListener('DOMContentLoaded', function() {
    // Seleziona tutti i pulsanti di tipo submit nella pagina
    const submitButtons = document.querySelectorAll('button[type="submit"]');

    // Verifica se ci sono pulsanti di tipo submit nella pagina
    if (submitButtons.length > 0) {
        // Aggiungi un event listener a ciascun pulsante di tipo submit
        submitButtons.forEach(button => {
            button.addEventListener('click', function(event) {
                // Disabilita l'interazione con la pagina
                disablePageInteraction();

                // Simula un compito asincrono (ad esempio, una richiesta AJAX)
                setTimeout(() => {
                    // Riabilita l'interazione con la pagina dopo il compito
                    enablePageInteraction();
                }, 10000); // Simula un compito che richiede 10 secondi
            });
        });
    }

    function disablePageInteraction() {
        // Aggiungi una classe CSS per disabilitare l'interazione
        document.body.classList.add('no-interaction');
    }

    function enablePageInteraction() {
        // Rimuovi la classe CSS per riabilitare l'interazione
        document.body.classList.remove('no-interaction');
    }
});