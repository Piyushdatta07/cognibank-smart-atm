# 🏦 CogniBank Smart ATM

> An AI-powered Smart ATM system built with Python Flask backend and vanilla HTML/CSS/JS frontend. Features fraud detection, international transfers, government bill payments, and real-time AI financial insights.

---

## 📸 Preview

> CogniBank Smart ATM — Indian Banking with AI Cognitive Analysis, Multi-currency Support, and International Transfers across 9 countries.

---

## ✨ Features

### 🔐 Authentication
- Bank account verification with Date of Birth (like real banking)
- 3-step Smart ATM activation flow for existing bank account holders
- SHA-256 hashed PIN with strict validation (4 unique digits, no repeating)
- Account lockout after 3 failed attempts
- Session timeout with live countdown bar
- Change PIN feature

### 💰 Transactions
- **Withdraw** — with AI fraud detection
- **Deposit** — instant credit
- **Domestic Transfer** — same-country accounts only (IMPS style)
- **International Transfer** — 9 countries with live exchange rates
- **Bill Payments** — 7 Government bills + 4 Private/Utility bills

### 🌍 International Support
| Country | Currency |
|---------|----------|
| 🇮🇳 India | INR ₹ |
| 🇺🇸 USA | USD $ |
| 🇬🇧 UK | GBP £ |
| 🇨🇳 China | CNY ¥ |
| 🇮🇷 Iran | IRR ﷼ |
| 🇮🇱 Israel | ILS ₪ |
| 🇨🇦 Canada | CAD C$ |
| 🇦🇺 Australia | AUD A$ |
| 🇳🇿 New Zealand | NZD NZ$ |
| 🇦🇫 Afghanistan | AFN ؋ |

### 🧠 AI Features (powered by Claude API)
- Real-time fraud detection using Isolation Forest ML model
- AI Cognitive Analysis on dashboard (spending chips, trust score)
- AI Financial Insights panel (spending, savings, behaviour, fraud report, security)
- AI Smart Suggestion on dashboard
- AI Chat Assistant (CogniBank AI)
- Auto transaction category tagging

### 📊 Other Features
- Transaction History with fraud flagging
- Mini Statement (last 5 transactions, printable)
- Savings Goals tracker
- Export bank statement as `.txt`
- Dark / Light mode toggle
- Mobile responsive with bottom navigation
- Reference number for every transaction
- BBPS-style bill payment system

---

## 🗂️ Project Structure

