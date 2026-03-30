from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import hashlib
from model import predict_fraud
from flask import send_from_directory

app = Flask(__name__)
CORS(app)



@app.route('/')
def serve_frontend():
    return send_from_directory('.', 'Smart_cognitive_ATM.html')

def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

def hash_pin(pin):
    return hashlib.sha256(str(pin).encode()).hexdigest()

def init_db():
    conn = get_db()
    cur  = conn.cursor()

    # Pre-registered bank accounts (the "bank registry" — existing traditional accounts)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS bank_registry (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        name        TEXT    NOT NULL,
        acct_no     TEXT    UNIQUE NOT NULL,
        dob         TEXT    NOT NULL,
        branch      TEXT    NOT NULL,
        ifsc        TEXT    NOT NULL,
        country     TEXT    DEFAULT 'IN',
        currency    TEXT    DEFAULT 'INR',
        activated   INTEGER DEFAULT 0
    )
    """)

    # Smart ATM users — linked to bank_registry
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        registry_id INTEGER UNIQUE,
        name        TEXT    NOT NULL,
        acct_no     TEXT    UNIQUE NOT NULL,
        pin_hash    TEXT    NOT NULL,
        balance     REAL    DEFAULT 0,
        country     TEXT    DEFAULT 'IN',
        currency    TEXT    DEFAULT 'INR'
    )
    """)

    # Transactions — all in INR equivalent
    cur.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id             INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id        INTEGER,
        amount         REAL,
        amount_foreign REAL    DEFAULT 0,
        currency       TEXT    DEFAULT 'INR',
        type           TEXT,
        note           TEXT    DEFAULT '',
        is_fraud       INTEGER DEFAULT 0,
        fraud_override INTEGER DEFAULT 0,
        timestamp      DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # ── SEED BANK REGISTRY (traditional bank accounts) ──
    # Indian domestic users
    indian = [
        ('Raj Patel',          '5593000000007711', '1990-05-12', 'Mumbai Main',    'COGN0001234', 'IN',  'INR',  120045.00),
        ('Sarah Chen',         '4242000000003819', '1995-08-22', 'Delhi CP',       'COGN0002345', 'IN',  'INR',   54321.80),
        ('Ana Souza',          '6011000000009934', '1988-03-17', 'Bangalore MG Rd','COGN0003456', 'IN',  'INR',   27800.00),
        ('Veerendra Lakavath', '7001000000000004', '1993-11-05', 'Hyderabad HiTec','COGN0004567', 'IN',  'INR',   50000.00),
        ('Piyush Datta',       '7002000000000005', '1997-07-30', 'Kolkata Park St','COGN0005678', 'IN',  'INR',   50000.00),
        ('Vasanth Sri',        '7003000000000006', '1992-02-14', 'Chennai Anna Ng','COGN0006789', 'IN',  'INR',   50000.00),
        ('Sharan',             '7004000000000007', '2000-09-01', 'Pune FC Road',   'COGN0007890', 'IN',  'INR',   50000.00),
    ]
    # International CogniBank account holders
    intl = [
        # US
        ('James Carter',       'US001000000001',   '1985-04-20', 'New York',       'COGNUS001',   'US',  'USD',  250000.00),
        ('Emily Thompson',     'US001000000002',   '1991-09-15', 'Los Angeles',    'COGNUS002',   'US',  'USD',  180000.00),
        # UK
        ('Oliver Smith',       'GB001000000001',   '1987-12-03', 'London',         'COGNGB001',   'GB',  'GBP',  300000.00),
        ('Charlotte Brown',    'GB001000000002',   '1993-06-28', 'Manchester',     'COGNGB002',   'GB',  'GBP',  150000.00),
        # China
        ('Wei Zhang',          'CN001000000001',   '1989-01-11', 'Beijing',        'COGNCN001',   'CN',  'CNY',  500000.00),
        ('Mei Liu',            'CN001000000002',   '1994-07-22', 'Shanghai',       'COGNCN002',   'CN',  'CNY',  320000.00),
        # Iran
        ('Ali Hassan',         'IR001000000001',   '1986-03-08', 'Tehran',         'COGNIR001',   'IR',  'IRR', 1200000.00),
        ('Fatima Rezaei',      'IR001000000002',   '1992-10-19', 'Isfahan',        'COGNIR002',   'IR',  'IRR',  800000.00),
        # Israel
        ('Yael Cohen',         'IL001000000001',   '1988-05-30', 'Tel Aviv',       'COGNIL001',   'IL',  'ILS',  420000.00),
        ('David Levi',         'IL001000000002',   '1995-02-14', 'Jerusalem',      'COGNIL002',   'IL',  'ILS',  280000.00),
        # Canada
        ('Liam Wilson',        'CA001000000001',   '1990-08-17', 'Toronto',        'COGNCA001',   'CA',  'CAD',  210000.00),
        ('Sophie Martin',      'CA001000000002',   '1996-04-05', 'Vancouver',      'COGNCA002',   'CA',  'CAD',  160000.00),
        # Australia
        ('Noah Johnson',       'AU001000000001',   '1983-11-25', 'Sydney',         'COGNAU001',   'AU',  'AUD',  190000.00),
        ('Olivia Davis',       'AU001000000002',   '1998-01-09', 'Melbourne',      'COGNAU002',   'AU',  'AUD',  140000.00),
        # New Zealand
        ('Ethan Williams',     'NZ001000000001',   '1991-06-13', 'Auckland',       'COGNNZ001',   'NZ',  'NZD',  170000.00),
        ('Isla Anderson',      'NZ001000000002',   '1997-03-27', 'Wellington',     'COGNNZ002',   'NZ',  'NZD',  130000.00),
        # Afghanistan
        ('Ahmad Karimi',       'AF001000000001',   '1984-09-04', 'Kabul',          'COGNAF001',   'AF',  'AFN',  900000.00),
        ('Soraya Ahmadi',      'AF001000000002',   '1993-12-16', 'Herat',          'COGNAF002',   'AF',  'AFN',  600000.00),
    ]

    for name, acct, dob, branch, ifsc, country, currency, bal in indian:
        cur.execute("INSERT OR IGNORE INTO bank_registry (name,acct_no,dob,branch,ifsc,country,currency) VALUES (?,?,?,?,?,?,?)",
                    (name, acct, dob, branch, ifsc, country, currency))
        # Auto-activate Indian seed users with PIN hash (for demo)
        reg = cur.execute("SELECT id FROM bank_registry WHERE acct_no=?", (acct,)).fetchone()
        if reg:
            pins = {'5593000000007711':'5678','4242000000003819':'1234','6011000000009934':'0000',
                    '7001000000000004':'2847','7002000000000005':'6193','7003000000000006':'3751','7004000000000007':'9042'}
            if acct in pins:
                cur.execute("INSERT OR IGNORE INTO users (registry_id,name,acct_no,pin_hash,balance,country,currency) VALUES (?,?,?,?,?,?,?)",
                            (reg['id'], name, acct, hash_pin(pins[acct]), bal, country, currency))
                cur.execute("UPDATE bank_registry SET activated=1 WHERE acct_no=?", (acct,))

    for name, acct, dob, branch, ifsc, country, currency, bal in intl:
        cur.execute("INSERT OR IGNORE INTO bank_registry (name,acct_no,dob,branch,ifsc,country,currency) VALUES (?,?,?,?,?,?,?)",
                    (name, acct, dob, branch, ifsc, country, currency))
        reg = cur.execute("SELECT id FROM bank_registry WHERE acct_no=?", (acct,)).fetchone()
        if reg:
            # Default PIN for all international: first 4 digits of acct
            default_pin = acct.replace('0','').replace('1','')[:4].ljust(4,'2')
            intl_pins = {
                'US001000000001':'1357','US001000000002':'2468',
                'GB001000000001':'1379','GB001000000002':'2468',
                'CN001000000001':'1357','CN001000000002':'3579',
                'IR001000000001':'1357','IR001000000002':'2468',
                'IL001000000001':'1379','IL001000000002':'3579',
                'CA001000000001':'1357','CA001000000002':'2468',
                'AU001000000001':'1379','AU001000000002':'3579',
                'NZ001000000001':'1357','NZ001000000002':'2468',
                'AF001000000001':'1379','AF001000000002':'3579',
            }
            pin = intl_pins.get(acct, '1357')
            cur.execute("INSERT OR IGNORE INTO users (registry_id,name,acct_no,pin_hash,balance,country,currency) VALUES (?,?,?,?,?,?,?)",
                        (reg['id'], name, acct, hash_pin(pin), bal, country, currency))
            cur.execute("UPDATE bank_registry SET activated=1 WHERE acct_no=?", (acct,))

    # Unactivated accounts — for testing Smart ATM registration
    unactivated = [
    ('Arjun Mehta',   '8001000000000001', '1995-06-15', 'Mumbai Andheri',  'COGN0008001', 'IN', 'INR'),
    ('Priya Sharma',  '8002000000000002', '1998-03-22', 'Delhi Saket',     'COGN0008002', 'IN', 'INR'),
    ('Kiran Reddy',   '8003000000000003', '1992-11-08', 'Hyderabad Banjara','COGN0008003', 'IN', 'INR'),
    ('Neha Joshi',    '8004000000000004', '2000-07-14', 'Pune Kothrud',    'COGN0008004', 'IN', 'INR'),
    ('Suresh Kumar',  '8005000000000005', '1988-01-30', 'Chennai T Nagar', 'COGN0008005', 'IN', 'INR')

    ]
    for name, acct, dob, branch, ifsc, country, currency in unactivated:
        cur.execute(
                    "INSERT OR IGNORE INTO bank_registry (name,acct_no,dob,branch,ifsc,country,currency,activated) VALUES (?,?,?,?,?,?,?,0)",
                    (name, acct, dob, branch, ifsc, country, currency)
    )

    conn.commit()
    conn.close()

