# Validaciones básicas de estructura y formato
def validar_voto(voto):
    """
    Valida que el voto tenga la estructura correcta
    
    Raises:
        ValueError: Si el voto es inválido
    """
    # Campos requeridos
    campos_requeridos = ['voto_id', 'votante_hash', 'candidato_id', 'timestamp']
    
    for campo in campos_requeridos:
        if campo not in voto:
            raise ValueError(f"Campo requerido faltante: {campo}")
    
    # Validar candidato_id
    if not isinstance(voto['candidato_id'], int):
        raise ValueError("candidato_id debe ser entero")
    
    if voto['candidato_id'] < 0 or voto['candidato_id'] > 4:
        raise ValueError(f"candidato_id inválido: {voto['candidato_id']}")
    
    # Validar votante_hash
    if not isinstance(voto['votante_hash'], str):
        raise ValueError("votante_hash debe ser string")
    
    if len(voto['votante_hash']) != 64:
        raise ValueError("votante_hash debe ser string de 64 caracteres (SHA256)")
    
    # Validar timestamp
    if not isinstance(voto['timestamp'], str):
        raise ValueError("timestamp debe ser string en formato ISO 8601")
    
    return True
