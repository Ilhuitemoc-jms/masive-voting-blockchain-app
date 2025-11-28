# Loop principal del Kafka Consumer
import os
import time
from kafka import KafkaConsumer
import json
from validators import validar_voto
from anomaly_detector import AnomalyDetector
from blockchain_integrator import BlockchainIntegrator
from db_handler import MongoDBHandler


# Configuración desde variables de entorno
KAFKA_BROKER = os.environ.get('KAFKA_BROKER', 'kafka:9092')
KAFKA_TOPIC = os.environ.get('KAFKA_TOPIC', 'votos_pendientes')

print(f"Iniciando Kafka Consumer...")
print(f"Conectando a Kafka: {KAFKA_BROKER}")
print(f"Topic: {KAFKA_TOPIC}")

# Esperar a que Kafka esté disponible
time.sleep(10)

# Inicializar componentes
detector_anomalias = AnomalyDetector()
blockchain = BlockchainIntegrator()
db = MongoDBHandler()

try:
    consumer = KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=[KAFKA_BROKER],
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='voting-consumer-group',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )
    
    print("Kafka Consumer conectado exitosamente")
    print("Esperando mensajes...\n")
    
    votos_procesados = 0
    anomalias_detectadas = 0
    start_time = time.time()
    
    for message in consumer:
        voto = message.value
        votos_procesados += 1
        
        print(f"\n[{votos_procesados}] Voto recibido: {voto.get('voto_id', 'ID no disponible')}")
        
        # Validación básica de estructura
        try:
            validar_voto(voto)
            print("  Validación básica: OK")
        except ValueError as e:
            print(f"  Validación fallida: {e}")
            db.marcar_voto_invalido(voto['voto_id'], str(e))
            continue
        
        # Detección de anomalías
        es_valido, razon = detector_anomalias.validar_voto(voto, db)
        
        if not es_valido:
            anomalias_detectadas += 1
            print(f"  ANOMALIA: {razon}")
            db.marcar_voto_rechazado(voto['voto_id'], razon)
            continue
        
        print("  Sin anomalías detectadas")

        # Enviar a Blockchain
        try:
            tx_hash = blockchain.enviar_voto(
                votante_hash=voto['votante_hash'],
                candidato_id=voto['candidato_id']
            )
            
            print(f"  Blockchain TX: {tx_hash[:16]}...")
            
            db.actualizar_tx_hash(voto['voto_id'], tx_hash)
            print(f"  Voto procesado exitosamente")
            
        except Exception as e:
            print(f"  Error enviando a blockchain: {e}")
            db.marcar_voto_error(voto['voto_id'], str(e))
            continue
        
        # Estadísticas cada 100 votos
        if votos_procesados % 100 == 0:
            elapsed = time.time() - start_time
            throughput = votos_procesados / elapsed if elapsed > 0 else 0
            tasa_anomalias = (anomalias_detectadas / votos_procesados) * 100
            print(f"\nESTADISTICAS:")
            print(f"   Total procesados: {votos_procesados}")
            print(f"   Anomalías detectadas: {anomalias_detectadas} ({tasa_anomalias:.2f}%)")
            print(f"   Throughput: {throughput:.2f} votos/seg")
            print(f"   Tiempo transcurrido: {elapsed:.2f} seg\n")

except Exception as e:
    print(f"\nError crítico en el consumer: {e}")
    raise

finally:
    print("\nCerrando Kafka Consumer...")
    consumer.close()
