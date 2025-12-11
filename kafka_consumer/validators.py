# Validadores de estructura de datos de votos
from datetime import datetime

def validar_estructura_voto(voto):
    """
    Valida que el voto tenga la estructura correcta y campos requeridos
    No desencripta, solo verifica que los campos existan
    
    Args:
        voto: Diccionario con datos del voto
    
    Returns:
        tuple: (es_valido: bool, mensaje_error: str)
    """
    # Campos obligatorios
    campos_requeridos = [
        'votante_hash',
        'candidato_id',
        'timestamp',
        'user_id'
    ]
    
    # Verificar campos requeridos
    for campo in campos_requeridos:
        if campo not in voto:
            return False, f"Campo requerido faltante: {campo}"
        
        if voto[campo] is None or voto[campo] == '':
            return False, f"Campo requerido vacio: {campo}"
    
    # Validar tipo de candidato_id
    try:
        candidato_id = int(voto['candidato_id'])
        if candidato_id < 0:
            return False, "candidato_id debe ser un numero positivo"
    except (ValueError, TypeError):
        return False, "candidato_id debe ser un numero entero"
    
    # Validar longitud de votante_hash (debe ser SHA256 = 64 caracteres hex)
    if len(voto['votante_hash']) != 64:
        return False, "votante_hash debe tener 64 caracteres (SHA256)"
    
    # Validar que timestamp sea valido
    try:
        if isinstance(voto['timestamp'], str):
            datetime.fromisoformat(voto['timestamp'].replace('Z', '+00:00'))
    except (ValueError, AttributeError):
        return False, "timestamp invalido"
    
    return True, "OK"


def validar_candidato(candidato_id, max_candidatos=10):
    """
    Valida que el candidato exista en el rango permitido
    
    Args:
        candidato_id: ID del candidato
        max_candidatos: Numero maximo de candidatos permitidos
    
    Returns:
        bool: True si es valido, False si no
    """
    try:
        candidato = int(candidato_id)
        return 0 <= candidato < max_candidatos
    except (ValueError, TypeError):
        return False
