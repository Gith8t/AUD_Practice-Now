# Meridian Transfer - Mobile Access

## Quick Mobile Access (No App Store Required)

### Option 1: Deploy Frontend to Netlify/Vercel (FREE)

**Using Netlify Drop:**
1. Visit https://app.netlify.com/drop
2. Drag the `frontend/` folder onto the page
3. Get instant URL like: `https://your-app.netlify.app`
4. Open on your phone's browser
5. Add to home screen for app-like experience

**Using Vercel:**
1. Visit https://vercel.com
2. Sign up free with GitHub
3. Import your repository
4. Deploy `frontend/` folder
5. Get URL like: `https://your-app.vercel.app`

### Option 2: Local Network Access (Testing)

If both your computer and phone are on the same WiFi:

1. Find your computer's IP address:
   ```bash
   # On Linux/Mac
   ifconfig | grep "inet "
   # Or
   hostname -I
   ```

2. Start frontend server:
   ```bash
   cd money_transfer_mvp/frontend
   python3 -m http.server 8080
   ```

3. On your phone, open browser and visit:
   ```
   http://YOUR_COMPUTER_IP:8080
   ```
   Example: `http://192.168.1.100:8080`

### Option 3: Build Native Mobile App

See instructions below for iOS/Android app building.

---

## 📲 Building Native Apps (App Store Distribution)

### For iOS App

**Prerequisites:**
- Mac computer with Xcode
- Apple Developer Account ($99/year)
- Node.js installed

**Steps:**
```bash
cd money_transfer_mvp

# Install Capacitor
npm install

# Add iOS platform
npm run mobile:add:ios

# Open in Xcode
npm run mobile:open:ios

# In Xcode:
# 1. Set your Team and Bundle ID
# 2. Connect your iPhone
# 3. Click "Run" to install on your phone
# 4. Or Archive > Distribute to App Store
```

### For Android App

**Prerequisites:**
- Android Studio installed
- Google Play Developer Account ($25 one-time)

**Steps:**
```bash
cd money_transfer_mvp

# Install Capacitor
npm install

# Add Android platform
npm run mobile:add:android

# Open in Android Studio
npm run mobile:open:android

# In Android Studio:
# 1. Build > Build Bundle(s) / APK(s) > Build APK
# 2. Transfer APK to phone and install
# 3. Or Build > Generate Signed Bundle for Play Store
```

---

## 🌐 Progressive Web App (PWA)

Add to home screen for app-like experience:

**On iPhone:**
1. Open the web app in Safari
2. Tap the Share button
3. Tap "Add to Home Screen"
4. App icon appears on home screen

**On Android:**
1. Open the web app in Chrome
2. Tap the menu (3 dots)
3. Tap "Add to Home screen"
4. App icon appears on home screen

---

## ☁️ Recommended: Deploy Backend First

Before using on phone, deploy the backend:

**Free Backend Hosting:**
- **Railway.app** (Recommended)
- **Render.com**
- **Fly.io**
- **PythonAnywhere**

Then update the API URL in:
- `frontend/app.js` line 1: `const API = "https://your-backend.railway.app"`
- `admin/admin.js` line 1: `const API = "https://your-backend.railway.app"`

---

## 🚀 Fastest Path to Your Phone:

1. **Deploy frontend to Netlify** (2 minutes)
2. **Deploy backend to Railway** (5 minutes)
3. **Open on your phone's browser**
4. **Add to home screen**

Total time: ~10 minutes, $0 cost!
