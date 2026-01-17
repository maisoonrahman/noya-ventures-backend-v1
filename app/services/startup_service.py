from app.models.db import get_db
from datetime import datetime

# ------------------------------
# STEP 0: Helper to get or create startup
# ------------------------------
def get_or_create_startup(user_id, data):
    db = get_db()
    cursor = db.cursor(dictionary=True)

    # Check if startup exists for this user
    cursor.execute("SELECT id FROM startups WHERE user_id=%s", (user_id,))
    startup = cursor.fetchone()
    if startup:
        startup_id = startup['id']
    else:
        # Insert new startup (minimal info for now)
        cursor.execute("""
            INSERT INTO startups (user_id, name, website, countrycode)
            VALUES (%s, %s, %s, %s)
        """, (
            user_id,
            data.get('startupName', ''),
            data.get('website', ''),
            data.get('incorporationCountry', '')
        ))
        db.commit()
        startup_id = cursor.lastrowid

        # Initialize intake progress
        cursor.execute("""
            INSERT INTO startup_intake_progress (startup_id)
            VALUES (%s)
        """, (startup_id,))
        db.commit()

    return startup_id


# ------------------------------
# STEP 1: Founders / Team
# ------------------------------
def save_founders(startup_id, data):
    db = get_db()
    cursor = db.cursor()

    # Delete existing founders for this startup (overwrite)
    cursor.execute("DELETE FROM startup_founders WHERE startup_id=%s", (startup_id,))

    founders = data.get('founders', [])
    for founder in founders:
        cursor.execute("""
            INSERT INTO startup_founders (startup_id, name, role, email, linkedin, is_primary)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            startup_id,
            founder.get('name', ''),
            founder.get('role', ''),
            founder.get('email', ''),
            founder.get('linkedin', ''),
            founder.get('is_primary', False)
        ))
    db.commit()


# ------------------------------
# STEP 2: Company & Product
# ------------------------------
def save_company_and_product(startup_id, data):
    db = get_db()
    cursor = db.cursor()

    # 1. Update startups table with basics
    cursor.execute("""
        UPDATE startups SET
            name=%s,
            website=%s,
            countrycode=%s,
            industry_id=%s,
            model_id=%s,
            region_id=%s,
            stage_id=%s
        WHERE id=%s
    """, (
        data.get('startupName', ''),
        data.get('website', ''),
        data.get('incorporationCountry', ''),
        data.get('industry_id'),
        data.get('model_id'),
        data.get('region_id'),
        data.get('stage_id'),
        startup_id
    ))

    # 2. Save profile
    cursor.execute("DELETE FROM startup_profile WHERE startup_id=%s", (startup_id,))
    cursor.execute("""
        INSERT INTO startup_profile (
            startup_id, short_description, full_description,
            problem, current_solution, your_solution,
            product_stage, demo_link, product_type, tech_stack,
            uses_ai, ai_description
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        startup_id,
        data.get('shortDescription', ''),
        data.get('fullDescription', ''),
        data.get('problem', ''),
        data.get('currentSolution', ''),
        data.get('yourSolution', ''),
        data.get('productStage', ''),
        data.get('demoLink', ''),
        data.get('productType', ''),
        data.get('techStack', ''),
        data.get('usesAI') == 'Yes',
        data.get('aiDescription', '')
    ))

    # 3. Save IP info
    cursor.execute("DELETE FROM startup_ip WHERE startup_id=%s", (startup_id,))
    cursor.execute("""
        INSERT INTO startup_ip (startup_id, has_patents, patents_list, trademarks, open_source_notes)
        VALUES (%s, %s, %s, %s, %s)
    """, (
        startup_id,
        data.get('hasPatents') == 'Yes',
        data.get('patentsList', ''),
        data.get('trademarks', ''),
        data.get('openSource', '')
    ))

    db.commit()


