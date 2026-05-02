-- ═══════════════════════════════════════════════════════════════
-- Extended Database Schema for User, Feed, Farming & ML Features
-- ═══════════════════════════════════════════════════════════════
-- Jalankan dengan: psql -U postgres -d aquaculture_db -f migrations_add_user_features.sql

-- ── Tabel 1: User Accounts ─────────────────────────────────────
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    phone_number VARCHAR(20),
    greenhouse_location VARCHAR(255),
    address TEXT,
    profile_photo_url TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- ── Tabel 2: User Auth (Email & Password) ─────────────────────
CREATE TABLE IF NOT EXISTS user_auth (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- ── Tabel 3: Farming Cycles ───────────────────────────────────
CREATE TABLE IF NOT EXISTS farming_cycles (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    cycle_name VARCHAR(255),
    seeding_date DATE NOT NULL,
    estimated_harvest_date DATE,
    actual_harvest_date DATE,
    status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('planning', 'active', 'harvesting', 'completed')),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- ── Tabel 4: Feed Stock ────────────────────────────────────────
CREATE TABLE IF NOT EXISTS feed_stock (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    farming_cycle_id INT,
    current_quantity FLOAT NOT NULL DEFAULT 0,
    unit VARCHAR(50) DEFAULT 'kg',
    min_threshold FLOAT,
    updated_at TIMESTAMP DEFAULT NOW(),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (farming_cycle_id) REFERENCES farming_cycles(id) ON DELETE SET NULL
);

-- ── Tabel 5: Feed Transactions (Input/Usage History) ───────────
CREATE TABLE IF NOT EXISTS feed_transactions (
    id SERIAL PRIMARY KEY,
    feed_stock_id INT NOT NULL,
    transaction_type VARCHAR(20) CHECK (transaction_type IN ('input', 'usage')),
    quantity FLOAT NOT NULL,
    notes TEXT,
    previous_quantity FLOAT,
    new_quantity FLOAT,
    created_at TIMESTAMP DEFAULT NOW(),
    FOREIGN KEY (feed_stock_id) REFERENCES feed_stock(id) ON DELETE CASCADE
);

-- ── Tabel 6: Feeding Schedule ──────────────────────────────────
CREATE TABLE IF NOT EXISTS feeding_schedule (
    id SERIAL PRIMARY KEY,
    farming_cycle_id INT NOT NULL,
    scheduled_time TIME NOT NULL,
    expected_quantity FLOAT NOT NULL,
    frequency VARCHAR(20) DEFAULT 'daily',
    status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active', 'paused', 'completed')),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    FOREIGN KEY (farming_cycle_id) REFERENCES farming_cycles(id) ON DELETE CASCADE
);

-- ── Tabel 7: Feeding History ───────────────────────────────────
CREATE TABLE IF NOT EXISTS feeding_history (
    id SERIAL PRIMARY KEY,
    feeding_schedule_id INT,
    farming_cycle_id INT NOT NULL,
    actual_time TIMESTAMP NOT NULL,
    quantity_given FLOAT NOT NULL,
    administered_by VARCHAR(50) DEFAULT 'system',
    notes TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    FOREIGN KEY (feeding_schedule_id) REFERENCES feeding_schedule(id) ON DELETE SET NULL,
    FOREIGN KEY (farming_cycle_id) REFERENCES farming_cycles(id) ON DELETE CASCADE
);

-- ── Tabel 8: Sensor Calibration ────────────────────────────────
CREATE TABLE IF NOT EXISTS sensor_calibrations (
    id SERIAL PRIMARY KEY,
    farming_cycle_id INT,
    sensor_type VARCHAR(50) NOT NULL,
    calibration_date TIMESTAMP DEFAULT NOW(),
    calibration_value FLOAT,
    reference_value FLOAT,
    status VARCHAR(20) DEFAULT 'valid' CHECK (status IN ('valid', 'invalid', 'pending')),
    notes TEXT,
    FOREIGN KEY (farming_cycle_id) REFERENCES farming_cycles(id) ON DELETE SET NULL
);

-- ── Tabel 9: ML Models Metadata ────────────────────────────────
CREATE TABLE IF NOT EXISTS ml_models (
    id SERIAL PRIMARY KEY,
    model_type VARCHAR(50) NOT NULL CHECK (model_type IN ('harvest_estimation', 'feeding_decision')),
    model_version VARCHAR(50) NOT NULL,
    model_path VARCHAR(255),
    model_params JSONB,
    training_date TIMESTAMP DEFAULT NOW(),
    accuracy FLOAT,
    status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active', 'inactive', 'deprecated')),
    created_at TIMESTAMP DEFAULT NOW()
);

-- ── Tabel 10: Harvest Predictions ──────────────────────────────
CREATE TABLE IF NOT EXISTS harvest_predictions (
    id SERIAL PRIMARY KEY,
    farming_cycle_id INT NOT NULL,
    predicted_harvest_date DATE NOT NULL,
    confidence_score FLOAT,
    ml_model_id INT,
    features_used JSONB,
    prediction_date TIMESTAMP DEFAULT NOW(),
    created_at TIMESTAMP DEFAULT NOW(),
    FOREIGN KEY (farming_cycle_id) REFERENCES farming_cycles(id) ON DELETE CASCADE,
    FOREIGN KEY (ml_model_id) REFERENCES ml_models(id) ON DELETE SET NULL
);

-- ── Tabel 11: Feeding Recommendations ──────────────────────────
CREATE TABLE IF NOT EXISTS feeding_recommendations (
    id SERIAL PRIMARY KEY,
    farming_cycle_id INT NOT NULL,
    recommended_quantity FLOAT NOT NULL,
    recommended_time TIME,
    reasoning TEXT,
    confidence_score FLOAT,
    ml_model_id INT,
    features_used JSONB,
    recommendation_date TIMESTAMP DEFAULT NOW(),
    created_at TIMESTAMP DEFAULT NOW(),
    FOREIGN KEY (farming_cycle_id) REFERENCES farming_cycles(id) ON DELETE CASCADE,
    FOREIGN KEY (ml_model_id) REFERENCES ml_models(id) ON DELETE SET NULL
);

-- ── Indexes untuk Performa ─────────────────────────────────────
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_farming_cycles_user_id ON farming_cycles(user_id);
CREATE INDEX idx_farming_cycles_status ON farming_cycles(status);
CREATE INDEX idx_farming_cycles_seeding_date ON farming_cycles(seeding_date);
CREATE INDEX idx_feed_stock_user_id ON feed_stock(user_id);
CREATE INDEX idx_feed_stock_farming_cycle_id ON feed_stock(farming_cycle_id);
CREATE INDEX idx_feed_transactions_feed_stock_id ON feed_transactions(feed_stock_id);
CREATE INDEX idx_feed_transactions_created_at ON feed_transactions(created_at DESC);
CREATE INDEX idx_feeding_schedule_farming_cycle_id ON feeding_schedule(farming_cycle_id);
CREATE INDEX idx_feeding_history_farming_cycle_id ON feeding_history(farming_cycle_id);
CREATE INDEX idx_feeding_history_created_at ON feeding_history(created_at DESC);
CREATE INDEX idx_harvest_predictions_farming_cycle_id ON harvest_predictions(farming_cycle_id);
CREATE INDEX idx_harvest_predictions_created_at ON harvest_predictions(created_at DESC);
CREATE INDEX idx_feeding_recommendations_farming_cycle_id ON feeding_recommendations(farming_cycle_id);
CREATE INDEX idx_feeding_recommendations_created_at ON feeding_recommendations(created_at DESC);
CREATE INDEX idx_sensor_calibrations_farming_cycle_id ON sensor_calibrations(farming_cycle_id);
CREATE INDEX idx_ml_models_model_type ON ml_models(model_type);