init_db()

# ── LOGIN ──
@app.route('/login', methods=['POST'])
def login():
    data    = request.json
    acct_no = str(data.get('acct_no', '')).strip()
    pin     = str(data.get('pin', '')).strip()
    if not acct_no or not pin:
        return jsonify({"error": "Account number and PIN required"}), 400
    conn = get_db()
    cur  = conn.cursor()
    user = cur.execute("SELECT * FROM users WHERE acct_no=? AND pin_hash=?", (acct_no, hash_pin(pin))).fetchone()
    conn.close()
    if not user:
        return jsonify({"error": "Invalid account number or PIN"}), 401
    return jsonify({"id":user["id"],"name":user["name"],"acct_no":user["acct_no"],"balance":user["balance"],"country":user["country"],"currency":user["currency"]})

# ── VERIFY BANK ACCOUNT (step 1 of registration) ──
@app.route('/verify-bank-account', methods=['POST'])
def verify_bank_account():
    data    = request.json
    acct_no = str(data.get('acct_no', '')).strip()
    dob     = str(data.get('dob', '')).strip()
    if not acct_no or not dob:
        return jsonify({"error": "Account number and date of birth required"}), 400
    conn = get_db()
    cur  = conn.cursor()
    reg  = cur.execute("SELECT * FROM bank_registry WHERE acct_no=? AND dob=?", (acct_no, dob)).fetchone()
    if not reg:
        conn.close()
        return jsonify({"error": "Account not found. Check your account number and date of birth."}), 404
    if reg['activated']:
        conn.close()
        return jsonify({"error": "This account is already registered for Smart ATM. Please login."}), 409
    conn.close()
    return jsonify({"status":"verified","name":reg["name"],"branch":reg["branch"],"ifsc":reg["ifsc"],"acct_no":reg["acct_no"]})

