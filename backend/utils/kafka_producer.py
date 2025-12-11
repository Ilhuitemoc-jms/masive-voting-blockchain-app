# Productor de Kafka para enviar eventos de votación
from kafka import KafkaProducer
from kafka.errors import KafkaError
from django.conf import settings
import json
import logging

logger = logging.getLogger(__name__)

class VotingKafkaProducer:
    """
    Productor de Kafka que envía eventos de votación de forma asíncrona
    Implementa patrón Singleton para reutilizar la conexión
    """
    
    _instance = None
    _producer = None
    
    def __new__(cls):
        """
        Implementa Singleton para evitar múltiples conexiones
        """
        if cls._instance is None:
            cls._instance = super(VotingKafkaProducer, cls).__new__(cls)
            cls._instance._initialize_producer()
        return cls._instance
    
    def _initialize_producer(self):
        """
        Inicializa el productor de Kafka con la configuración
        """
        try:
            self._producer = KafkaProducer(
                bootstrap_servers=settings.KAFKA_CONFIG['bootstrap_servers'],
                acks=settings.KAFKA_CONFIG['acks'],
                retries=settings.KAFKA_CONFIG['retries'],
                batch_size=settings.KAFKA_CONFIG['batch_size'],
                linger_ms=settings.KAFKA_CONFIG['linger_ms'],
                buffer_memory=settings.KAFKA_CONFIG['buffer_memory'],
                compression_type=settings.KAFKA_CONFIG['compression_type'],
                request_timeout_ms=settings.KAFKA_CONFIG['request_timeout_ms'],
                value_serializer=lambda v: json.dumps(v).encode('utf-8')
            )
            logger.info("Kafka Producer inicializado correctamente")
        except Exception as e:
            logger.error(f"Error inicializando Kafka Producer: {e}")
            raise
    
    def enviar_voto(self, datos_voto):
        """
        Envía un voto a Kafka de forma asíncrona
        
        Args:
            datos_voto: Diccionario con los datos del voto (ya encriptado)
        
        Returns:
            bool: True si se envió correctamente, False si falló
        """
        try:
            # Envío asíncrono
            future = self._producer.send(
                settings.KAFKA_TOPIC,
                value=datos_voto
            )
            
            # Flush para garantizar envío rápido
            self._producer.flush(timeout=5)
            
            logger.info(f"Voto enviado a Kafka: {datos_voto.get('votante_hash', 'N/A')[:16]}")
            return True
            
        except KafkaError as e:
            logger.error(f"Error enviando voto a Kafka: {e}")
            return False
        except Exception as e:
            logger.error(f"Error inesperado en envío a Kafka: {e}")
            return False
    
    def cerrar(self):
        """
        Cierra el productor de Kafka
        """
        if self._producer:
            self._producer.close()
            logger.info("Kafka Producer cerrado")


def obtener_productor():
    """
    Obtiene la instancia Singleton del productor
    """
    return VotingKafkaProducer()
