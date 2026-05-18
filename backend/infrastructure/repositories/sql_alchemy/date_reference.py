from datetime import datetime, timezone

"""Cada vez que creamos una fecha y hora para create_at o last_edited_at, usamos esta función para asegurarnos de que esté en UTC"""
def get_utc_now():
    return datetime.now(timezone.utc)