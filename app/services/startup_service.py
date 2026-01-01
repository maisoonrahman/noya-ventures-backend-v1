from app.models.db import get_db

# Save a specific intake step
def save_intake_step(user_id, step, data):
    db = get_db()
    cursor = db.cursor(dictionary=True)

    # Example: map step to columns
    if step == 1:
        cursor.execute(
            "UPDATE startups SET name=%s, industry=%s WHERE user_id=%s",
            (data.get('company_name'), data.get('industry'), user_id)
        )
    elif step == 2:
        cursor.execute(
            "UPDATE startups SET team_size=%s, website=%s WHERE user_id=%s",
            (data.get('team_size'), data.get('website'), user_id)
        )
    elif step == 3:
        cursor.execute(
            "UPDATE startups SET funding_stage=%s, revenue=%s WHERE user_id=%s",
            (data.get('funding_stage'), data.get('revenue'), user_id)
        )
    elif step == 4:
        cursor.execute(
            "UPDATE startups SET description=%s, goals=%s WHERE user_id=%s",
            (data.get('description'), data.get('goals'), user_id)
        )
    else:
        cursor.close()
        return {"error": "Invalid step"}

    db.commit()
    cursor.close()
    return {"message": f"Step {step} saved successfully"}

# Get startup by user ID
def get_startup_by_user(user_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM startups WHERE user_id=%s", (user_id,))
    startup = cursor.fetchone()
    cursor.close()
    return startup
