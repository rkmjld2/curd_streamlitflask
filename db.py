import os
import mysql.connector


def get_connection():

    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    database = os.getenv("DB_NAME")

    missing = []

    if not host:
        missing.append("DB_HOST")

    if not port:
        missing.append("DB_PORT")

    if not user:
        missing.append("DB_USER")

    if not password:
        missing.append("DB_PASSWORD")

    if not database:
        missing.append("DB_NAME")

    if missing:
        raise Exception(
            "Missing environment variable(s): "
            + ", ".join(missing)
        )

    connection = mysql.connector.connect(
        host=host,
        port=int(port),
        user=user,
        password=password,
        database=database,

        # TiDB Cloud SSL
        ssl_verify_cert=False,
        ssl_verify_identity=False
	
    )

    return connection