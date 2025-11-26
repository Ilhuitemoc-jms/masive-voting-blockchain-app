import os
import time
from kafka import KafkaConsumer
import json

# Configuración desde variables de entorno
KAFKA_BROKER = os.environ.get('KAFKA_BROKER', 'kafka:9092')
KAFKA_TOPIC = os.environ.get('KAFKA_TOPIC', 'votos_pendientes')

print(f"🔄 Iniciando Kafka Consumer...")
print(f"📡 Conectando a Kafka: {KAFKA_BROKER}")
print(f"📬 Escuchando topic: {KAFKA_TOPIC}")

# Esperar a que Kafka esté disponible
time.sleep(10)

try:
    consumer = KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=[KAFKA_BROKER],
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='voting-consumer-group',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )
    
    print("✅ Kafka Consumer conectado exitosamente")
    print("👂 Esperando mensajes...")
    
    for message in consumer:
        voto = message.value
        print(f"📥 Voto recibido: {voto}")
        
        # TODO: Aquí irá la lógica de:
        # 1. Validación
        # 2. Detección de anomalías
        # 3. Guardar en MongoDB
        # 4. Enviar a Ganache
        
except Exception as e:
    print(f"❌ Error en el consumer: {e}")
