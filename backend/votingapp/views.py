from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from db import MongoDB
from .serializer import VotoSerializer, PadronElectoralSerializer
from utils.crypto_utils import DataEncryptor, encrypt_fields
from utils.kafka_producer import obtener_productor  # AGREGAR ESTA LÍNEA
from auth import generate_jwt_token, jwt_required
from datetime import datetime
import json
import hashlib
import logging

logger = logging.getLogger(__name__) #logger para kafka


# Inicializa el encriptador
encryptor = DataEncryptor()


@csrf_exempt
@require_http_methods(["POST"])
def login(request):
    """
    Autentica un usuario del padrón electoral y retorna JWT
    """
    try:
        # Parsear datos
        data = json.loads(request.body)
        
        # Validar con serializer
        serializer = PadronElectoralSerializer(data=data)
        if not serializer.is_valid():
            return JsonResponse({
                'success': False,
                'errors': serializer.errors
            }, status=400)
        
        # Buscar en MongoDB en colección de padrón electoral
        collection = MongoDB.get_collection('padron_electoral')
        usuario = collection.find_one({
            'no_cuenta': serializer.validated_data['no_cuenta'],
            'clave_elector': serializer.validated_data['clave_elector'],
            'ya_voto': False  # Verificar que no haya votado
        })
        
        if not usuario:
            return JsonResponse({
                'success': False,
                'error': 'Credenciales invalidas o ya voto'
            }, status=401)
        
        # Generar token JWT
        token = generate_jwt_token(usuario)
        
        return JsonResponse({
            'success': True,
            'token': token,
            'user_id': str(usuario['_id'])
        })
        
    except Exception as e:
        logger.error(f"Error en login: {e}")
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)

@csrf_exempt
@jwt_required
@require_http_methods(["POST"])
def crear_voto(request):
    """
    Recibe voto, encripta datos sensibles y envía a Kafka
    Retorna inmediatamente sin esperar inserción en MongoDB
    """
    try:
        # Parsear datos
        data = json.loads(request.body)
        
        # Validar con serializer
        serializer = VotoSerializer(data=data)
        if not serializer.is_valid():
            return JsonResponse({
                'success': False,
                'errors': serializer.errors
            }, status=400)
        
        validated_data = serializer.validated_data
        
        # Generar hash único del votante
        votante_hash = hashlib.sha256(
            f"{request.user_data['no_cuenta']}{datetime.utcnow().isoformat()}".encode()
        ).hexdigest()
        
        # Campos que se encriptan
        campos_sensibles = [
            'precinct_medst', 'precinct_cvr', 'district',
            'state', 'county', 'magnitude', 'party', 'party_detailed', 'candidate'
        ]
        
        # Encriptar datos sensibles
        datos_encriptados = encrypt_fields(
            validated_data,
            campos_sensibles,
            encryptor
        )
        
        # Preparar datos para Kafka (YA ENCRIPTADOS)
        datos_para_kafka = {
            **datos_encriptados,
            "user_id": str(request.user_data['user_id']),
            "votante_hash": votante_hash,
            "candidato_id": validated_data['candidato_id'],
            "timestamp": datetime.utcnow().isoformat(),
            "no_cuenta": request.user_data['no_cuenta']
        }
        
        # Obtener productor y enviar a Kafka
        productor = obtener_productor()
        
        # Envío asíncrono a Kafka
        resultado = productor.enviar_voto(datos_para_kafka)
        
        if not resultado:
            return JsonResponse({
                'success': False,
                'error': 'Error al enviar voto al sistema de procesamiento'
            }, status=500)
        
        # Marcar usuario como que ya votó
        padron_collection = MongoDB.get_collection('padron_electoral')
        padron_collection.update_one(
            {'_id': request.user_data['user_id']},
            {'$set': {'ya_voto': True}}
        )
        
        # Retorna inmediatamente (status 202 = Accepted)
        # La inserción en MongoDB ocurre en background vía Consumer
        return JsonResponse({
            'success': True,
            'votante_hash': votante_hash,
            'mensaje': 'Voto recibido y en cola de procesamiento',
            'status': 'procesando'
        }, status=202)
        
    except Exception as e:
        logger.error(f"Error en crear_voto: {e}")
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)

@jwt_required
@require_http_methods(["GET"])
def obtener_votos(request):
    """
    Retorna lista de votos (solo para administradores)
    """
    try:
        page = int(request.GET.get('page', 1))
        limit = int(request.GET.get('limit', 100))
        skip = (page - 1) * limit
        
        collection = MongoDB.get_collection('votes')
        votos = list(collection.find().skip(skip).limit(limit))
        
        # Convertir ObjectId y desencriptar (solo si es admin)
        for voto in votos:
            voto['_id'] = str(voto['_id'])
            if 'timestamp' in voto:
                if isinstance(voto['timestamp'], datetime):  # AGREGAR ESTA CONDICIÓN
                    voto['timestamp'] = voto['timestamp'].isoformat()
        
        total = collection.count_documents({})
        
        return JsonResponse({
            "success": True,
            "votos": votos,
            "total": total,
            "page": page,
            "limit": limit
        })
        
    except Exception as e:
        logger.error(f"Error en obtener_votos: {e}")  # AGREGAR ESTA LÍNEA
        return JsonResponse({
            "success": False,
            "error": str(e)
        }, status=400)

@require_http_methods(["GET"])
def estadisticas(request):
    """
    Retorna estadísticas públicas de votos por candidato
    """
    try:
        collection = MongoDB.get_collection('votes')
        
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
        
        resultados = list(collection.aggregate(pipeline))
        
        stats = []
        for r in resultados:
            stats.append({
                "candidato": r['_id'],
                "total_votos": r['total']
            })
        
        return JsonResponse({
            "success": True,
            "estadisticas": stats
        })
        
    except Exception as e:
        logger.error(f"Error en estadisticas: {e}")  # AGREGAR ESTA LÍNEA
        return JsonResponse({
            "success": False,
            "error": str(e)
        }, status=400)

@require_http_methods(["GET"])
def health_check(request):
    """
    Verifica conexión a MongoDB y Kafka
    """
    try:
        # Verificar MongoDB
        client = MongoDB.get_client()
        client.admin.command('ping')
        mongodb_status = "conectado"
        
        # Verificar Kafka
        try:
            productor = obtener_productor()
            kafka_status = "conectado" if productor._producer else "desconectado"
        except Exception as e:
            logger.warning(f"Kafka no disponible: {e}")
            kafka_status = "desconectado"
        
        return JsonResponse({
            "success": True,
            "mongodb": mongodb_status,
            "kafka": kafka_status,
            "database": MongoDB.get_database().name
        })
        
    except Exception as e:
        logger.error(f"Error en health_check: {e}")
        return JsonResponse({
            "success": False,
            "error": str(e)
        }, status=503)