```
cognibank-backend/
├── app.py                    # Flask backend — all API routes
├── model.py                  # AI fraud detection (Isolation Forest)
├── Smart_cognitive_ATM.html  # Complete frontend (single file)
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- pip

### Step 1 — Install dependencies
```bash
pip install flask flask-cors scikit-learn numpy
```

### Step 2 — Start the backend
```bash
cd cognibank-backend
python app.py
```
You should see:
```
Running on http://127.0.0.1:5000
```

### Step 3 — Start the frontend server
```bash
python -m http.server 5500
```

### Step 4 — Open in browser
```
http://localhost:5500/Smart_cognitive_ATM.html
```

---

## 🔑 Test Accounts

### 🇮🇳 India (INR ₹)
| Name | Account Number | PIN |
|------|---------------|-----|
| Raj Patel | `5593000000007711` | `5678` |
| Sarah Chen | `4242000000003819` | `1234` |
| Ana Souza | `6011000000009934` | `0000` |
| Veerendra Lakavath | `7001000000000004` | `2847` |
| Piyush Datta | `7002000000000005` | `6193` |
| Vasanth Sri | `7003000000000006` | `3751` |
| Sharan | `7004000000000007` | `9042` |

### 🇺🇸 USA (USD $)
| Name | Account Number | PIN |
|------|---------------|-----|
| James Carter | `US001000000001` | `1357` |
| Emily Thompson | `US001000000002` | `2468` |

### 🇬🇧 UK (GBP £)
| Name | Account Number | PIN |
|------|---------------|-----|
| Oliver Smith | `GB001000000001` | `1379` |
| Charlotte Brown | `GB001000000002` | `2468` |

### 🇨🇳 China (CNY ¥)
| Name | Account Number | PIN |
|------|---------------|-----|
| Wei Zhang | `CN001000000001` | `1357` |
| Mei Liu | `CN001000000002` | `3579` |

### 🇮🇷 Iran (IRR ﷼)
| Name | Account Number | PIN |
|------|---------------|-----|
| Ali Hassan | `IR001000000001` | `1357` |
| Fatima Rezaei | `IR001000000002` | `2468` |

### 🇮🇱 Israel (ILS ₪)
| Name | Account Number | PIN |
|------|---------------|-----|
| Yael Cohen | `IL001000000001` | `1379` |
| David Levi | `IL001000000002` | `3579` |

### 🇨🇦 Canada (CAD C$)
| Name | Account Number | PIN |
|------|---------------|-----|
| Liam Wilson | `CA001000000001` | `1357` |
| Sophie Martin | `CA001000000002` | `2468` |

### 🇦🇺 Australia (AUD A$)
| Name | Account Number | PIN |
|------|---------------|-----|
| Noah Johnson | `AU001000000001` | `1379` |
| Olivia Davis | `AU001000000002` | `3579` |

### 🇳🇿 New Zealand (NZD NZ$)
| Name | Account Number | PIN |
|------|---------------|-----|
| Ethan Williams | `NZ001000000001` | `1357` |
| Isla Anderson | `NZ001000000002` | `2468` |

### 🇦🇫 Afghanistan (AFN ؋)
| Name | Account Number | PIN |
|------|---------------|-----|
| Ahmad Karimi | `AF001000000001` | `1379` |
| Soraya Ahmadi | `AF001000000002` | `3579` |

### 🏛️ Unactivated Bank Accounts (for testing Smart ATM registration)
| Name | Account Number | Date of Birth |
|------|---------------|--------------|
| Arjun Mehta | `8001000000000001` | `1995-06-15` |
| Priya Sharma | `8002000000000002` | `1998-03-22` |
| Kiran Reddy | `8003000000000003` | `1992-11-08` |
| Neha Joshi | `8004000000000004` | `2000-07-14` |
| Suresh Kumar | `8005000000000005` | `1988-01-30` |

---

## 🏛️ API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/login` | Login with account number + PIN |
| POST | `/verify-bank-account` | Verify existing bank account |
| POST | `/activate` | Activate Smart ATM for verified account |
| POST | `/register` | Register new account |
| POST | `/change-pin` | Change ATM PIN |
| GET | `/user/<id>` | Get user details |
| GET | `/users` | List all users |
| POST | `/transaction` | Withdraw or deposit |
| POST | `/transfer` | Domestic transfer |
| POST | `/intl-transfer` | International transfer |
| GET | `/transactions/<id>` | Transaction history |
| GET | `/fraud-report/<id>` | Fraud report for user |

---

## 🧠 Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | HTML5, CSS3, Vanilla JavaScript |
| Backend | Python, Flask, Flask-CORS |
| Database | SQLite |
| ML Model | Scikit-learn (Isolation Forest) |
| AI | Anthropic Claude API |
| Tunneling | ngrok |

---

## 🌐 Sharing with Others (ngrok)

To share the ATM with anyone over the internet:

```bash
# Terminal 1
python app.py

# Terminal 2
ngrok http 5000
```

Update `Smart_cognitive_ATM.html`:
```javascript
const API='https://YOUR-NGROK-URL.ngrok-free.dev';
```

Open in any browser worldwide:
```
https://YOUR-NGROK-URL.ngrok-free.dev/
```

---

## ⚠️ Notes

- `database.db` is auto-created on first run — do not upload to GitHub
- The AI features (insights, chat, category tagging) require an Anthropic API key passed via browser — they gracefully fall back to local calculations if unavailable
- Exchange rates are approximate and fixed — not live market rates
- ngrok URL changes every restart on the free plan

---

## 👨‍💻 Team

**CogniBank Smart ATM — College Project**

| Name | Role |
|------|------|
| Piyush Datta | Project Lead & Full Stack Developer |
| L. Veerendra Kumar | Backend Development & Database |
| A. Vasanth | Frontend Development & UI/UX |
| Sharan R.S | AI/ML Integration & Fraud Detection |
| Tobin Antony | Testing & Deployment |

---

## 📄 License

This project is for educational purposes only.
