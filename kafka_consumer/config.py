# Configuración centralizada del consumer
import os

class ConsumerConfig:
    """
    Configuración del Kafka Consumer
    """
    # Kafka
    KAFKA_BROKER = os.environ.get('KAFKA_BROKER', 'kafka:9092')
    KAFKA_TOPIC = os.environ.get('KAFKA_TOPIC', 'voting_data_stream')
    KAFKA_GROUP_ID = 'voting-consumer-group'
    
    # MongoDB
    MONGO_HOST = os.environ.get('MONGO_HOST', 'mongodb')
    MONGO_PORT = int(os.environ.get('MONGO_PORT', 27017))
    MONGO_USER = os.environ.get('MONGO_USER', 'root')
    MONGO_PASS = os.environ.get('MONGO_PASS', 'rootpassword')
    MONGO_DBNAME = os.environ.get('MONGO_DBNAME', 'votosdb')
    
    # Procesamiento
    BATCH_SIZE = 100
    MAX_POLL_RECORDS = 500
    
    # Campos sensibles a encriptar
    CAMPOS_SENSIBLES = [
        'precinct_medst', 'precinct_cvr', 'office', 'district',
        'state', 'county', 'magnitude', 'party', 'party_detailed',
        'voting_hour', 'candidate'
    ]
