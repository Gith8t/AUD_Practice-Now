from fastapi import FastAPI, HTTPException, Header, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime, timedelta
import sqlite3
import uuid
import os
import json

app = FastAPI(title="Meridian Transfer - Money Transfer with Social Impact")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB = "app.db"
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def db():
    conn = sqlite3.connect(DB, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

# Initialize database
with db() as conn:
    conn.executescript(open("schema.sql").read())

# ---------------- MODELS ----------------

class RegisterIn(BaseModel):
    email: EmailStr
    name: str
    password: str
    phone: str
    address: str
    city: str
    state: str = "Minnesota"
    zip_code: str
    date_of_birth: str

class LoginIn(BaseModel):
    email: EmailStr
    password: str

class KYCSubmission(BaseModel):
    document_type: str
    document_number: str

class RecipientIn(BaseModel):
    name: str
    phone: str
    country: str
    mobile_money_provider: str
    mobile_money_number: str

class TransferIn(BaseModel):
    recipient_id: int
    send_amount: float
    receive_currency: str

class KYCReview(BaseModel):
    document_id: int
    status: str  # APPROVED or REJECTED
    rejection_reason: Optional[str] = None

class AdminLogin(BaseModel):
    email: EmailStr
    password: str

# ---------------- HELPERS ----------------

def get_user(token: str):
    """Get user ID from session token"""
    conn = db()
    cur = conn.cursor()
    cur.execute(
        "SELECT users.id, users.kyc_tier FROM sessions JOIN users ON users.id=sessions.user_id WHERE token=?",
        (token,)
    )
    row = cur.fetchone()
    if not row:
        raise HTTPException(401, "Invalid session")
    return {"id": row[0], "kyc_tier": row[1]}

def get_admin(token: str):
    """Get admin user from token"""
    conn = db()
    cur = conn.cursor()
    cur.execute(
        "SELECT admin_users.id, admin_users.role FROM sessions JOIN admin_users ON admin_users.id=sessions.user_id WHERE token=?",
        (token,)
    )
    row = cur.fetchone()
    if not row:
        raise HTTPException(401, "Invalid admin session")
    return {"id": row[0], "role": row[1]}

def check_transaction_limits(user_id: int, kyc_tier: int, amount: float):
    """Check if transaction is within limits"""
    conn = db()
    cur = conn.cursor()

    # Get limits for tier
    cur.execute("SELECT daily_limit, monthly_limit, per_transaction_limit FROM transaction_limits WHERE kyc_tier=?", (kyc_tier,))
    limits = cur.fetchone()
    if not limits:
        raise HTTPException(400, "Invalid KYC tier")

    daily_limit, monthly_limit, per_tx_limit = limits

    # Check per-transaction limit
    if amount > per_tx_limit:
        raise HTTPException(400, f"Amount exceeds per-transaction limit of ${per_tx_limit}")

    # Check daily limit
    today = datetime.now().date()
    cur.execute(
        """SELECT SUM(send_amount) FROM transfers
           WHERE user_id=? AND DATE(created_at)=? AND status NOT IN ('FAILED', 'CANCELLED')""",
        (user_id, today)
    )
    daily_total = cur.fetchone()[0] or 0
    if daily_total + amount > daily_limit:
        raise HTTPException(400, f"Daily limit of ${daily_limit} exceeded. Used: ${daily_total}")

    # Check monthly limit
    first_day = datetime.now().replace(day=1).date()
    cur.execute(
        """SELECT SUM(send_amount) FROM transfers
           WHERE user_id=? AND DATE(created_at)>=? AND status NOT IN ('FAILED', 'CANCELLED')""",
        (user_id, first_day)
    )
    monthly_total = cur.fetchone()[0] or 0
    if monthly_total + amount > monthly_limit:
        raise HTTPException(400, f"Monthly limit of ${monthly_limit} exceeded. Used: ${monthly_total}")

    return True

def calculate_transfer_cost(send_amount: float, to_currency: str):
    """Calculate FX conversion with spread and fees"""
    conn = db()
    cur = conn.cursor()

    # Get exchange rate
    cur.execute(
        "SELECT base_rate, spread_percentage, effective_rate FROM exchange_rates WHERE from_currency='USD' AND to_currency=?",
        (to_currency,)
    )
    rate_row = cur.fetchone()
    if not rate_row:
        raise HTTPException(400, f"Currency {to_currency} not supported")

    base_rate, spread_pct, effective_rate = rate_row

    # Calculate amounts
    receive_amount = send_amount * base_rate
    spread_amount = send_amount * base_rate * (spread_pct / 100)
    fee_amount = max(2.99, send_amount * 0.01)  # $2.99 minimum or 1% of amount

    # Revenue = fee + spread
    revenue = fee_amount + spread_amount
    education_contribution = revenue * 0.02  # 2% of revenue to education

    total_cost = send_amount + fee_amount

    return {
        "send_amount": round(send_amount, 2),
        "receive_amount": round(receive_amount, 2),
        "exchange_rate": base_rate,
        "effective_rate": effective_rate,
        "fee_amount": round(fee_amount, 2),
        "spread_amount": round(spread_amount, 2),
        "education_contribution": round(education_contribution, 2),
        "total_cost": round(total_cost, 2)
    }

# ---------------- PUBLIC ROUTES ----------------

@app.get("/health")
def health():
    return {"status": "ok", "service": "Meridian Transfer"}

@app.get("/countries")
def get_countries():
    """Get supported countries and mobile money providers"""
    conn = db()
    cur = conn.cursor()
    cur.execute("SELECT country_code, country_name, mobile_money_providers, education_partner, flag_emoji FROM country_settings WHERE supported=1")
    countries = []
    for row in cur.fetchall():
        countries.append({
            "code": row[0],
            "name": row[1],
            "providers": json.loads(row[2]),
            "education_partner": row[3],
            "flag": row[4]
        })
    return countries

@app.get("/rates")
def get_rates():
    """Get all exchange rates"""
    conn = db()
    cur = conn.cursor()
    cur.execute("SELECT to_currency, base_rate, spread_percentage, effective_rate FROM exchange_rates WHERE from_currency='USD'")
    rates = {}
    for row in cur.fetchall():
        rates[row[0]] = {
            "base_rate": row[1],
            "spread": row[2],
            "effective_rate": row[3]
        }
    return rates

@app.get("/quote")
def get_quote(amount: float, to_currency: str):
    """Get transfer quote"""
    if amount <= 0:
        raise HTTPException(400, "Amount must be positive")

    quote = calculate_transfer_cost(amount, to_currency)
    return quote

# ---------------- AUTH ROUTES ----------------

@app.post("/auth/register")
def register(data: RegisterIn):
    """Register new user"""
    conn = db()
    try:
        cur = conn.cursor()
        cur.execute(
            """INSERT INTO users (email, name, password, phone, address, city, state, zip_code, date_of_birth)
               VALUES (?,?,?,?,?,?,?,?,?)""",
            (data.email, data.name, data.password, data.phone, data.address, data.city, data.state, data.zip_code, data.date_of_birth)
        )
        conn.commit()
        return {"success": True, "message": "Account created. Please complete KYC to start transferring."}
    except sqlite3.IntegrityError:
        raise HTTPException(400, "Email already exists")

@app.post("/auth/login")
def login(data: LoginIn):
    """User login"""
    conn = db()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, name, kyc_status, kyc_tier FROM users WHERE email=? AND password=?",
        (data.email, data.password)
    )
    row = cur.fetchone()
    if not row:
        raise HTTPException(401, "Invalid credentials")

    token = str(uuid.uuid4())
    conn.execute("INSERT INTO sessions (token, user_id) VALUES (?,?)", (token, row[0]))
    conn.commit()

    return {
        "token": token,
        "user": {
            "id": row[0],
            "name": row[1],
            "kyc_status": row[2],
            "kyc_tier": row[3]
        }
    }

