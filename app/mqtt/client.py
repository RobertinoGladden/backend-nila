import paho.mqtt.client as mqtt
import os
from dotenv import load_dotenv

load_dotenv()

# ── Konfigurasi HiveMQ ────────────────────────────────────────
BROKER_HOST = os.getenv("MQTT_BROKER_HOST", "broker.hivemq.com")
BROKER_PORT = int(os.getenv("MQTT_BROKER_PORT", 1883))
CLIENT_ID   = os.getenv("MQTT_CLIENT_ID", "aquaculture-backend")
USERNAME    = os.getenv("MQTT_USERNAME", "")
PASSWORD    = os.getenv("MQTT_PASSWORD", "")

# ── Topics ────────────────────────────────────────────────────
TOPIC_SENSOR           = os.getenv("MQTT_TOPIC_SENSOR",           "aqua/sensor/data")
TOPIC_ACTUATOR_COMMAND = os.getenv("MQTT_TOPIC_ACTUATOR_COMMAND", "aqua/actuator/command")
TOPIC_ACTUATOR_STATUS  = os.getenv("MQTT_TOPIC_ACTUATOR_STATUS",  "aqua/actuator/status")
TOPIC_ALERT            = os.getenv("MQTT_TOPIC_ALERT",            "aqua/alert")

# Global instance
_mqtt_client: mqtt.Client = None


def get_mqtt_client() -> mqtt.Client:
    return _mqtt_client


def create_mqtt_client(on_message_callback) -> mqtt.Client:
    """
    Buat MQTT client dengan semua callback.
    on_message_callback → handler dari subscriber.py
    """
    global _mqtt_client

    client = mqtt.Client(client_id=CLIENT_ID, clean_session=True)

    # Set credentials jika pakai HiveMQ Cloud
    if USERNAME and PASSWORD:
        client.username_pw_set(USERNAME, PASSWORD)

    # ── Callbacks ─────────────────────────────────────────────
    def on_connect(client, userdata, flags, rc):
        rc_msg = {
            0: "✅ Connected",
            1: "❌ Wrong protocol version",
            2: "❌ Invalid client ID",
            3: "❌ Server unavailable",
            4: "❌ Bad username/password",
            5: "❌ Not authorized",
        }
        print(f"MQTT on_connect: {rc_msg.get(rc, f'Unknown rc={rc}')}")

        if rc == 0:
            # Subscribe semua topic yang dibutuhkan
            client.subscribe(TOPIC_SENSOR,          qos=1)
            client.subscribe(TOPIC_ACTUATOR_STATUS, qos=1)
            print(f"📡 Subscribe: {TOPIC_SENSOR}")
            print(f"📡 Subscribe: {TOPIC_ACTUATOR_STATUS}")

    def on_disconnect(client, userdata, rc):
        if rc != 0:
            print(f"⚠️  MQTT Disconnected (rc={rc}) — akan reconnect otomatis")

    def on_subscribe(client, userdata, mid, granted_qos):
        print(f"✅ Subscribe OK (mid={mid}, qos={granted_qos})")

    def on_publish(client, userdata, mid):
        print(f"📤 Publish OK (mid={mid})")

    client.on_connect    = on_connect
    client.on_disconnect = on_disconnect
    client.on_subscribe  = on_subscribe
    client.on_publish    = on_publish
    client.on_message    = on_message_callback

    # Auto reconnect: coba lagi 1s → 30s
    client.reconnect_delay_set(min_delay=1, max_delay=30)

    _mqtt_client = client
    return client


def connect_mqtt(client: mqtt.Client):
    """Connect ke HiveMQ broker dan start background loop"""
    try:
        print(f"🔌 Connecting ke MQTT Broker: {BROKER_HOST}:{BROKER_PORT}")
        client.connect(BROKER_HOST, BROKER_PORT, keepalive=60)
        client.loop_start()  # non-blocking — jalan di background thread
    except Exception as e:
        print(f"❌ Gagal connect MQTT: {e}")
        raise


def disconnect_mqtt(client: mqtt.Client):
    """Disconnect bersih saat shutdown"""
    if client:
        client.loop_stop()
        client.disconnect()
        print("🔌 MQTT Disconnected")