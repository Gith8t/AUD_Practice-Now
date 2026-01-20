# 🌍 Meridian Transfer

**Send Money. Support Education.**

A socially-conscious money transfer application for sending remittances from Minnesota, USA to West Africa with 2% of revenue supporting education initiatives in recipient countries.

## ✨ Features

### Core Money Transfer
- 💸 **Instant Transfers** - Send money to mobile money accounts in West Africa
- 🌍 **6 Countries Supported** - Liberia, Ghana, Nigeria, Senegal, Sierra Leone, Côte d'Ivoire
- 📱 **Mobile Money Integration** - MTN, Orange, Airtel, Vodafone, and local providers
- 💱 **Real-time Exchange Rates** - Competitive rates with transparent fees

### Social Impact (Inspired by TOMS Shoes Model)
- 🎓 **2% to Education** - Every transfer contributes 2% of revenue to education in recipient countries
- 🗺️ **Impact Heat Map** - Visual representation of your contributions by country
- 📊 **Transparency** - See exactly how much you've contributed to education
- 🤝 **Local Partners** - Working with education organizations in each country

### KYC & Compliance
- 🔐 **Tiered KYC System**
  - **Tier 0** (Unverified): No transfers allowed
  - **Tier 1** (Basic): $500/day, $2,000/month limit
  - **Tier 2** (Full): $5,000/day, $20,000/month limit
- 📄 **Document Upload** - Secure ID and proof of address verification
- ✅ **Admin Review** - Manual KYC review process

### FX Engine
- 📈 **Market-Based Rates** - Real exchange rates for all currencies
- 💰 **Transparent Fees** - 2.5% spread + $2.99 minimum fee (or 1% of amount)
- 📊 **Quote Preview** - See all costs before confirming transfer

### Admin Dashboard
- 👥 **User Management** - View all users and their KYC status
- ✓ **KYC Review** - Approve or reject identity documents
- 💸 **Transfer Monitoring** - Track all transactions in real-time
- 🎓 **Education Fund Tracking** - Monitor contributions by country
- 📊 **Analytics** - Platform-wide statistics and insights

### Mobile Ready
- 📱 **Capacitor Setup** - Convert to native iOS/Android apps
- 🎨 **Responsive Design** - Works seamlessly on all devices
- 🌙 **Dark Theme** - Beautiful green-themed interface

## 🏗️ Architecture

```
money_transfer_mvp/
├── backend/
│   ├── main.py              # FastAPI application with all endpoints
│   ├── schema.sql           # Database schema with all tables
│   ├── requirements.txt     # Python dependencies
│   └── init_admin.py        # Script to create admin user
├── frontend/
│   ├── index.html           # User-facing app
│   ├── app.js               # Frontend logic
│   └── styles.css           # Responsive styling
├── admin/
│   ├── index.html           # Admin dashboard
│   ├── admin.js             # Admin logic
│   └── admin.css            # Admin styling
├── capacitor.config.json    # Mobile app configuration
├── package.json             # Mobile app dependencies
└── README.md                # This file
```

## 🚀 Quick Start

### Backend Setup

1. **Install Python dependencies**
```bash
cd money_transfer_mvp/backend
pip install -r requirements.txt
```

2. **Initialize database and create admin user**
```bash
python init_admin.py
```

3. **Start the backend server**
```bash
python main.py
# or
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`

### Frontend Setup

1. **Open the user app**
```bash
cd money_transfer_mvp/frontend
# Open index.html in your browser or use a local server
python -m http.server 8080
```

Visit `http://localhost:8080`

2. **Open the admin dashboard**
```bash
cd money_transfer_mvp/admin
# Open index.html in your browser
```

**Default Admin Credentials:**
- Email: `admin@meridian.com`
- Password: `admin123` (⚠️ Change immediately!)

## 📱 Mobile App Setup

### Convert to iOS/Android

1. **Install Capacitor**
```bash
cd money_transfer_mvp
npm run mobile:init
```

2. **Add platforms**
```bash
npm run mobile:add:ios      # For iOS
npm run mobile:add:android  # For Android
```

3. **Sync web code to mobile**
```bash
npm run mobile:sync
```

4. **Open in Xcode/Android Studio**
```bash
npm run mobile:open:ios     # Open in Xcode
npm run mobile:open:android # Open in Android Studio
```

## 💳 Supported Countries & Currencies

