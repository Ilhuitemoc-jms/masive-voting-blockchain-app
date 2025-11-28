# Módulo que gestiona la conexión a MongoDB
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import os

class MongoDB:
    """
    Clase Singleton para gestionar conexión única a MongoDB
    """
    _client = None
    _db = None

    @classmethod
    def get_client(cls):
        """
        Retorna el cliente de MongoDB (singleton)
        """
        if cls._client is None:
            try:
                cls._client = MongoClient(
                    host=os.environ.get('MONGO_HOST', 'mongodb'),
                    port=int(os.environ.get('MONGO_PORT', 27017)),
                    username=os.environ.get('MONGO_USER', 'root'),
                    password=os.environ.get('MONGO_PASS', 'rootpassword'),
                    authSource='admin',
                    serverSelectionTimeoutMS=5000
                )
                # Verificar conexión
                cls._client.admin.command('ping')
                print("Conexión a MongoDB exitosa")
            except ConnectionFailure as e:
                print(f"Error conectando a MongoDB: {e}")
                raise
        return cls._client

    @classmethod
    def get_database(cls):
        """
        Retorna la base de datos configurada
        """
        if cls._db is None:
            client = cls.get_client()
            db_name = os.environ.get('MONGO_DBNAME', 'votosdb')
            cls._db = client[db_name]
        return cls._db

    @classmethod
    def get_collection(cls, collection_name):
        """
        Retorna una colección específica
        """
        db = cls.get_database()
        return db[collection_name]
