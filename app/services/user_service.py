from app.models.db import get_db
from werkzeug.security import generate_password_hash, check_password_hash

# -----------------------
# Signup new user
# -----------------------
def signup_user(data):
    db = get_db()
    cursor = db.cursor(dictionary=True)

    # 1. Check if email exists
    cursor.execute(
        "SELECT id FROM users WHERE email = %s",
        (data['email'],)
    )
    if cursor.fetchone():
        cursor.close()
        return {"error": "User already exists"}

    # 2. Map frontend roles to internal roles
    role_map = {
        "entrepreneur": "founder",
        "startup": "founder",
        "founder": "startup",
        "investor/lp": "investor",
        "investor": "investor",
        "partner": "partner",
        "mentor/advisor": "partner"
    }

    role = role_map.get(data['role'].lower())
    if not role:
        cursor.close()
        return {"error": "Invalid role"}

    # 3. Resolve country name -> country code
    normalized_country = normalize_country_name(data['country'])

    cursor.execute(
    """
    SELECT countrycode, countryname
    FROM countries
    WHERE LOWER(countryname) = LOWER(%s)
       OR LOWER(countryname) LIKE LOWER(%s)
    LIMIT 1
    """,
    (
        normalized_country,
        f"%{normalized_country}%"
    )
)

    country_row = cursor.fetchone()
    if not country_row:
        cursor.close()
        return {"error": f"Invalid country: {data['country']}"}

    countrycode = country_row['countrycode']


    # 4. Insert user
    password_hash = generate_password_hash(data['password'])

    cursor.execute(
        """
        INSERT INTO users (email, password_hash, role, countrycode)
        VALUES (%s, %s, %s, %s)
        """,
        (data['email'], password_hash, role, countrycode)
    )

    db.commit()
    user_id = cursor.lastrowid
    cursor.close()

    return {
        "id": user_id,
        "email": data['email'],
        "role": role,
        "country": data['country'],
        "countrycode": countrycode
    }


# -----------------------
# Login existing user
# -----------------------
def login_user(data):
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT
            u.id,
            u.email,
            u.password_hash,
            u.role,
            c.countryname
        FROM users u
        LEFT JOIN countries c ON u.countrycode = c.countrycode
        WHERE u.email = %s
        """,
        (data['email'],)
    )

    user = cursor.fetchone()
    cursor.close()

    if user and check_password_hash(user['password_hash'], data['password']):
        return {
            "id": user['id'],
            "email": user['email'],
            "role": user['role'],
            "country": user['countryname']
        }

    return None


# -----------------------
# Get user by ID
# -----------------------
def get_user_by_id(user_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT
            u.id,
            u.email,
            u.role,
            c.countryname
        FROM users u
        LEFT JOIN countries c ON u.countrycode = c.countrycode
        WHERE u.id = %s
        """,
        (user_id,)
    )

    user = cursor.fetchone()
    cursor.close()
    return user


# -----------------------
# List all users (dev only)
# -----------------------
def get_all_users():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT
            u.id,
            u.email,
            u.role,
            c.countryname
        FROM users u
        LEFT JOIN countries c ON u.countrycode = c.countrycode
        """
    )

    users = cursor.fetchall()
    cursor.close()
    return users

def normalize_country_name(raw_country: str) -> str:
    country_map = {
        # United States
        "usa": "United States",
        "us": "United States",
        "u.s.": "United States",
        "united states": "United States",
        "united states of america": "United States",

        # United Kingdom
        "uk": "United Kingdom",
        "u.k.": "United Kingdom",
        "britain": "United Kingdom",
        "great britain": "United Kingdom",
        "england": "United Kingdom",
        "scotland": "United Kingdom",
        "wales": "United Kingdom",
        "northern ireland": "United Kingdom",

        # Common extras (optional)
        "uae": "United Arab Emirates",
        "emirates": "United Arab Emirates",
        "south korea": "Korea, Republic of",
        "north korea": "Korea, Democratic People's Republic of",
    }

    key = raw_country.strip().lower()
    return country_map.get(key, raw_country.strip())

