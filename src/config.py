
import os


DB_PASSWORD = os.getenv("DB_PASSWORD")

if not DB_PASSWORD:
    raise RuntimeError(
        "DB_PASSWORD is missing. Check your environment variables."
    )


DB_SETTINGS = {
    "host": os.getenv("DB_HOST", "postgres"),
    "database": os.getenv("DB_NAME", "devdb"),
    "user": os.getenv("DB_USER", "admin"),
    "password": DB_PASSWORD,
    "port": os.getenv("DB_PORT", "5432")
}