# ── ACTIVATE SMART ATM (step 2 of registration — set PIN) ──
@app.route('/activate', methods=['POST'])
def activate():
    data    = request.json
    acct_no = str(data.get('acct_no', '')).strip()
    pin     = str(data.get('pin', '')).strip()
    if not acct_no or not pin:
        return jsonify({"error": "Account number and PIN required"}), 400
    if len(pin) != 4 or not pin.isdigit():
        return jsonify({"error": "PIN must be exactly 4 digits"}), 400
    if len(set(pin)) < 4:
        return jsonify({"error": "PIN must have 4 unique digits — no repeating numbers allowed"}), 400

    conn = get_db()
    cur  = conn.cursor()
    reg  = cur.execute("SELECT * FROM bank_registry WHERE acct_no=?", (acct_no,)).fetchone()
    if not reg:
        conn.close()
        return jsonify({"error": "Bank account not found"}), 404
    if reg['activated']:
        conn.close()
        return jsonify({"error": "Account already activated"}), 409

    cur.execute(
        "INSERT INTO users (registry_id,name,acct_no,pin_hash,balance,country,currency) VALUES (?,?,?,?,?,?,?)",
        (reg['id'], reg['name'], acct_no, hash_pin(pin), 0.0, reg['country'], reg['currency'])
    )
    cur.execute("UPDATE bank_registry SET activated=1 WHERE acct_no=?", (acct_no,))
    conn.commit()
    new_id = cur.execute("SELECT id FROM users WHERE acct_no=?", (acct_no,)).fetchone()['id']
    conn.close()
    return jsonify({"status":"success","message":f"Smart ATM activated for {reg['name']}","id":new_id,"acct_no":acct_no,"name":reg['name']})

