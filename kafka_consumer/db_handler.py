# Manejador de operaciones en MongoDB
from pymongo import MongoClient
from bson import ObjectId
import os
from datetime import datetime


class MongoDBHandler:
    """
    Clase que gestiona operaciones en MongoDB
    """
    
    def __init__(self):
        # Conectar a MongoDB
        try:
            client = MongoClient(
                host=os.environ.get('MONGO_HOST', 'mongodb'),
                port=int(os.environ.get('MONGO_PORT', 27017)),
                username=os.environ.get('MONGO_USER', 'root'),
                password=os.environ.get('MONGO_PASS', 'rootpassword'),
                authSource='admin',
                serverSelectionTimeoutMS=5000
            )
            
            # Verificar conexión
            client.admin.command('ping')
            
            db_name = os.environ.get('MONGO_DBNAME', 'votosdb')
            self.db = client[db_name]
            
            print(f"Conectado a MongoDB: {db_name}")
        except Exception as e:
            print(f"Error conectando a MongoDB: {e}")
            raise
    
    def actualizar_tx_hash(self, voto_id, tx_hash):
        """
        Actualiza el documento con el hash de la transacción blockchain
        """
        try:
            # Convertir voto_id a ObjectId si es string
            if isinstance(voto_id, str):
                voto_id = ObjectId(voto_id)
            
            result = self.db.votes.update_one(
                {'_id': voto_id},
                {
                    '$set': {
                        'blockchain_tx_hash': tx_hash,
                        'status': 'confirmado_blockchain',
                        'processed_at': datetime.utcnow()
                    }
                }
            )
            
            if result.modified_count == 0:
                print(f"  ⚠️  Advertencia: No se actualizó el voto {voto_id}")
        
        except Exception as e:
            print(f"Error actualizando MongoDB: {e}")
            raise
    
    def marcar_voto_invalido(self, voto_id, razon):
        """
        Marca un voto como inválido
        """
        try:
            if isinstance(voto_id, str):
                voto_id = ObjectId(voto_id)
            
            self.db.votes.update_one(
                {'_id': voto_id},
                {
                    '$set': {
                        'status': 'invalido',
                        'error_razon': razon,
                        'processed_at': datetime.utcnow()
                    }
                }
            )
        except Exception as e:
            print(f"Error marcando voto inválido: {e}")
    
    def marcar_voto_error(self, voto_id, error):
        """
        Marca un voto con error en blockchain
        """
        try:
            if isinstance(voto_id, str):
                voto_id = ObjectId(voto_id)
            
            self.db.votes.update_one(
                {'_id': voto_id},
                {
                    '$set': {
                        'status': 'error_blockchain',
                        'error': error,
                        'processed_at': datetime.utcnow()
                    }
                }
            )
        except Exception as e:
            print(f"Error marcando error de blockchain: {e}")