@app.post("/auth/logout")
def logout(authorization: str = Header(None)):
    """User logout"""
    conn = db()
    conn.execute("DELETE FROM sessions WHERE token=?", (authorization,))
    conn.commit()
    return {"success": True}

@app.get("/auth/me")
def get_current_user(authorization: str = Header(None)):
    """Get current user profile"""
    user = get_user(authorization)
    conn = db()
    cur = conn.cursor()
    cur.execute(
        """SELECT id, email, name, phone, address, city, state, zip_code,
                  kyc_status, kyc_tier, created_at FROM users WHERE id=?""",
        (user["id"],)
    )
    row = cur.fetchone()
    if not row:
        raise HTTPException(404, "User not found")

    # Get limits
    cur.execute("SELECT daily_limit, monthly_limit, per_transaction_limit FROM transaction_limits WHERE kyc_tier=?", (row[9],))
    limits = cur.fetchone()

    return {
        "id": row[0],
        "email": row[1],
        "name": row[2],
        "phone": row[3],
        "address": row[4],
        "city": row[5],
        "state": row[6],
        "zip_code": row[7],
        "kyc_status": row[8],
        "kyc_tier": row[9],
        "limits": {
            "daily": limits[0] if limits else 0,
            "monthly": limits[1] if limits else 0,
            "per_transaction": limits[2] if limits else 0
        } if limits else None,
        "joined": row[10]
    }

