#!/usr/bin/env python3
"""
Initialize database with default admin user
Run this script once to create the first admin account
"""

import sqlite3

DB = "app.db"

def init_admin():
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    # Create default admin
    admin_email = "admin@meridian.com"
    admin_password = "admin123"  # CHANGE THIS IN PRODUCTION!
    admin_name = "System Admin"

    try:
        cursor.execute(
            "INSERT INTO admin_users (email, name, password, role) VALUES (?, ?, ?, ?)",
            (admin_email, admin_name, admin_password, "SUPER_ADMIN")
        )
        conn.commit()
        print(f"✓ Admin user created successfully!")
        print(f"  Email: {admin_email}")
        print(f"  Password: {admin_password}")
        print(f"\n⚠️  IMPORTANT: Change the default password immediately!")
    except sqlite3.IntegrityError:
        print("Admin user already exists!")

    conn.close()

if __name__ == "__main__":
    init_admin()
