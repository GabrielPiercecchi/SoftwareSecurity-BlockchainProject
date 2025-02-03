# Esempio base di configurazione per Gunicorn
bind = "0.0.0.0:5000"
workers = 4

def on_starting(server):
    from app import initialize_database
    print("Inizializzo il database prima di avviare Gunicorn...")
    initialize_database()