# ── CHANGE PIN ──
@app.route('/change-pin', methods=['POST'])
def change_pin():
    data        = request.json
    user_id     = data.get('user_id')
    old_pin     = str(data.get('old_pin', '')).strip()
    new_pin     = str(data.get('new_pin', '')).strip()
    if not user_id or not old_pin or not new_pin:
        return jsonify({"error": "All fields required"}), 400
    if len(new_pin) != 4 or not new_pin.isdigit():
        return jsonify({"error": "New PIN must be exactly 4 digits"}), 400
    if len(set(new_pin)) < 4:
        return jsonify({"error": "New PIN must have 4 unique digits — no repeating numbers"}), 400
    if old_pin == new_pin:
        return jsonify({"error": "New PIN must be different from current PIN"}), 400
    conn = get_db()
    cur  = conn.cursor()
    user = cur.execute("SELECT * FROM users WHERE id=? AND pin_hash=?", (user_id, hash_pin(old_pin))).fetchone()
    if not user:
        conn.close()
        return jsonify({"error": "Current PIN is incorrect"}), 401
    cur.execute("UPDATE users SET pin_hash=? WHERE id=?", (hash_pin(new_pin), user_id))
    conn.commit()
    conn.close()
    return jsonify({"status":"success","message":"PIN changed successfully"})

# ── GET USER ──
@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    conn = get_db()
    cur  = conn.cursor()
    user = cur.execute("SELECT id,name,acct_no,balance,country,currency FROM users WHERE id=?", (user_id,)).fetchone()
    conn.close()
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(dict(user))

# ── LIST ALL USERS ──
@app.route('/users', methods=['GET'])
def list_users():
    conn = get_db()
    cur  = conn.cursor()
    rows = cur.execute("SELECT id,name,acct_no,country,currency FROM users ORDER BY name").fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])

