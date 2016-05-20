from django.conf import settings


_PRIVATE_KEY = None
def get_private_key():
    global _PRIVATE_KEY
    if _PRIVATE_KEY is None:
        with open(settings.JWT_SIGNATURE_KEY_FILE, 'rb') as f:
            _PRIVATE_KEY = f.read()
    return _PRIVATE_KEY


_CERTIFICATE = None
def get_certificate():
    global _CERTIFICATE
    if _CERTIFICATE is None:
        with open(settings.JWT_SIGNATURE_CERT_FILE, 'rb') as f:
            _CERTIFICATE = f.read()
    return _CERTIFICATE