| Country | Currency | Code | Mobile Money Providers |
|---------|----------|------|------------------------|
| 🇱🇷 Liberia | Liberian Dollar | LRD | MTN, Orange, Lonestar |
| 🇬🇭 Ghana | Ghana Cedi | GHS | MTN, Vodafone, AirtelTigo |
| 🇳🇬 Nigeria | Nigerian Naira | NGN | MTN, Airtel, Glo, 9mobile |
| 🇸🇳 Senegal | West African CFA | XOF | Orange, Free, Expresso |
| 🇸🇱 Sierra Leone | Sierra Leone Leone | SLL | Orange, Africell, Qcell |
| 🇨🇮 Côte d'Ivoire | West African CFA | XOF | MTN, Orange, Moov |

## 🎓 Education Partners

Each country has dedicated education partners:
- **Liberia**: Liberia Education Fund
- **Ghana**: Ghana Schools Initiative
- **Nigeria**: Nigeria Education Trust
- **Senegal**: Senegal Learning Centers
- **Sierra Leone**: Sierra Leone School Support
- **Côte d'Ivoire**: Ivory Coast Education Fund

## 📊 API Endpoints

### Public Endpoints
- `GET /health` - Health check
- `GET /countries` - List supported countries
- `GET /rates` - Get exchange rates
- `GET /quote` - Get transfer quote

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - User login
- `POST /auth/logout` - Logout
- `GET /auth/me` - Get current user

### KYC
- `POST /kyc/upload` - Upload KYC document
- `GET /kyc/status` - Get KYC status

### Recipients
- `POST /recipients` - Add recipient
- `GET /recipients` - List recipients
- `DELETE /recipients/{id}` - Delete recipient

### Transfers
- `POST /transfers` - Create transfer
- `GET /transfers` - List transfers
- `GET /transfers/{id}` - Get transfer details

### Analytics
- `GET /analytics/heatmap` - Get heat map data
- `GET /analytics/impact` - Get impact summary

### Admin Endpoints
- `POST /admin/login` - Admin login
- `GET /admin/dashboard` - Dashboard stats
- `GET /admin/kyc/pending` - Pending KYC reviews
- `GET /admin/kyc/{user_id}/documents` - Get user documents
- `POST /admin/kyc/review` - Review KYC document
- `GET /admin/education-fund` - Education fund stats

## 🔒 Security Features

- **KYC Compliance** - Required before transfers
- **Transaction Limits** - Tier-based daily/monthly limits
- **Document Verification** - Manual admin review
- **Session Management** - Token-based authentication
- **File Upload Validation** - Secure document storage

## 💡 Future Enhancements

### Short-term
- [ ] Email notifications for transfers
- [ ] SMS notifications via Twilio
- [ ] Real mobile money API integration
- [ ] Multi-factor authentication (MFA)
- [ ] Password hashing (bcrypt)

### Medium-term
- [ ] Automated KYC with ID verification APIs
- [ ] Recurring transfers/scheduled payments
- [ ] Transfer history export (PDF/CSV)
- [ ] Referral program
- [ ] In-app messaging

### Long-term
- [ ] Blockchain integration for transparency
- [ ] Cryptocurrency support
- [ ] Bill payment services
- [ ] Airtime top-up
- [ ] Education project voting (let users choose projects)

## 🌟 Social Impact Model

Following the TOMS Shoes "One for One" model:

**For every transfer:**
1. User pays competitive FX rate + transparent fee
2. 2% of revenue (fee + spread) goes to education fund
3. Funds are allocated to country of recipient
4. Partner organizations implement education projects
5. Users see their impact via heat map and analytics

**Example:**
- Transfer: $100 to Ghana
- Fee: $2.99
- Spread: $0.31
- Education contribution: $0.07 (2% of $3.30 revenue)
- User sees: "You've contributed $0.07 to Ghana Schools Initiative"

## 🛠️ Technology Stack

**Backend:**
- FastAPI - Modern Python web framework
- SQLite - Lightweight database
- Pydantic - Data validation
- Uvicorn - ASGI server

**Frontend:**
- Vanilla JavaScript - No framework overhead
- HTML5/CSS3 - Responsive design
- Chart.js - Data visualization (optional)

**Mobile:**
- Capacitor - Native mobile wrapper
- iOS/Android support

## 📝 License

MIT License - See LICENSE file for details

## 🤝 Contributing

This is a MVP for a social impact money transfer platform. Contributions welcome!

## 📧 Contact

For questions or support, contact the development team.

---

**Built with ❤️ for communities in Minnesota and West Africa**
