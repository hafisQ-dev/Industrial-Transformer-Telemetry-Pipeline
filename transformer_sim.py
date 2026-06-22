import time
import random
import json
import paho.mqtt.client as mqtt


MQTT_BROKER = "127.0.0.1"  # KESİNLİKLE LOCALHOST OLSUN
MQTT_PORT = 1883
MQTT_TOPIC = "silo/trafo_1/telemetry"

client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)

try:
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    print("✅ Mosquitto'ya bağlantı BAŞARILI!")
    client.loop_start()
except Exception as e:
    print(f"❌ Mosquitto'ya bağlanılamadı! Docker ayakta mı? Hata: {e}")
    exit(1) # Bağlantı yoksa kodu tamamen durdur ki hatayı görelim

# Döngüyü try-except dışına alıyoruz ki bağlantı koptuğunda ne olduğunu anlayalım
while True:
    temperature_data = random.uniform(50.0, 70.0)
    
    payload = {
        "transformer_id": "TX_Silo_01",
        "temperature_celcius": round(temperature_data, 2)
    }
    
    data_message = json.dumps(payload)
    client.publish(MQTT_TOPIC, data_message)
    print(f"🚀 Veri Gönderildi: {data_message}")
    time.sleep(2)