# ── TRANSACTION (withdraw / deposit) ──
@app.route('/transaction', methods=['POST'])
def transaction():
    data           = request.json
    user_id        = data.get('user_id')
    amount         = data.get('amount')
    txn_type       = data.get('type')
    note           = data.get('note', '')
    fraud_override = data.get('fraud_override', False)

    if user_id is None or amount is None or txn_type is None:
        return jsonify({"error": "Missing required fields"}), 400
    if amount <= 0:
        return jsonify({"error": "Invalid amount"}), 400

    conn = get_db()
    cur  = conn.cursor()
    user = cur.execute("SELECT * FROM users WHERE id=?", (user_id,)).fetchone()
    if not user:
        conn.close()
        return jsonify({"error": "User not found"}), 404

    if txn_type in ["withdraw", "transfer"]:
        if user["balance"] < amount:
            conn.close()
            return jsonify({"error": f"Insufficient balance. Available: ₹{user['balance']:.2f}"}), 400
        if not fraud_override and predict_fraud(amount):
            conn.close()
            return jsonify({"status":"fraud","message":f"₹{amount:.2f} flagged as unusually high by AI fraud detection."})
        cur.execute("UPDATE users SET balance = balance - ? WHERE id=?", (amount, user_id))
    else:
        cur.execute("UPDATE users SET balance = balance + ? WHERE id=?", (amount, user_id))

    is_fraud = 1 if fraud_override else 0
    cur.execute("INSERT INTO transactions (user_id,amount,type,note,is_fraud,fraud_override) VALUES (?,?,?,?,?,?)",
                (user_id, amount, txn_type, note, is_fraud, is_fraud))
    conn.commit()
    updated = cur.execute("SELECT balance FROM users WHERE id=?", (user_id,)).fetchone()
    conn.close()
    return jsonify({"status":"success","balance":updated["balance"]})

# ── INTERNAL TRANSFER (domestic) ──
@app.route('/transfer', methods=['POST'])
def internal_transfer():
    data           = request.json
    sender_id      = data.get('sender_id')
    recipient_acct = str(data.get('recipient_acct', '')).strip()
    amount         = data.get('amount')
    note           = data.get('note', '')
    fraud_override = data.get('fraud_override', False)

    if not sender_id or not recipient_acct or not amount:
        return jsonify({"error": "Missing required fields"}), 400
    if amount <= 0:
        return jsonify({"error": "Invalid amount"}), 400

    conn      = get_db()
    cur       = conn.cursor()
    sender    = cur.execute("SELECT * FROM users WHERE id=?", (sender_id,)).fetchone()
    recipient = cur.execute("SELECT * FROM users WHERE acct_no=?", (recipient_acct,)).fetchone()

    if not sender:
        conn.close()
        return jsonify({"error": "Sender not found"}), 404
    if not recipient:
        conn.close()
        return jsonify({"error": "Recipient account not found in CogniBank"}), 404
    if sender["id"] == recipient["id"]:
        conn.close()
        return jsonify({"error": "Cannot transfer to your own account"}), 400
    if sender["balance"] < amount:
        conn.close()
        return jsonify({"error": f"Insufficient balance. Available: ₹{sender['balance']:.2f}"}), 400
    if not fraud_override and predict_fraud(amount):
        conn.close()
        return jsonify({"status":"fraud","message":f"Transfer of ₹{amount:.2f} flagged as suspicious."})

    is_fraud = 1 if fraud_override else 0
    cur.execute("UPDATE users SET balance = balance - ? WHERE id=?", (amount, sender_id))
    cur.execute("INSERT INTO transactions (user_id,amount,type,note,is_fraud,fraud_override) VALUES (?,?,?,?,?,?)",
                (sender_id, amount, 'transfer', f"To {recipient['name']} ({recipient_acct}) {note}", is_fraud, is_fraud))
    cur.execute("UPDATE users SET balance = balance + ? WHERE id=?", (amount, recipient["id"]))
    cur.execute("INSERT INTO transactions (user_id,amount,type,note,is_fraud,fraud_override) VALUES (?,?,?,?,?,?)",
                (recipient["id"], amount, 'credit', f"From {sender['name']} ({sender['acct_no']}) {note}", 0, 0))

    conn.commit()
    updated = cur.execute("SELECT balance FROM users WHERE id=?", (sender_id,)).fetchone()
    conn.close()
    return jsonify({"status":"success","balance":updated["balance"],"recipient_name":recipient["name"]})

