# 📱 Get Meridian Transfer on Your Phone

## ⚡ FASTEST METHOD (5 Minutes, FREE)

### Step 1: Deploy Frontend to Netlify

1. **Go to:** https://app.netlify.com/drop

2. **Sign up** (free) if you don't have an account

3. **Drag and drop** the entire `frontend` folder onto the Netlify Drop page

4. **Wait 30 seconds** - Netlify will give you a URL like:
   ```
   https://random-name-12345.netlify.app
   ```

5. **Open that URL on your phone!** 🎉

### Step 2: Add to Home Screen

**On iPhone:**
1. Open the URL in Safari
2. Tap the Share button (box with arrow)
3. Scroll down and tap "Add to Home Screen"
4. Tap "Add"
5. ✅ App icon now on your home screen!

**On Android:**
1. Open the URL in Chrome
2. Tap the menu (3 vertical dots)
3. Tap "Add to Home screen"
4. Tap "Add"
5. ✅ App icon now on your home screen!

---

## 🌐 Deploy Backend (Recommended)

The app needs a backend to work. Deploy it for free:

### Quick Backend Deploy to Railway.app

1. **Go to:** https://railway.app

2. **Sign up** with GitHub (free)

3. **Click:** "New Project" → "Deploy from GitHub repo"

4. **Select** your repository

5. **Settings:**
   - Root Directory: `money_transfer_mvp/backend`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

6. **Railway gives you a URL** like:
   ```
   https://your-app.railway.app
   ```

7. **Update your frontend:**
   - Edit `frontend/app.js`
   - Change line 1: `const API = "https://your-app.railway.app"`
   - Re-upload to Netlify

---

## 📲 Alternative: Build Real Native Apps

### For iOS (Requires Mac + Xcode)

```bash
cd money_transfer_mvp

# Install dependencies
npm install

# Add iOS platform
npx cap add ios

# Sync files
npx cap sync

# Open in Xcode
npx cap open ios

# In Xcode, click Run to install on your connected iPhone
```

### For Android (Requires Android Studio)

```bash
cd money_transfer_mvp

# Install dependencies
npm install

# Add Android platform
npx cap add android

# Sync files
npx cap sync

# Open in Android Studio
npx cap open android

# In Android Studio, click Run or Build APK
# Install APK on your Android phone
```

---

## 🔄 Quick Summary

**Easiest Path:**
1. Drag `frontend` folder to Netlify Drop
2. Get URL
3. Open on phone
4. Add to home screen
5. Done! 🎉

**For full functionality:**
1. Deploy backend to Railway
2. Update API URL in frontend
3. Re-deploy frontend
4. Access on phone

**For native apps:**
1. Run `npm install` in project folder
2. Add iOS/Android platform
3. Build in Xcode/Android Studio
4. Install on device

---

## 💡 Tips

- **The PWA (web app) works great** - you don't need a native app for testing
- **Native apps are only needed** for App Store/Play Store distribution
- **Backend deployment is crucial** - the app won't work without it
- **Free tiers available** on Netlify, Railway, Vercel, Render

---

## ❓ Troubleshooting

**"App doesn't load"**
- Check if backend is running
- Make sure API URL in `app.js` is correct

**"Can't connect to server"**
- Backend might be sleeping (free tier)
- Wait 30 seconds and retry

**"Transfers not working"**
- Backend must be deployed
- KYC must be completed in the app

---

## 🎯 Recommended Setup

1. **Frontend:** Netlify (free forever)
2. **Backend:** Railway.app (free tier available)
3. **Access:** Progressive Web App (add to home screen)
4. **Later:** Build native apps for App Store distribution

**Total Cost: $0** for testing and development!
