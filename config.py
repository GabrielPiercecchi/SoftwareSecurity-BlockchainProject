from datetime import timedelta

class Config:
    # Altre configurazioni...
    PERMANENT_SESSION_LIFETIME = timedelta(hours=1)
    SESSION_COOKIE_HTTPONLY = True  # Impedisce l'accesso ai cookie di sessione tramite JavaScript
    SESSION_COOKIE_SECURE = True  # Richiede HTTPS per i cookie di sessione
    REMEMBER_COOKIE_HTTPONLY = True  # Impedisce l'accesso ai cookie di "remember me" tramite JavaScript
    REMEMBER_COOKIE_SECURE = True  # Richiede HTTPS per i cookie di "remember me"
    SESSION_PROTECTION = 'strong'  # Protezione contro il "session fixation"
    WTF_CSRF_ENABLED = True  # Abilita la protezione CSRF per i moduli Flask-WTF