# ── INTERNATIONAL TRANSFER (INR deducted, foreign amount recorded) ──
@app.route('/intl-transfer', methods=['POST'])
def intl_transfer():
    data           = request.json
    sender_id      = data.get('sender_id')
    recipient_acct = str(data.get('recipient_acct', '')).strip()
    amount_inr     = data.get('amount_inr')      # INR to deduct from sender
    amount_foreign = data.get('amount_foreign')  # Foreign amount for record
    currency       = str(data.get('currency', 'USD')).strip()
    note           = data.get('note', '')
    fraud_override = data.get('fraud_override', False)

    if not sender_id or not recipient_acct or not amount_inr:
        return jsonify({"error": "Missing required fields"}), 400
    if amount_inr <= 0:
        return jsonify({"error": "Invalid amount"}), 400

    conn      = get_db()
    cur       = conn.cursor()
    sender    = cur.execute("SELECT * FROM users WHERE id=?", (sender_id,)).fetchone()
    recipient = cur.execute("SELECT * FROM users WHERE acct_no=?", (recipient_acct,)).fetchone()

    if not sender:
        conn.close()
        return jsonify({"error": "Sender not found"}), 404
    if not recipient:
        conn.close()
        return jsonify({"error": "Recipient CogniBank account not found"}), 404
    if sender["balance"] < amount_inr:
        conn.close()
        return jsonify({"error": f"Insufficient balance. Available: ₹{sender['balance']:.2f}"}), 400
    if not fraud_override and predict_fraud(amount_inr):
        conn.close()
        return jsonify({"status":"fraud","message":f"International transfer of ₹{amount_inr:.2f} flagged as suspicious."})

    is_fraud = 1 if fraud_override else 0
    # Debit sender in INR
    cur.execute("UPDATE users SET balance = balance - ? WHERE id=?", (amount_inr, sender_id))
    cur.execute("INSERT INTO transactions (user_id,amount,amount_foreign,currency,type,note,is_fraud,fraud_override) VALUES (?,?,?,?,?,?,?,?)",
                (sender_id, amount_inr, amount_foreign, currency, 'intl_transfer',
                 f"Intl to {recipient['name']} [{currency}] {note}", is_fraud, is_fraud))
    # Credit recipient in their currency (stored as INR equivalent for simplicity)
    cur.execute("UPDATE users SET balance = balance + ? WHERE id=?", (amount_inr, recipient["id"]))
    cur.execute("INSERT INTO transactions (user_id,amount,amount_foreign,currency,type,note,is_fraud,fraud_override) VALUES (?,?,?,?,?,?,?,?)",
                (recipient["id"], amount_inr, amount_foreign, currency, 'intl_credit',
                 f"Intl from {sender['name']} [INR] {note}", 0, 0))

    conn.commit()
    updated = cur.execute("SELECT balance FROM users WHERE id=?", (sender_id,)).fetchone()
    conn.close()
    return jsonify({"status":"success","balance":updated["balance"],"recipient_name":recipient["name"],"currency":currency,"amount_foreign":amount_foreign})

# ── HISTORY ──
@app.route('/transactions/<int:user_id>', methods=['GET'])
def get_transactions(user_id):
    conn = get_db()
    cur  = conn.cursor()
    rows = cur.execute("SELECT * FROM transactions WHERE user_id=? ORDER BY timestamp DESC", (user_id,)).fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])

# ── FRAUD REPORT ──
@app.route('/fraud-report/<int:user_id>', methods=['GET'])
def fraud_report(user_id):
    conn = get_db()
    cur  = conn.cursor()
    rows = cur.execute("SELECT * FROM transactions WHERE user_id=? AND (is_fraud=1 OR fraud_override=1) ORDER BY timestamp DESC", (user_id,)).fetchall()
    total_fraud = cur.execute("SELECT COUNT(*) as cnt FROM transactions WHERE is_fraud=1").fetchone()["cnt"]
    conn.close()
    return jsonify({"user_fraud_transactions":[dict(r) for r in rows],"system_total_fraud_count":total_fraud})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
