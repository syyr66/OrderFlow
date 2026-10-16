from .base import *

DEBUG = True

ALLOWED_HOSTS = [h.strip() for h in env("ALLOWED_HOSTS", "").split(",") if h.strip()] \
    or ["127.0.0.1", "localhost"]