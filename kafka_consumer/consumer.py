# Consumer de Kafka que procesa votos y los inserta en MongoDB
import os
import time
from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable
import json
from validators import validar_estructura_voto
from db_handler import MongoDBHandler

# Configuración desde variables de entorno
KAFKA_BROKER = os.environ.get('KAFKA_BROKER', 'kafka:9092')
KAFKA_TOPIC = os.environ.get('KAFKA_TOPIC', 'voting_data_stream')

print(f"Iniciando Kafka Consumer...")
print(f"Broker: {KAFKA_BROKER}")
print(f"Topic: {KAFKA_TOPIC}")

# Inicializar componentes
db = MongoDBHandler()

# Reintentos de conexión a Kafka
max_retries = 10
retry_delay = 5

consumer = None

for attempt in range(max_retries):
    try:
        print(f"\nIntento {attempt + 1}/{max_retries} de conexión a Kafka...")
        
        # Crear consumer de Kafka
        consumer = KafkaConsumer(
            KAFKA_TOPIC,
            bootstrap_servers=[KAFKA_BROKER],
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            group_id='voting-consumer-group',
            value_deserializer=lambda x: json.loads(x.decode('utf-8')),
            max_poll_records=500,
            session_timeout_ms=30000
        )
        
        print("Kafka Consumer conectado exitosamente")
        break
        
    except NoBrokersAvailable:
        if attempt < max_retries - 1:
            print(f"Kafka no disponible. Reintentando en {retry_delay} seg...")
            time.sleep(retry_delay)
        else:
            print("No se pudo conectar a Kafka después de varios intentos")
            raise
    except Exception as e:
        print(f"Error inesperado: {e}")
        if attempt < max_retries - 1:
            time.sleep(retry_delay)
        else:
            raise

if not consumer:
    raise Exception("No se pudo inicializar el consumer de Kafka")

# Estadísticas
votos_procesados = 0
votos_invalidos = 0
start_time = time.time()

print("\n" + "-"*60)
print("Consumer iniciado. Esperando mensajes...")
print("-"*60 + "\n")

try:
    # Buffer para procesamiento en lotes
    buffer_votos = []
    BATCH_SIZE = 100
    
    for message in consumer:
        try:
            voto = message.value
            
            # Validar estructura básica del voto
            es_valido, error = validar_estructura_voto(voto)
            
            if not es_valido:
                votos_invalidos += 1
                print(f"[X] Voto invalido: {error}")
                continue
            
            # Agregar al buffer (YA VIENE ENCRIPTADO DEL BACKEND)
            buffer_votos.append(voto)
            
            # Procesar lote cuando se alcanza el tamaño
            if len(buffer_votos) >= BATCH_SIZE:
                insertados = db.insertar_lote_votos(buffer_votos)
                votos_procesados += insertados
                
                print(f"[OK] Lote insertado: {insertados} votos")
                print(f"     Total procesados: {votos_procesados}")
                
                # Limpiar buffer
                buffer_votos = []
                
                # Estadísticas cada 500 votos
                if votos_procesados % 500 == 0:
                    elapsed = time.time() - start_time
                    throughput = votos_procesados / elapsed if elapsed > 0 else 0
                    
                    print("\n" + "-"*60)
                    print("ESTADISTICAS:")
                    print(f"  Votos procesados:  {votos_procesados}")
                    print(f"  Votos invalidos:   {votos_invalidos}")
                    print(f"  Throughput:        {throughput:.2f} votos/seg")
                    print(f"  Tiempo total:      {elapsed:.2f} seg")
                    print("-"*60 + "\n")
        
        except Exception as e:
            print(f"[!] Error procesando mensaje: {e}")
            votos_invalidos += 1
            continue

except KeyboardInterrupt:
    print("\n\nInterrupcion por usuario")

except Exception as e:
    print(f"\n[X] Error critico en el consumer: {e}")
    raise

finally:
    # Procesar votos restantes en el buffer
    if buffer_votos:
        print(f"\nProcesando {len(buffer_votos)} votos pendientes...")
        insertados = db.insertar_lote_votos(buffer_votos)
        votos_procesados += insertados
        print(f"[OK] Ultimos {insertados} votos insertados")
    
    # Estadísticas finales
    elapsed = time.time() - start_time
    throughput = votos_procesados / elapsed if elapsed > 0 else 0
    
    print("\n" + "-"*60)
    print("RESUMEN FINAL:")
    print(f"  Total procesados:  {votos_procesados}")
    print(f"  Total invalidos:   {votos_invalidos}")
    print(f"  Throughput final:  {throughput:.2f} votos/seg")
    print(f"  Tiempo total:      {elapsed:.2f} seg")
    print("-"*60)
    
    if consumer:
        print("\nCerrando Kafka Consumer...")
        consumer.close()
    
    print("Consumer finalizado correctamente\n")
