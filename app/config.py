import os

APP_NAME = "Libreya Gestión"
APP_VERSION = "1.0.0"

SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "libreya-desarrollo-cambiar-en-produccion"
)

COOKIE_SECURE = os.getenv(
    "COOKIE_SECURE",
    "false"
).lower() == "true"
