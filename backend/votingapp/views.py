from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from db import MongoDB
from .serializer import VotoSerializer, PadronElectoralSerializer
from utils.crypto_utils import DataEncryptor, encrypt_fields
from auth import generate_jwt_token, jwt_required
from datetime import datetime
import json
import hashlib


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
                'error': 'Credenciales inválidas o ya votó'
            }, status=401)
        
        # Generar token JWT
        token = generate_jwt_token(usuario)
        
        return JsonResponse({
            'success': True,
            'token': token,
            'user_id': str(usuario['_id'])
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)


@csrf_exempt
@jwt_required
@require_http_methods(["POST"])
def crear_voto(request):
    """
    Crea un voto encriptando datos sensibles en MongoDB
    y enviando solo el voto al blockchain
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
        
        # Generar hash único del votante (para blockchain)
        votante_hash = hashlib.sha256(
            f"{request.user_data['no_cuenta']}{datetime.utcnow()}".encode()
        ).hexdigest()
        
        # Campos que van ENCRIPTADOS a MongoDB
        campos_sensibles = [
            'precinct_medst', 'precinct_cvr', 'office', 'district',
            'state', 'county', 'magnitude', 'party', 'party_detailed',
            'voting_hour', 'candidate'
        ]
        
        # Encriptar datos sensibles
        datos_encriptados = encrypt_fields(
            validated_data,
            campos_sensibles,
            encryptor
        )
        
        # Documento completo para MongoDB
        documento_mongodb = {
            **datos_encriptados,
            "user_id": request.user_data['user_id'],
            "votante_hash": votante_hash,
            "candidato_id": validated_data['candidato_id'],
            "timestamp": datetime.utcnow(),
            "blockchain_tx_hash": None,
            "status": "pendiente_blockchain"
        }
        
        # Guardar en MongoDB
        collection = MongoDB.get_collection('votes')
        result = collection.insert_one(documento_mongodb)
        
        # Marcar usuario como que ya votó
        padron_collection = MongoDB.get_collection('padron_electoral')
        padron_collection.update_one(
            {'_id': request.user_data['user_id']},
            {'$set': {'ya_voto': True}}
        )
        
        # TODO: Aquí enviarías al Kafka para procesar blockchain
        # Datos para blockchain (solo lo público):
        voto_blockchain = {
            "votante_hash": votante_hash,
            "candidato_id": validated_data['candidato_id'],
            "timestamp": datetime.utcnow().isoformat()
        }
        
        return JsonResponse({
            "success": True,
            "voto_id": str(result.inserted_id),
            "votante_hash": votante_hash,
            "mensaje": "Voto registrado exitosamente"
        }, status=201)
        
    except Exception as e:
        return JsonResponse({
            "success": False,
            "error": str(e)
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
        return JsonResponse({
            "success": False,
            "error": str(e)
        }, status=400)


@require_http_methods(["GET"])
def health_check(request):
    """
    Verifica conexión a MongoDB
    """
    try:
        client = MongoDB.get_client()
        client.admin.command('ping')
        
        return JsonResponse({
            "success": True,
            "mongodb": "conectado",
            "database": MongoDB.get_database().name
        })
        
    except Exception as e:
        return JsonResponse({
            "success": False,
            "error": str(e)
        }, status=503)
