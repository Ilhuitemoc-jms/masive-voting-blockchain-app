# Autenticación con JWT
import jwt
import datetime
from django.conf import settings
from django.http import JsonResponse
from functools import wraps
from db import MongoDB

# Clave secreta para firmar tokens
JWT_SECRET = settings.SECRET_KEY
JWT_ALGORITHM = 'HS256'
JWT_EXP_DELTA_SECONDS = 10  # 10 minutos - Cambiar aquí para modificar la expiración del token

def generate_jwt_token(user_data):
    """
    Genera un token JWT para un usuario autenticado
    """
    payload = {
        'user_id': str(user_data['_id']),
        'no_cuenta': user_data['no_cuenta'],
        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=JWT_EXP_DELTA_SECONDS),
        'iat': datetime.datetime.utcnow()
    }
    
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token


def verify_jwt_token(token):
    """
    Verifica y decodifica un token JWT
    """
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def jwt_required(view_func):
    """
    Decorador para proteger vistas que requieren autenticación
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # Obtiene el token del header Authorization
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        
        if not auth_header.startswith('Bearer '):
            return JsonResponse({
                'success': False,
                'error': 'Token no proporcionado'
            }, status=401)
        
        token = auth_header.split(' ')[1]
        
        # Verifica el token
        payload = verify_jwt_token(token)
        
        if not payload:
            return JsonResponse({
                'success': False,
                'error': 'Token inválido o expirado'
            }, status=401)
        
        # Agrega los datos del usuario al request
        request.user_data = payload
        
        return view_func(request, *args, **kwargs)
    
    return wrapper
