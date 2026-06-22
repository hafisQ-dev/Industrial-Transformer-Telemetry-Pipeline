import paho.mqtt.client as mqtt
import json
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import os
from dotenv import load_dotenv

load_dotenv()

MQTT_BROKER="127.0.0.1"
MQTT_PORT=1883
MQTT_TOPIC="silo/trafo_1/telemetry"

INFLUX_URL="http://localhost:8086"
INFLUX_TOKEN=os.getenv("INFLUXDB_TOKEN")
INFLUX_ORG=os.getenv("INFLUXDB_ORG_NAME")
INFLUX_BUCKET=os.getenv("INFLUXDB_NAME")

influx_client=InfluxDBClient(
   url=INFLUX_URL,
   token=INFLUX_TOKEN,
   org=INFLUX_ORG
)
write_api=influx_client.write_api(write_options=SYNCHRONOUS)

def on_message(client, userdata, message):
    try:
        # 1. Ham byte verisini string'e çevir
        msg_payload = message.payload.decode("utf-8")
        print(f"📩 Mosquitto'dan mesaj yakalandı: {msg_payload}")
        
        # 2. String formatındaki JSON'ı Python sözlüğüne dönüştür
        data = json.loads(msg_payload)
        
        # 3. InfluxDB Veri Noktasını (Point) Oluştur
        point = Point("transformer_telemetry") \
            .tag("transformer_id", data["transformer_id"]) \
            .field("temperature", float(data["temperature_celcius"]))
        
        # 4. Veriyi InfluxDB Bucket'ına Yaz
        write_api.write(bucket=INFLUX_BUCKET, org=INFLUX_ORG, record=point)
        print("💾 Veri başarıyla InfluxDB'ye kaydedildi!")
        
    except Exception as e:
        print(f"❌ Veri işlenirken veya yazılırken hata oluştu: {e}")


mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_message = on_message
mqttc.connect(MQTT_BROKER, MQTT_PORT, 60)
mqttc.subscribe(MQTT_TOPIC)
print(f"📡 Köprü başlatıldı. {MQTT_TOPIC} kanalı dinleniyor...")
mqttc.loop_forever()
