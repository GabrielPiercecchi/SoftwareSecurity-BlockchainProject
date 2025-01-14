document.addEventListener('DOMContentLoaded', function() {
    const flashMessagesElement = document.getElementById('flash-messages');
    if (flashMessagesElement) {
        const messages = JSON.parse(flashMessagesElement.textContent);
        if (messages.length > 0) {
            alert(messages.join('\n'));
            window.location.href = flashMessagesElement.dataset.redirectUrl;
        }
    }

    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function(event) {
            event.preventDefault();
            const action = form.action;
            fetch(action, {
                method: 'POST',
                body: new FormData(form)
            }).then(response => response.json())
              .then(data => {
                  if (data.message) {
                      alert(data.message);
                      window.location.href = data.redirect_url;
                  }
              });
        });
    });
});