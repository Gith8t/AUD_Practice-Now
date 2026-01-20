-- Enhanced schema for money transfer MVP with KYC, limits, fees, and education tracking

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    password TEXT NOT NULL,
    phone TEXT,
    address TEXT,
    city TEXT,
    state TEXT DEFAULT 'Minnesota',
    zip_code TEXT,
    country TEXT DEFAULT 'USA',
    date_of_birth TEXT,
    kyc_status TEXT DEFAULT 'NONE', -- NONE, PENDING, VERIFIED, REJECTED
    kyc_tier INTEGER DEFAULT 0, -- 0=unverified, 1=basic, 2=full
    kyc_submitted_at DATETIME,
    kyc_verified_at DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS kyc_documents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    document_type TEXT NOT NULL, -- ID, PASSPORT, DRIVERS_LICENSE, PROOF_OF_ADDRESS
    document_number TEXT,
    file_path TEXT,
    status TEXT DEFAULT 'PENDING', -- PENDING, APPROVED, REJECTED
    rejection_reason TEXT,
    uploaded_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    reviewed_at DATETIME,
    reviewed_by INTEGER,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS sessions (
    token TEXT PRIMARY KEY,
    user_id INTEGER,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS recipients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    phone TEXT NOT NULL,
    country TEXT NOT NULL,
    mobile_money_provider TEXT, -- MTN, ORANGE, AIRTEL, VODAFONE
    mobile_money_number TEXT NOT NULL,
    account_name TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS transfers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    recipient_id INTEGER NOT NULL,
    send_amount REAL NOT NULL,
    send_currency TEXT DEFAULT 'USD',
    receive_amount REAL NOT NULL,
    receive_currency TEXT NOT NULL,
    exchange_rate REAL NOT NULL,
    fee_amount REAL NOT NULL,
    spread_amount REAL NOT NULL,
    education_contribution REAL NOT NULL, -- 2% of revenue
    total_cost REAL NOT NULL, -- send_amount + fee_amount
    status TEXT DEFAULT 'PENDING', -- PENDING, PROCESSING, COMPLETED, FAILED, CANCELLED
    mobile_money_transaction_id TEXT,
    failure_reason TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    completed_at DATETIME,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (recipient_id) REFERENCES recipients(id)
);

CREATE TABLE IF NOT EXISTS education_fund (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    transfer_id INTEGER NOT NULL,
    country TEXT NOT NULL,
    amount_usd REAL NOT NULL,
    allocated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    disbursed BOOLEAN DEFAULT 0,
    disbursed_at DATETIME,
    project_name TEXT,
    FOREIGN KEY (transfer_id) REFERENCES transfers(id)
);

CREATE TABLE IF NOT EXISTS exchange_rates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    from_currency TEXT NOT NULL,
    to_currency TEXT NOT NULL,
    base_rate REAL NOT NULL,
    spread_percentage REAL DEFAULT 2.5, -- Our markup
    effective_rate REAL NOT NULL,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS transaction_limits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    kyc_tier INTEGER NOT NULL,
    daily_limit REAL NOT NULL,
    monthly_limit REAL NOT NULL,
    per_transaction_limit REAL NOT NULL,
    description TEXT
);

CREATE TABLE IF NOT EXISTS country_settings (
    country_code TEXT PRIMARY KEY,
    country_name TEXT NOT NULL,
    supported BOOLEAN DEFAULT 1,
    mobile_money_providers TEXT, -- JSON array
    education_partner TEXT,
    flag_emoji TEXT
);

CREATE TABLE IF NOT EXISTS admin_users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    password TEXT NOT NULL,
    role TEXT DEFAULT 'ADMIN', -- ADMIN, SUPER_ADMIN
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Insert default transaction limits
INSERT OR IGNORE INTO transaction_limits (kyc_tier, daily_limit, monthly_limit, per_transaction_limit, description) VALUES
(0, 0, 0, 0, 'Unverified - No transfers allowed'),
(1, 500, 2000, 500, 'Basic KYC - Limited transfers'),
(2, 5000, 20000, 3000, 'Full KYC - Standard limits');

-- Insert default exchange rates (West African countries)
INSERT OR IGNORE INTO exchange_rates (from_currency, to_currency, base_rate, spread_percentage, effective_rate) VALUES
('USD', 'LRD', 190.00, 2.5, 194.75),  -- Liberia Dollar
('USD', 'GHS', 12.50, 2.5, 12.81),    -- Ghana Cedi
('USD', 'NGN', 1500.00, 2.5, 1537.50), -- Nigerian Naira
('USD', 'XOF', 600.00, 2.5, 615.00),   -- West African CFA Franc (used in multiple countries)
('USD', 'SLL', 22000.00, 2.5, 22550.00); -- Sierra Leone Leone

-- Insert country settings
INSERT OR IGNORE INTO country_settings (country_code, country_name, mobile_money_providers, education_partner, flag_emoji) VALUES
('LR', 'Liberia', '["MTN", "Orange", "Lonestar"]', 'Liberia Education Fund', '🇱🇷'),
('GH', 'Ghana', '["MTN", "Vodafone", "AirtelTigo"]', 'Ghana Schools Initiative', '🇬🇭'),
('NG', 'Nigeria', '["MTN", "Airtel", "Glo", "9mobile"]', 'Nigeria Education Trust', '🇳🇬'),
('SN', 'Senegal', '["Orange", "Free", "Expresso"]', 'Senegal Learning Centers', '🇸🇳'),
('SL', 'Sierra Leone', '["Orange", "Africell", "Qcell"]', 'Sierra Leone School Support', '🇸🇱'),
('CI', 'Côte d''Ivoire', '["MTN", "Orange", "Moov"]', 'Ivory Coast Education Fund', '🇨🇮');

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_transfers_user_id ON transfers(user_id);
CREATE INDEX IF NOT EXISTS idx_transfers_status ON transfers(status);
CREATE INDEX IF NOT EXISTS idx_transfers_created_at ON transfers(created_at);
CREATE INDEX IF NOT EXISTS idx_recipients_user_id ON recipients(user_id);
CREATE INDEX IF NOT EXISTS idx_education_fund_country ON education_fund(country);
CREATE INDEX IF NOT EXISTS idx_kyc_documents_user_id ON kyc_documents(user_id);