# ---------------- KYC ROUTES ----------------

@app.post("/kyc/upload")
async def upload_kyc_document(
    authorization: str = Header(None),
    document_type: str = Form(...),
    document_number: str = Form(...),
    file: UploadFile = File(...)
):
    """Upload KYC document"""
    user = get_user(authorization)

    # Save file
    file_ext = os.path.splitext(file.filename)[1]
    filename = f"{user['id']}_{document_type}_{uuid.uuid4()}{file_ext}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)

    # Save to database
    conn = db()
    conn.execute(
        """INSERT INTO kyc_documents (user_id, document_type, document_number, file_path)
           VALUES (?,?,?,?)""",
        (user["id"], document_type, document_number, file_path)
    )

    # Update user KYC status
    conn.execute(
        "UPDATE users SET kyc_status='PENDING', kyc_submitted_at=? WHERE id=?",
        (datetime.now(), user["id"])
    )
    conn.commit()

    return {"success": True, "message": "Document uploaded. KYC review in progress."}

@app.get("/kyc/status")
def get_kyc_status(authorization: str = Header(None)):
    """Get KYC status and documents"""
    user = get_user(authorization)
    conn = db()
    cur = conn.cursor()

    cur.execute(
        """SELECT id, document_type, status, rejection_reason, uploaded_at, reviewed_at
           FROM kyc_documents WHERE user_id=? ORDER BY uploaded_at DESC""",
        (user["id"],)
    )

    documents = []
    for row in cur.fetchall():
        documents.append({
            "id": row[0],
            "type": row[1],
            "status": row[2],
            "rejection_reason": row[3],
            "uploaded_at": row[4],
            "reviewed_at": row[5]
        })

    cur.execute("SELECT kyc_status, kyc_tier FROM users WHERE id=?", (user["id"],))
    user_row = cur.fetchone()

    return {
        "status": user_row[0],
        "tier": user_row[1],
        "documents": documents
    }

# ---------------- RECIPIENT ROUTES ----------------

@app.post("/recipients")
def add_recipient(data: RecipientIn, authorization: str = Header(None)):
    """Add recipient"""
    user = get_user(authorization)
    conn = db()
    conn.execute(
        """INSERT INTO recipients (user_id, name, phone, country, mobile_money_provider, mobile_money_number)
           VALUES (?,?,?,?,?,?)""",
        (user["id"], data.name, data.phone, data.country, data.mobile_money_provider, data.mobile_money_number)
    )
    conn.commit()
    return {"success": True}

@app.get("/recipients")
def list_recipients(authorization: str = Header(None)):
    """List user's recipients"""
    user = get_user(authorization)
    conn = db()
    cur = conn.cursor()
    cur.execute(
        """SELECT id, name, phone, country, mobile_money_provider, mobile_money_number, created_at
           FROM recipients WHERE user_id=? ORDER BY created_at DESC""",
        (user["id"],)
    )

    recipients = []
    for row in cur.fetchall():
        recipients.append({
            "id": row[0],
            "name": row[1],
            "phone": row[2],
            "country": row[3],
            "provider": row[4],
            "number": row[5],
            "created_at": row[6]
        })
    return recipients

@app.delete("/recipients/{recipient_id}")
def delete_recipient(recipient_id: int, authorization: str = Header(None)):
    """Delete recipient"""
    user = get_user(authorization)
    conn = db()
    conn.execute("DELETE FROM recipients WHERE id=? AND user_id=?", (recipient_id, user["id"]))
    conn.commit()
    return {"success": True}

# ---------------- TRANSFER ROUTES ----------------

