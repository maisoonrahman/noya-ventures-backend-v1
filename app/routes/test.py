import os
import mysql.connector
from flask import Blueprint

test_bp = Blueprint("test", __name__)

@test_bp.route("/db-test")
def db_test():
    conn = mysql.connector.connect(
        host=os.environ["DB_HOST"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        database=os.environ["DB_NAME"],
    )

    cursor = conn.cursor()
    cursor.execute("SELECT DATABASE()")
    db_name = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return {
        "status": "connected",
        "database": db_name
    }
