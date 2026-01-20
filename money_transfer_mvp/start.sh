#!/bin/bash

echo "🌍 Meridian Transfer - Startup Script"
echo "======================================"

cd backend

# Check if database exists
if [ ! -f "app.db" ]; then
    echo "📊 Initializing database..."
    python3 -c "
import sqlite3
conn = sqlite3.connect('app.db')
conn.executescript(open('schema.sql').read())
conn.close()
print('✓ Database initialized')
"

    echo "👤 Creating default admin user..."
    python3 init_admin.py
fi

echo ""
echo "🚀 Starting backend server..."
echo "📍 API will be available at: http://127.0.0.1:8000"
echo "📍 API docs at: http://127.0.0.1:8000/docs"
echo ""
echo "🌐 Frontend URLs:"
echo "   User App: ../frontend/index.html"
echo "   Admin Dashboard: ../admin/index.html"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python3 main.py