@app.post("/transfers")
def create_transfer(data: TransferIn, authorization: str = Header(None)):
    """Create money transfer"""
    user = get_user(authorization)

    # Check KYC
    if user["kyc_tier"] == 0:
        raise HTTPException(403, "Please complete KYC verification before transferring money")

    # Check limits
    check_transaction_limits(user["id"], user["kyc_tier"], data.send_amount)

    # Calculate costs
    costs = calculate_transfer_cost(data.send_amount, data.receive_currency)

    # Get recipient
    conn = db()
    cur = conn.cursor()
    cur.execute("SELECT id, country FROM recipients WHERE id=? AND user_id=?", (data.recipient_id, user["id"]))
    recipient = cur.fetchone()
    if not recipient:
        raise HTTPException(404, "Recipient not found")

    # Create transfer
    cur.execute(
        """INSERT INTO transfers
           (user_id, recipient_id, send_amount, send_currency, receive_amount, receive_currency,
            exchange_rate, fee_amount, spread_amount, education_contribution, total_cost, status)
           VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
        (user["id"], data.recipient_id, costs["send_amount"], "USD", costs["receive_amount"],
         data.receive_currency, costs["exchange_rate"], costs["fee_amount"], costs["spread_amount"],
         costs["education_contribution"], costs["total_cost"], "PROCESSING")
    )
    transfer_id = cur.lastrowid

    # Record education contribution
    cur.execute(
        """INSERT INTO education_fund (transfer_id, country, amount_usd) VALUES (?,?,?)""",
        (transfer_id, recipient[1], costs["education_contribution"])
    )

    conn.commit()

    # Simulate mobile money processing (in production, integrate with actual API)
    conn.execute(
        """UPDATE transfers SET status='COMPLETED', completed_at=?, mobile_money_transaction_id=?
           WHERE id=?""",
        (datetime.now(), f"MM{uuid.uuid4().hex[:12].upper()}", transfer_id)
    )
    conn.commit()

    return {
        "transfer_id": transfer_id,
        "status": "COMPLETED",
        "education_contribution": costs["education_contribution"],
        "message": f"${costs['education_contribution']:.2f} contributed to education in {recipient[1]}"
    }

@app.get("/transfers")
def list_transfers(authorization: str = Header(None), limit: int = 50):
    """List user's transfers"""
    user = get_user(authorization)
    conn = db()
    cur = conn.cursor()
    cur.execute(
        """SELECT t.id, t.send_amount, t.receive_amount, t.receive_currency, t.fee_amount,
                  t.education_contribution, t.status, t.created_at, t.completed_at,
                  r.name as recipient_name, r.country
           FROM transfers t
           JOIN recipients r ON t.recipient_id = r.id
           WHERE t.user_id=?
           ORDER BY t.created_at DESC LIMIT ?""",
        (user["id"], limit)
    )

    transfers = []
    for row in cur.fetchall():
        transfers.append({
            "id": row[0],
            "send_amount": row[1],
            "receive_amount": row[2],
            "currency": row[3],
            "fee": row[4],
            "education_contribution": row[5],
            "status": row[6],
            "created_at": row[7],
            "completed_at": row[8],
            "recipient": row[9],
            "country": row[10]
        })
    return transfers

@app.get("/transfers/{transfer_id}")
def get_transfer_details(transfer_id: int, authorization: str = Header(None)):
    """Get transfer details"""
    user = get_user(authorization)
    conn = db()
    cur = conn.cursor()
    cur.execute(
        """SELECT t.*, r.name as recipient_name, r.country, r.mobile_money_provider, r.mobile_money_number
           FROM transfers t
           JOIN recipients r ON t.recipient_id = r.id
           WHERE t.id=? AND t.user_id=?""",
        (transfer_id, user["id"])
    )
    row = cur.fetchone()
    if not row:
        raise HTTPException(404, "Transfer not found")

    return dict(row)

# ---------------- ANALYTICS ROUTES ----------------

@app.get("/analytics/heatmap")
def get_heatmap_data(authorization: str = Header(None)):
    """Get heat map data - transfers by country with education contributions"""
    user = get_user(authorization)
    conn = db()
    cur = conn.cursor()

    cur.execute(
        """SELECT r.country,
                  COUNT(t.id) as transfer_count,
                  SUM(t.send_amount) as total_sent,
                  SUM(t.education_contribution) as total_education,
                  cs.country_name, cs.flag_emoji, cs.education_partner
           FROM transfers t
           JOIN recipients r ON t.recipient_id = r.id
           LEFT JOIN country_settings cs ON r.country = cs.country_code
           WHERE t.user_id=? AND t.status='COMPLETED'
           GROUP BY r.country""",
        (user["id"],)
    )

    heatmap = []
    for row in cur.fetchall():
        heatmap.append({
            "country_code": row[0],
            "country_name": row[4],
            "flag": row[5],
            "transfer_count": row[1],
            "total_sent_usd": round(row[2], 2),
            "education_contribution_usd": round(row[3], 2),
            "education_partner": row[6]
        })

    return heatmap

@app.get("/analytics/impact")
def get_impact_summary(authorization: str = Header(None)):
    """Get overall social impact summary"""
    user = get_user(authorization)
    conn = db()
    cur = conn.cursor()

    # User's total contribution
    cur.execute(
        """SELECT COUNT(*) as transfers, SUM(send_amount) as total_sent,
                  SUM(education_contribution) as total_education
           FROM transfers WHERE user_id=? AND status='COMPLETED'""",
        (user["id"],)
    )
    user_stats = cur.fetchone()

    # Platform-wide stats
    cur.execute(
        """SELECT COUNT(*) as transfers, SUM(education_contribution) as total_education
           FROM transfers WHERE status='COMPLETED'"""
    )
    platform_stats = cur.fetchone()

    # Education fund by country
    cur.execute(
        """SELECT ef.country, SUM(ef.amount_usd) as total, cs.education_partner
           FROM education_fund ef
           LEFT JOIN country_settings cs ON ef.country = cs.country_code
           WHERE ef.transfer_id IN (SELECT id FROM transfers WHERE user_id=?)
           GROUP BY ef.country""",
        (user["id"],)
    )

    by_country = []
    for row in cur.fetchall():
        by_country.append({
            "country": row[0],
            "amount": round(row[1], 2),
            "partner": row[2]
        })

    return {
        "your_impact": {
            "transfers": user_stats[0] or 0,
            "total_sent": round(user_stats[1] or 0, 2),
            "education_contribution": round(user_stats[2] or 0, 2),
            "by_country": by_country
        },
        "platform_impact": {
            "total_transfers": platform_stats[0] or 0,
            "total_education_fund": round(platform_stats[1] or 0, 2)
        }
    }

# ---------------- ADMIN ROUTES ----------------

@app.post("/admin/login")
def admin_login(data: AdminLogin):
    """Admin login"""
    conn = db()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, name, role FROM admin_users WHERE email=? AND password=?",
        (data.email, data.password)
    )
    row = cur.fetchone()
    if not row:
        raise HTTPException(401, "Invalid admin credentials")

    token = str(uuid.uuid4())
    conn.execute("INSERT INTO sessions (token, user_id) VALUES (?,?)", (token, row[0]))
    conn.commit()

    return {"token": token, "admin": {"id": row[0], "name": row[1], "role": row[2]}}