# ------------------------------
# STEP 3: Market, Traction, Financials
# ------------------------------
def save_market_and_financials(startup_id, data):
    db = get_db()
    cursor = db.cursor()

    # Market
    cursor.execute("DELETE FROM startup_market WHERE startup_id=%s", (startup_id,))
    cursor.execute("""
        INSERT INTO startup_market (
            startup_id, target_customers, customer_locations,
            tam, sam, som, why_now, competitors, competitive_advantage, switching_costs
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        startup_id,
        data.get('targetCustomers', ''),
        data.get('customerLocations', ''),
        data.get('tam', ''),
        data.get('sam', ''),
        data.get('som', ''),
        data.get('whyNow', ''),
        data.get('competitors', ''),
        data.get('competitiveAdvantage', ''),
        data.get('switchingCosts', '')
    ))

    # Traction
    cursor.execute("DELETE FROM startup_traction WHERE startup_id=%s", (startup_id,))
    cursor.execute("""
        INSERT INTO startup_traction (
            startup_id, traction_summary, notable_customers,
            total_users, paying_customers, monthly_active_users, churn_comments
        ) VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        startup_id,
        data.get('tractionSummary', ''),
        data.get('notableCustomers', ''),
        data.get('totalUsers', 0),
        data.get('payingCustomers', 0),
        data.get('monthlyActiveUsers', 0),
        data.get('churnComments', '')
    ))

    # Financials
    cursor.execute("DELETE FROM startup_financials WHERE startup_id=%s", (startup_id,))
    cursor.execute("""
        INSERT INTO startup_financials (
            startup_id, arr, revenue_status, annual_burn, runway, valuation
        ) VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        startup_id,
        data.get('arr') or 0,
        data.get('revenueStatus', ''),
        data.get('annualBurn') or 0,
        data.get('runway') or 0,
        data.get('valuation') or 0
    ))

    db.commit()


# ------------------------------
# STEP 4: Legal, Funding, Final
# ------------------------------
def finalize_application(startup_id, data):
    db = get_db()
    cursor = db.cursor()

    # Funding
    cursor.execute("DELETE FROM startup_funding WHERE startup_id=%s", (startup_id,))
    cursor.execute("""
        INSERT INTO startup_funding (
            startup_id, current_round, raise_amount, pre_money_valuation,
            capital_committed, special_terms, total_raised, instruments_used, past_investors
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        startup_id,
        data.get('currentRound', ''),
        data.get('raiseAmount') or 0,
        data.get('preMoneyValuation') or 0,
        data.get('capitalCommitted') or 0,
        data.get('specialTerms', ''),
        data.get('totalRaised') or 0,
        data.get('instrumentsUsed', ''),
        data.get('pastInvestors', '')
    ))

    # Legal
    cursor.execute("DELETE FROM startup_legal WHERE startup_id=%s", (startup_id,))
    cursor.execute("""
        INSERT INTO startup_legal (
            startup_id, has_legal_issues, legal_issue_details,
            data_privacy, data_storage, additional_info,
            declaration_truth, declaration_policy
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        startup_id,
        data.get('hasLegalIssues') == 'Yes',
        data.get('legalIssueDetails', ''),
        data.get('dataPrivacy', ''),
        data.get('dataStorage', ''),
        data.get('additionalInfo', ''),
        data.get('declarationTruth', False),
        data.get('declarationPolicy', False)
    ))

    # Mark step 4 completed and submitted
    cursor.execute("""
        UPDATE startup_intake_progress
        SET step_4_completed=TRUE, last_completed_step=4, submitted_at=%s
        WHERE startup_id=%s
    """, (datetime.utcnow(), startup_id))

    db.commit()


# ------------------------------
# STEP 5: Update progress
# ------------------------------
def update_progress(startup_id, step):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(f"""
        UPDATE startup_intake_progress
        SET step_{step}_completed=TRUE, last_completed_step=%s
        WHERE startup_id=%s
    """, (step, startup_id))
    db.commit()


# ------------------------------
# Helper: Get startup by user
# ------------------------------
def get_startup_by_user(user_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM startups WHERE user_id=%s", (user_id,))
    return cursor.fetchone()
