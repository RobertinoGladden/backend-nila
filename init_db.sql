-- ═══════════════════════════════════════════════════════════════
-- Jalankan dengan:
-- psql -U postgres -f init_db.sql
-- ═══════════════════════════════════════════════════════════════

-- Buat database
CREATE DATABASE aquaculture_db;
\c aquaculture_db;

-- ── Tabel 1: Data mentah sensor ───────────────────────────────
CREATE TABLE sensor_data (
    id          SERIAL PRIMARY KEY,
    device_id   VARCHAR(50)  DEFAULT 'sensor-01',
    tds         FLOAT        NOT NULL,
    ph          FLOAT        NOT NULL,
    do_level    FLOAT        NOT NULL,
    temperature FLOAT        NOT NULL,
    turbidity   FLOAT        NOT NULL DEFAULT 0,
    created_at  TIMESTAMP    DEFAULT NOW()
);

-- ── Tabel 2: Hasil prediksi AI ────────────────────────────────
CREATE TABLE predictions (
    id              SERIAL PRIMARY KEY,
    sensor_data_id  INT          REFERENCES sensor_data(id) ON DELETE CASCADE,
    status          VARCHAR(10)  NOT NULL CHECK (status IN ('Normal','Waspada','Kritis')),
    confidence      FLOAT        NOT NULL,
    prob_normal     FLOAT        DEFAULT 0,
    prob_waspada    FLOAT        DEFAULT 0,
    prob_kritis     FLOAT        DEFAULT 0,
    urgency         VARCHAR(10)  DEFAULT 'low',
    model_version   VARCHAR(20)  DEFAULT 'RF-v1',
    created_at      TIMESTAMP    DEFAULT NOW()
);

-- ── Tabel 3: Alert ────────────────────────────────────────────
CREATE TABLE alerts (
    id              SERIAL PRIMARY KEY,
    sensor_data_id  INT          REFERENCES sensor_data(id) ON DELETE CASCADE,
    prediction_id   INT          REFERENCES predictions(id) ON DELETE SET NULL,
    level           VARCHAR(10)  NOT NULL CHECK (level IN ('Waspada','Kritis')),
    message         TEXT         NOT NULL,
    action          TEXT,
    status          VARCHAR(10)  DEFAULT 'active' CHECK (status IN ('active','resolved')),
    created_at      TIMESTAMP    DEFAULT NOW(),
    resolved_at     TIMESTAMP
);

-- ── Tabel 4: Notifikasi untuk Flutter ────────────────────────
CREATE TABLE notifications (
    id          SERIAL PRIMARY KEY,
    alert_id    INT          REFERENCES alerts(id) ON DELETE CASCADE,
    title       VARCHAR(100) NOT NULL,
    message     TEXT         NOT NULL,
    is_read     BOOLEAN      DEFAULT FALSE,
    created_at  TIMESTAMP    DEFAULT NOW()
);

-- ── Tabel 5: Status aktuator real-time ───────────────────────
CREATE TABLE actuator_status (
    id          SERIAL PRIMARY KEY,
    device_name VARCHAR(50)  UNIQUE NOT NULL,
    is_active   BOOLEAN      DEFAULT FALSE,
    mode        VARCHAR(10)  DEFAULT 'auto' CHECK (mode IN ('manual','auto')),
    updated_at  TIMESTAMP    DEFAULT NOW()
);

-- ── Tabel 6: Log history aktuator ────────────────────────────
CREATE TABLE actuator_logs (
    id           SERIAL PRIMARY KEY,
    device_name  VARCHAR(50)  NOT NULL,
    action       VARCHAR(10)  NOT NULL CHECK (action IN ('on','off')),
    triggered_by VARCHAR(20)  DEFAULT 'manual' CHECK (triggered_by IN ('manual','ai','schedule')),
    alert_id     INT          REFERENCES alerts(id) ON DELETE SET NULL,
    created_at   TIMESTAMP    DEFAULT NOW()
);

-- ── Data awal aktuator ────────────────────────────────────────
INSERT INTO actuator_status (device_name, is_active, mode) VALUES
    ('aerator', FALSE, 'auto'),
    ('heater',  FALSE, 'auto'),
    ('pompa',   FALSE, 'auto');

-- ── Index untuk performa query ────────────────────────────────
CREATE INDEX idx_sensor_created   ON sensor_data(created_at DESC);
CREATE INDEX idx_pred_sensor      ON predictions(sensor_data_id);
CREATE INDEX idx_pred_created     ON predictions(created_at DESC);
CREATE INDEX idx_alert_status     ON alerts(status) WHERE status = 'active';
CREATE INDEX idx_notif_read       ON notifications(is_read) WHERE is_read = FALSE;
CREATE INDEX idx_actuator_log_dev ON actuator_logs(device_name, created_at DESC);