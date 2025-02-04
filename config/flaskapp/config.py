import os
from datetime import timedelta

class Config:
    # Carica la chiave segreta dall'ambiente
    SECRET_KEY = os.getenv('SECRET_KEY')
    
    # Durata della sessione permanente
    PERMANENT_SESSION_LIFETIME = timedelta(hours=1)
    # Impedisce l'accesso ai cookie di sessione tramite JavaScript
    SESSION_COOKIE_HTTPONLY = True

    # Richiede HTTPS per i cookie di sessione (impostare a True in produzione)
    SESSION_COOKIE_SECURE = True

    # Impedisce l'accesso ai cookie di "remember me" tramite JavaScript
    REMEMBER_COOKIE_HTTPONLY = True

    # Richiede HTTPS per i cookie di "remember me" (impostare a True in produzione)
    REMEMBER_COOKIE_SECURE = True

    # Protezione contro il "session fixation"
    SESSION_PROTECTION = 'strong'
    # Protezione contro gli attacchi CSRF
    SESSION_COOKIE_SAMESITE = 'Lax'
    # Abilita la protezione CSRF per i moduli Flask-WTF
    WTF_CSRF_ENABLED = True

    # Configurazione di Talisman
    # Politica di sicurezza del contenuto (None per disabilitare)
    TALISMAN_CONTENT_SECURITY_POLICY = None
    # Forza l'uso di HTTPS se True (impostare a True in produzione)
    TALISMAN_FORCE_HTTPS = False 
    # IMPORTANTE: Siccome la nostra applicazione è in esecuzione in localhost non possiamo forzare l'uso di HTTPS

    # Configurazione del proxy per il reverse proxy Heroku
    # Numero di livelli di proxy da considerare per l'header X-Forwarded-For
    PROXY_FIX_X_FOR = 1
    # Numero di livelli di proxy da considerare per l'header X-Forwarded-Proto
    PROXY_FIX_X_PROTO = 1
    # Numero di livelli di proxy da considerare per l'header X-Forwarded-Host
    PROXY_FIX_X_HOST = 1
    # Numero di livelli di proxy da considerare per l'header X-Forwarded-Port
    PROXY_FIX_X_PORT = 1
    # Numero di livelli di proxy da considerare per l'header X-Forwarded-Prefix
    PROXY_FIX_X_PREFIX = 1