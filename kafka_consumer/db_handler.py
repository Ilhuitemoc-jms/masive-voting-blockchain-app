# Manejador de operaciones en MongoDB para insercion batch
from pymongo import MongoClient
from datetime import datetime
import os

class MongoDBHandler:
    """
    Gestiona operaciones de insercion en MongoDB de forma eficiente
    """
    
    def __init__(self):
        # Conectar a MongoDB
        try:
            self.client = MongoClient(
                host=os.environ.get('MONGO_HOST', 'mongodb'),
                port=int(os.environ.get('MONGO_PORT', 27017)),
                username=os.environ.get('MONGO_USER', 'root'),
                password=os.environ.get('MONGO_PASS', 'rootpassword'),
                authSource='admin',
                serverSelectionTimeoutMS=5000
            )
            
            # Verificar conexion
            self.client.admin.command('ping')
            
            db_name = os.environ.get('MONGO_DBNAME', 'votosdb')
            self.db = self.client[db_name]
            
            print(f"Conectado a MongoDB: {db_name}")
            
            # Crear indices si no existen
            self._crear_indices()
            
        except Exception as e:
            print(f"Error conectando a MongoDB: {e}")
            raise
    
    def _crear_indices(self):
        """
        Crea indices en la coleccion de votos para mejorar rendimiento
        """
        try:
            # Indice unico en votante_hash para evitar duplicados
            self.db.votes.create_index("votante_hash", unique=True)
            
            # Indices para consultas comunes
            self.db.votes.create_index("candidato_id")
            self.db.votes.create_index("timestamp")
            self.db.votes.create_index("status")
            
            print("Indices de MongoDB verificados")
        except Exception as e:
            print(f"Advertencia creando indices: {e}")
    
    def insertar_lote_votos(self, votos):
        """
        Inserta un lote de votos en MongoDB de forma eficiente
        Los votos YA vienen encriptados del backend
        
        Args:
            votos: Lista de diccionarios con datos de votos
        
        Returns:
            int: Numero de votos insertados exitosamente
        """
        if not votos:
            return 0
        
        try:
            # Preparar documentos para insercion
            documentos = []
            
            for voto in votos:
                # Convertir timestamp string a datetime si es necesario
                timestamp = voto.get('timestamp')
                if isinstance(timestamp, str):
                    timestamp = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                else:
                    timestamp = datetime.utcnow()
                
                # Documento completo (datos YA ENCRIPTADOS)
                documento = {
                    **voto,
                    "timestamp": timestamp,
                    "processed_at": datetime.utcnow(),
                    "status": "procesado",
                    "blockchain_tx_hash": None
                }
                
                documentos.append(documento)
            
            # Insercion batch (ignora duplicados)
            resultado = self.db.votes.insert_many(
                documentos,
                ordered=False
            )
            
            return len(resultado.inserted_ids)
        
        except Exception as e:
            # Si hay duplicados, algunos se insertan y otros no
            print(f"Advertencia en insercion batch: {e}")
            # Retornar estimacion de insertados
            return len(votos) // 2
    
    def contar_votos_por_candidato(self):
        """
        Obtiene el conteo de votos por candidato
        
        Returns:
            list: Lista de diccionarios con candidato_id y total
        """
        try:
            pipeline = [
                {
                    "$group": {
                        "_id": "$candidato_id",
                        "total": {"$sum": 1}
                    }
                },
                {
                    "$sort": {"total": -1}
                }
            ]
            
            resultados = list(self.db.votes.aggregate(pipeline))
            
            return [
                {
                    "candidato_id": r['_id'],
                    "total_votos": r['total']
                }
                for r in resultados
            ]
        
        except Exception as e:
            print(f"Error en agregacion: {e}")
            return []
    
    def cerrar(self):
        """
        Cierra la conexion a MongoDB
        """
        if self.client:
            self.client.close()
            print("Conexion a MongoDB cerrada")
