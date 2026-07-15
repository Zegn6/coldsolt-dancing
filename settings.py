# ── Production settings ────────────────────────
import os

# Static files for production
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Override settings from environment variables if set
_secret = os.environ.get('DJANGO_SECRET_KEY')
if _secret:
    SECRET_KEY = _secret

_debug = os.environ.get('DJANGO_DEBUG')
if _debug is not None:
    DEBUG = _debug == 'True'

_hosts = os.environ.get('DJANGO_ALLOWED_HOSTS')
if _hosts:
    ALLOWED_HOSTS = _hosts.split()