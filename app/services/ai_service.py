import joblib
import numpy as np
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

MODEL_PATH   = os.getenv("AI_MODEL_PATH",   "ml/models/rf_classifier.pkl")
SCALER_PATH  = os.getenv("AI_SCALER_PATH",  "ml/models/scaler.pkl")
ENCODER_PATH = os.getenv("AI_ENCODER_PATH", "ml/models/label_encoder.pkl")
MODEL_VERSION = "RF-v1"

# Cache model di memory — load sekali saat startup
_model   = None
_scaler  = None
_encoder = None

ACTIONS = {
    "Normal":  "Kondisi kolam baik. Lanjutkan monitoring rutin.",
    "Waspada": "Periksa aerator. Pertimbangkan penggantian air 20-30%.",
    "Kritis":  "SEGERA: Aktifkan aerator darurat, kurangi pakan, periksa sumber pencemaran.",
}

URGENCY = {
    "Normal":  "low",
    "Waspada": "medium",
    "Kritis":  "high",
}


def load_model() -> bool:
    """
    Load model RF dari file .pkl ke memory.
    Dipanggil sekali saat startup FastAPI.
    Return True jika berhasil, False jika gagal.
    """
    global _model, _scaler, _encoder
    try:
        _model   = joblib.load(MODEL_PATH)
        _scaler  = joblib.load(SCALER_PATH)
        _encoder = joblib.load(ENCODER_PATH)
        print(f"✅ AI Model loaded: {MODEL_PATH}")
        return True
    except FileNotFoundError as e:
        print(f"⚠️  Model tidak ditemukan: {e}")
        print("⚠️  Menggunakan rule-based fallback")
        return False
    except Exception as e:
        print(f"❌ Gagal load model: {e}")
        return False


def _rule_based_predict(
    tds: float,
    ph: float,
    do_level: float,
    temperature: float,
    turbidity: float
) -> dict:
    """
    Fallback rule-based jika model .pkl belum ada.
    Threshold berdasarkan standar budidaya ikan nila.
    """
    is_critical = (
        do_level    < 4.0  or
        temperature > 29.5 or
        ph          < 7.0  or
        ph          > 8.5  or
        turbidity   > 4.8
    )
    is_warning = (
        do_level    < 5.0  or
        temperature > 28.5 or
        ph          < 7.3  or
        ph          > 8.1  or
        turbidity   > 4.0
    )

    if is_critical:
        status = "Kritis"
    elif is_warning:
        status = "Waspada"
    else:
        status = "Normal"

    return {
        "status":      status,
        "confidence":  85.0,
        "prob_normal":  100.0 if status == "Normal"  else 0.0,
        "prob_waspada": 100.0 if status == "Waspada" else 0.0,
        "prob_kritis":  100.0 if status == "Kritis"  else 0.0,
        "urgency":     URGENCY[status],
        "action":      ACTIONS[status],
        "model_version": "rule-based-v1",
    }


def predict(
    tds: float,
    ph: float,
    do_level: float,
    temperature: float,
    turbidity: float = 0.0
) -> dict:
    """
    Fungsi utama prediksi kualitas air.
    Dipanggil dari subscriber MQTT dan router /predict.

    Return dict berisi:
        status, confidence, prob_*, urgency, action, model_version
    """
    # Gunakan rule-based jika model belum di-load
    if _model is None or _encoder is None:
        return _rule_based_predict(tds, ph, do_level, temperature, turbidity)

    try:
        now = datetime.now()

        # Susun feature vector sesuai urutan training
        # [Temperature, Dissolved_Oxygen, pH, Turbidity, Hour, DayOfWeek, Month]
        features = np.array([[
            temperature,
            do_level,
            ph,
            turbidity,
            now.hour,
            now.weekday(),
            now.month,
        ]])

        # Predict
        pred_idx = _model.predict(features)[0]
        status   = _encoder.inverse_transform([pred_idx])[0]
        proba    = _model.predict_proba(features)[0]

        # Map probabilitas ke nama kelas
        prob_map = {
            cls: round(float(p) * 100, 2)
            for cls, p in zip(_encoder.classes_, proba)
        }

        return {
            "status":       status,
            "confidence":   round(float(proba.max()) * 100, 2),
            "prob_normal":  prob_map.get("Normal",  0.0),
            "prob_waspada": prob_map.get("Waspada", 0.0),
            "prob_kritis":  prob_map.get("Kritis",  0.0),
            "urgency":      URGENCY[status],
            "action":       ACTIONS[status],
            "model_version": MODEL_VERSION,
        }

    except Exception as e:
        print(f"❌ Predict error: {e}, fallback ke rule-based")
        return _rule_based_predict(tds, ph, do_level, temperature, turbidity)