@app.get("/admin/dashboard")
def admin_dashboard(authorization: str = Header(None)):
    """Admin dashboard statistics"""
    admin = get_admin(authorization)
    conn = db()
    cur = conn.cursor()

    # Overall stats
    cur.execute("SELECT COUNT(*) FROM users")
    total_users = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM users WHERE kyc_status='PENDING'")
    pending_kyc = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM transfers WHERE status='COMPLETED'")
    total_transfers = cur.fetchone()[0]

    cur.execute("SELECT SUM(send_amount), SUM(fee_amount), SUM(education_contribution) FROM transfers WHERE status='COMPLETED'")
    money_stats = cur.fetchone()

    # Recent transfers
    cur.execute(
        """SELECT t.id, u.name, t.send_amount, t.receive_currency, t.status, t.created_at
           FROM transfers t
           JOIN users u ON t.user_id = u.id
           ORDER BY t.created_at DESC LIMIT 10"""
    )
    recent_transfers = [dict(row) for row in cur.fetchall()]

    return {
        "total_users": total_users,
        "pending_kyc": pending_kyc,
        "total_transfers": total_transfers,
        "total_volume": round(money_stats[0] or 0, 2),
        "total_fees": round(money_stats[1] or 0, 2),
        "total_education_fund": round(money_stats[2] or 0, 2),
        "recent_transfers": recent_transfers
    }

