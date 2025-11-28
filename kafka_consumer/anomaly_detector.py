# Detector de anomalías básico (preparado para agregar ML después)
from datetime import datetime

class AnomalyDetector:
    """
    Clase para detectar anomalías en votos
    """
    
    def __init__(self):
        """
        Inicializa el detector
        Aquí cargarías tu modelo ML cuando lo tengas
        """
        print("Detector de anomalías inicializado")
        # TODO: Cargar modelo ML
        # self.modelo = tensorflow.keras.models.load_model('modelo.h5')
    
    def detectar_duplicado(self, voto, db):
        """
        Detecta si el votante ya votó anteriormente
        
        Args:
            voto: Diccionario con datos del voto
            db: Instancia de MongoDBHandler
        
        Returns:
            bool: True si es duplicado, False si no
        """
        # Buscar votos previos del mismo votante
        duplicados = db.db.votes.count_documents({
            "votante_hash": voto['votante_hash']
        })
        
        if duplicados > 0:
            print(f"  Anomalia: Votante {voto['votante_hash'][:8]}... ya voto")
            
            # Guardar anomalía en colección separada
            db.db.anomalies.insert_one({
                "tipo": "voto_duplicado",
                "votante_hash": voto['votante_hash'],
                "voto_id": voto.get('voto_id'),
                "timestamp": datetime.utcnow()
            })
            
            return True
        
        return False
    
    def validar_voto(self, voto, db):
        """
        Valida un voto completo
        
        Args:
            voto: Diccionario con datos del voto
            db: Instancia de MongoDBHandler
        
        Returns:
            tuple: (es_valido: bool, razon: str)
        """
        # Validación 1: Duplicados
        if self.detectar_duplicado(voto, db):
            return False, "Voto duplicado detectado"
        
        return True, "Voto valido"
