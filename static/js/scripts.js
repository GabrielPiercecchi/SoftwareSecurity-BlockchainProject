document.addEventListener('DOMContentLoaded', function() {
    // Seleziona tutti i moduli nella pagina
    const forms = document.querySelectorAll('form');

    // Aggiungi un event listener a ciascun modulo
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {

            // Disabilita tutti i pulsanti
            disableButtons();

            // Aggiungi un overlay per disabilitare l'interazione con la pagina
            disablePageInteraction();
        });
    });

    function disableButtons() {
        // Disabilita tutti i pulsanti
        const buttons = document.querySelectorAll('button');
        buttons.forEach(button => {
            button.disabled = true;
        });
    }

    function disablePageInteraction() {
        // Aggiungi un overlay trasparente per disabilitare l'interazione con la pagina
        const overlay = document.createElement('div');
        overlay.id = 'interaction-overlay';
        overlay.style.position = 'fixed';
        overlay.style.top = 0;
        overlay.style.left = 0;
        overlay.style.width = '100%';
        overlay.style.height = '100%';
        overlay.style.backgroundColor = 'rgba(255, 255, 255, 0.7)';
        overlay.style.zIndex = 9999;
        document.body.appendChild(overlay);
    }
});