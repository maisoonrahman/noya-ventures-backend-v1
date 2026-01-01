from app.models.db import get_db
from werkzeug.security import generate_password_hash, check_password_hash

# Signup new user
def signup_user(data):
    db = get_db()
    cursor = db.cursor(dictionary=True)

    # Check if email exists
    cursor.execute("SELECT id FROM users WHERE email = %s", (data['email'],))
    if cursor.fetchone():
        cursor.close()
        return {"error": "User already exists"}

    # Map frontend roles to internal roles
    role_map = {
        "entrepreneur/startup": "startup",
        "investor/lp": "investor",
        "partner": "partner",
        "mentor/advisor": "partner"
    }
    role_name = role_map.get(data['role'].lower(), "startup")

    # Insert user
    hashed_pw = generate_password_hash(data['password'])
    cursor.execute(
        "INSERT INTO users (email, password, company, country, role_id) "
        "VALUES (%s, %s, %s, %s, "
        "(SELECT id FROM user_roles WHERE role_name=%s))",
        (data['email'], hashed_pw, data['company'], data['country'], role_name)
    )
    db.commit()
    user_id = cursor.lastrowid
    cursor.close()

    return {
        "id": user_id,
        "email": data['email'],
        "company": data['company'],
        "country": data['country'],
        "role": role_name
    }

# Login existing user
def login_user(data):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute(
        "SELECT u.id, u.email, u.name, u.password, u.company, u.country, r.role_name AS role "
        "FROM users u "
        "LEFT JOIN user_roles r ON u.role_id = r.id "
        "WHERE u.email = %s",
        (data['email'],)
    )
    user = cursor.fetchone()
    cursor.close()

    if user and check_password_hash(user['password'], data['password']):
        return {
            "id": user['id'],
            "email": user['email'],
            "name": user['name'],
            "company": user['company'],
            "country": user['country'],
            "role": user['role']
        }
    return None

# Get user by ID
def get_user_by_id(user_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute(
        "SELECT u.id, u.email, u.name, u.company, u.country, r.role_name AS role "
        "FROM users u "
        "LEFT JOIN user_roles r ON u.role_id = r.id "
        "WHERE u.id = %s",
        (user_id,)
    )
    user = cursor.fetchone()
    cursor.close()
    return user

# Optional: list all users (for dev)
def get_all_users():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute(
        "SELECT u.id, u.email, u.name, u.company, u.country, r.role_name AS role "
        "FROM users u LEFT JOIN user_roles r ON u.role_id = r.id"
    )
    users = cursor.fetchall()
    cursor.close()
    return users
