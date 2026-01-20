# 🚀 Deployment Guide

## Quick Start (Development)

### Option 1: Using the startup script (Recommended)

```bash
cd money_transfer_mvp
./start.sh
```

This will:
1. Initialize the database if it doesn't exist
2. Create default admin user
3. Start the backend on port 8000

### Option 2: Manual setup

```bash
# 1. Navigate to backend
cd money_transfer_mvp/backend

# 2. Install dependencies
pip install -r requirements.txt

# 3. Initialize database
python3 -c "import sqlite3; conn = sqlite3.connect('app.db'); conn.executescript(open('schema.sql').read()); conn.close()"

# 4. Create admin user
python3 init_admin.py

# 5. Start server
python3 main.py
# OR
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Access the Application

**Backend API:**
- URL: http://127.0.0.1:8000
- API Docs: http://127.0.0.1:8000/docs
- OpenAPI: http://127.0.0.1:8000/openapi.json

**Frontend (User App):**
1. Open `frontend/index.html` in a browser
2. Or serve with Python: `cd frontend && python3 -m http.server 8080`
3. Visit: http://localhost:8080

**Admin Dashboard:**
1. Open `admin/index.html` in a browser
2. Login with: `admin@meridian.com` / `admin123`

## Production Deployment

### Backend Deployment

#### Option 1: Cloud Platform (Heroku, Railway, Render)

**Render.com Example:**
1. Create new Web Service
2. Connect your GitHub repo
3. Build Command: `pip install -r backend/requirements.txt`
4. Start Command: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables if needed

#### Option 2: VPS (DigitalOcean, Linode, AWS EC2)

```bash
# Install dependencies
sudo apt update
sudo apt install python3 python3-pip nginx

# Clone repo
git clone <your-repo>
cd money_transfer_mvp/backend

# Install Python packages
pip3 install -r requirements.txt

# Setup systemd service
sudo nano /etc/systemd/system/meridian.service
```

**meridian.service:**
```ini
[Unit]
Description=Meridian Transfer API
After=network.target

[Service]
User=www-data
WorkingDirectory=/path/to/money_transfer_mvp/backend
ExecStart=/usr/bin/python3 -m uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# Start service
sudo systemctl enable meridian
sudo systemctl start meridian

# Configure Nginx as reverse proxy
sudo nano /etc/nginx/sites-available/meridian
```

**Nginx config:**
```nginx
server {
    listen 80;
    server_name api.meridian.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Frontend Deployment

#### Static Hosting (Netlify, Vercel, Cloudflare Pages)

**Netlify Example:**
1. Drag and drop `frontend/` folder to Netlify
2. Update `API` variable in `app.js` to production backend URL
3. Deploy!

**Important:** Update the API URL in both files:
- `frontend/app.js` - Change `const API = "http://127.0.0.1:8000"`
- `admin/admin.js` - Change `const API = "http://127.0.0.1:8000"`

To your production backend URL (e.g., `https://api.meridian.com`)

### Database

**For Production, migrate to PostgreSQL:**

1. Install PostgreSQL
2. Update `main.py` to use PostgreSQL instead of SQLite:

```python
# Replace sqlite3 with psycopg2
import psycopg2
from psycopg2.extras import RealDictCursor

DATABASE_URL = os.getenv("DATABASE_URL")

def db():
    return psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
```

3. Add to `requirements.txt`:
```
psycopg2-binary==2.9.9
```

## Mobile App Deployment

### iOS Deployment

1. **Setup**
```bash
npm run mobile:init
npm run mobile:add:ios
npm run mobile:sync
```

2. **Configure Xcode**
```bash
npm run mobile:open:ios
```

3. **In Xcode:**
   - Set your Team and Bundle ID
   - Configure signing certificates
   - Update Info.plist for permissions
   - Build and run on device/simulator

4. **App Store Submission:**
   - Archive the app
   - Submit through Xcode Organizer
   - Complete App Store Connect listing

### Android Deployment

1. **Setup**
```bash
npm run mobile:init
npm run mobile:add:android
npm run mobile:sync
```

2. **Configure Android Studio**
```bash
npm run mobile:open:android
```

3. **In Android Studio:**
   - Update package name in `build.gradle`
   - Set up signing keys
   - Configure permissions in `AndroidManifest.xml`
   - Build APK/Bundle

4. **Play Store Submission:**
   - Generate signed bundle
   - Upload to Play Console
   - Complete store listing

## Environment Variables

**Backend (.env file):**
```bash
# Database
DATABASE_URL=postgresql://user:pass@host/db

# Security
SECRET_KEY=your-secret-key-here
JWT_ALGORITHM=HS256

# Mobile Money APIs (when integrated)
MTN_API_KEY=your-mtn-api-key
ORANGE_API_KEY=your-orange-api-key

# Email (when implemented)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email
SMTP_PASS=your-password

# SMS (when implemented)
TWILIO_ACCOUNT_SID=your-sid
TWILIO_AUTH_TOKEN=your-token
TWILIO_PHONE=your-phone
```

## Security Checklist

Before going to production:

- [ ] Change default admin password
- [ ] Add password hashing (bcrypt)
- [ ] Implement JWT tokens instead of UUIDs
- [ ] Add rate limiting
- [ ] Enable HTTPS/SSL
- [ ] Configure CORS properly
- [ ] Add input validation
- [ ] Implement file upload limits
- [ ] Add logging and monitoring
- [ ] Setup backup system for database
- [ ] Add fraud detection
- [ ] Implement MFA for admin
- [ ] Security audit

## Performance Optimization

- [ ] Add Redis for caching
- [ ] Implement CDN for static files
- [ ] Database indexing
- [ ] Connection pooling
- [ ] Compress API responses
- [ ] Optimize images
- [ ] Lazy loading for frontend
- [ ] Service worker for PWA

## Monitoring

**Recommended tools:**
- Sentry - Error tracking
- Datadog - Application monitoring
- Grafana - Metrics visualization
- LogRocket - Frontend monitoring

## Compliance

**Before handling real money:**
- [ ] Register as Money Service Business (MSB)
- [ ] Implement AML/KYC procedures
- [ ] Get licenses for each state/country
- [ ] Partner with licensed financial institutions
- [ ] Setup compliance reporting
- [ ] Implement transaction monitoring
- [ ] Regular compliance audits

## Support

For deployment issues or questions, refer to:
- FastAPI docs: https://fastapi.tiangolo.com/
- Capacitor docs: https://capacitorjs.com/
- SQLite docs: https://sqlite.org/docs.html

---

**Remember:** This is an MVP. Consult with legal and financial experts before handling real money transfers.