@app.get("/admin/kyc/pending")
def get_pending_kyc(authorization: str = Header(None)):
    """Get pending KYC submissions"""
    admin = get_admin(authorization)
    conn = db()
    cur = conn.cursor()

    cur.execute(
        """SELECT u.id, u.name, u.email, u.kyc_submitted_at,
                  COUNT(kd.id) as documents
           FROM users u
           LEFT JOIN kyc_documents kd ON u.id = kd.user_id AND kd.status='PENDING'
           WHERE u.kyc_status='PENDING'
           GROUP BY u.id
           ORDER BY u.kyc_submitted_at ASC"""
    )

    pending = []
    for row in cur.fetchall():
        pending.append({
            "user_id": row[0],
            "name": row[1],
            "email": row[2],
            "submitted_at": row[3],
            "documents_count": row[4]
        })

    return pending

@app.get("/admin/kyc/{user_id}/documents")
def get_user_kyc_documents(user_id: int, authorization: str = Header(None)):
    """Get KYC documents for a user"""
    admin = get_admin(authorization)
    conn = db()
    cur = conn.cursor()

    cur.execute(
        """SELECT id, document_type, document_number, file_path, status, uploaded_at
           FROM kyc_documents WHERE user_id=? ORDER BY uploaded_at DESC""",
        (user_id,)
    )

    documents = []
    for row in cur.fetchall():
        documents.append({
            "id": row[0],
            "type": row[1],
            "number": row[2],
            "file_path": row[3],
            "status": row[4],
            "uploaded_at": row[5]
        })

    return documents

@app.post("/admin/kyc/review")
def review_kyc(data: KYCReview, authorization: str = Header(None)):
    """Review KYC document"""
    admin = get_admin(authorization)
    conn = db()
    cur = conn.cursor()

    # Update document
    cur.execute(
        """UPDATE kyc_documents SET status=?, rejection_reason=?, reviewed_at=?, reviewed_by=?
           WHERE id=?""",
        (data.status, data.rejection_reason, datetime.now(), admin["id"], data.document_id)
    )

    # Get user_id
    cur.execute("SELECT user_id FROM kyc_documents WHERE id=?", (data.document_id,))
    user_id = cur.fetchone()[0]

    # Check if all documents are approved
    cur.execute(
        "SELECT COUNT(*) FROM kyc_documents WHERE user_id=? AND status='PENDING'",
        (user_id,)
    )
    pending_count = cur.fetchone()[0]

    if pending_count == 0:
        # Check if we have required documents approved
        cur.execute(
            """SELECT COUNT(DISTINCT document_type) FROM kyc_documents
               WHERE user_id=? AND status='APPROVED'""",
            (user_id,)
        )
        approved_types = cur.fetchone()[0]

        if approved_types >= 2:  # Need at least ID and proof of address
            # Approve KYC - set to tier 2 (full KYC)
            cur.execute(
                """UPDATE users SET kyc_status='VERIFIED', kyc_tier=2, kyc_verified_at=?
                   WHERE id=?""",
                (datetime.now(), user_id)
            )
        elif approved_types >= 1:
            # Basic KYC - tier 1
            cur.execute(
                """UPDATE users SET kyc_status='VERIFIED', kyc_tier=1, kyc_verified_at=?
                   WHERE id=?""",
                (datetime.now(), user_id)
            )
        else:
            # Rejected
            cur.execute("UPDATE users SET kyc_status='REJECTED' WHERE id=?", (user_id,))

    conn.commit()
    return {"success": True}

@app.get("/admin/education-fund")
def get_education_fund_stats(authorization: str = Header(None)):
    """Get education fund statistics by country"""
    admin = get_admin(authorization)
    conn = db()
    cur = conn.cursor()

    cur.execute(
        """SELECT ef.country, cs.country_name, cs.education_partner,
                  COUNT(ef.id) as contributions,
                  SUM(ef.amount_usd) as total_amount,
                  SUM(CASE WHEN ef.disbursed=1 THEN ef.amount_usd ELSE 0 END) as disbursed
           FROM education_fund ef
           LEFT JOIN country_settings cs ON ef.country = cs.country_code
           GROUP BY ef.country
           ORDER BY total_amount DESC"""
    )

    stats = []
    for row in cur.fetchall():
        stats.append({
            "country": row[0],
            "country_name": row[1],
            "partner": row[2],
            "contributions": row[3],
            "total_usd": round(row[4], 2),
            "disbursed_usd": round(row[5], 2),
            "pending_usd": round(row[4] - row[5], 2)
        })

    return stats

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
