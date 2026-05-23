# Utilidades criptográficas usando Ed25519 + AES-128-CTR
# Ed25519: Firma digital para autenticación (Solana-compatible)
# AES-128-CTR: Encriptación simétrica para confidencialidad
# Arquitectura: Encrypt-then-Sign para máxima seguridad

from nacl.public import PrivateKey
from nacl.signing import SigningKey, VerifyKey
from nacl.utils import random
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os
import base64
import hashlib
import logging

logger = logging.getLogger(__name__)


class DataEncryptor:
    """
    Encriptador híbrido que combina:
    - AES-128-CTR para datos (simétrico, rápido)
    - Ed25519 para firmas (asimétrico, autentica)
    """
    
    def __init__(self):
        """
        Inicializa el encriptador con claves desde variables de entorno
        Requiere: ED25519_PRIVATE_KEY (64 hex) y AES_ENCRYPTION_KEY (base64)
        """
        # Cargar clave privada Ed25519 para firmar
        private_key_hex = os.environ.get('ED25519_PRIVATE_KEY')
        if not private_key_hex:
            raise ValueError("ED25519_PRIVATE_KEY no definida en variables de entorno")
        
        # Normalizar formato (quitar 0x si existe)
        if private_key_hex.startswith('0x'):
            private_key_hex = private_key_hex[2:]
        
        # Validar longitud (32 bytes = 64 caracteres hex)
        if len(private_key_hex) != 64:
            raise ValueError("ED25519_PRIVATE_KEY debe tener 64 caracteres hex")
        
        try:
            # Convertir hex a bytes y crear instancia de firma
            private_key_bytes = bytes.fromhex(private_key_hex)
            self.signing_key = SigningKey(private_key_bytes)
            self.verify_key = self.signing_key.verify_key
            
            # Cargar clave AES-128 para encriptar
            aes_key_b64 = os.environ.get('AES_ENCRYPTION_KEY')
            if not aes_key_b64:
                raise ValueError("AES_ENCRYPTION_KEY no definida en variables de entorno")
            
            self.aes_key = base64.b64decode(aes_key_b64)
            
            # Validar tamaño (128 bits = 16 bytes)
            if len(self.aes_key) != 16:
                raise ValueError("AES_ENCRYPTION_KEY debe ser de 16 bytes")
            
            # Pre-inicializar backend para mejor rendimiento
            self.backend = default_backend()
            
            logger.info("DataEncryptor inicializado correctamente con Ed25519 + AES-128-CTR")
            
        except Exception as e:
            logger.error(f"Error inicializando DataEncryptor: {e}")
            raise
    
    def encrypt(self, plaintext):
        """
        Encripta texto plano y lo firma digitalmente
        
        Proceso:
        1. Genera IV aleatorio (16 bytes)
        2. Encripta con AES-128-CTR (confidencialidad)
        3. Firma el resultado con Ed25519 (autenticidad)
        
        Args:
            plaintext: Texto a encriptar (string)
        
        Returns:
            str: Paquete en formato "IV:Ciphertext:Signature" (base64)
        
        Tiempo: <0.1ms por operación
        """
        try:
            # Paso 1: Generar IV aleatorio para AES
            # IV debe ser único por cada encriptación
            iv = random(16)
            
            # Paso 2: Encriptar con AES-128 en modo CTR
            # CTR no requiere padding y permite procesamiento paralelo
            plaintext_bytes = plaintext.encode('utf-8')
            
            cipher = Cipher(
                algorithms.AES(self.aes_key),
                modes.CTR(iv),
                backend=self.backend
            )
            encryptor = cipher.encryptor()
            ciphertext = encryptor.update(plaintext_bytes) + encryptor.finalize()
            
            # Paso 3: Firmar IV + Ciphertext con Ed25519
            # Esto garantiza integridad y autenticidad
            data_to_sign = iv + ciphertext
            signed = self.signing_key.sign(data_to_sign)
            signature = signed.signature
            
            # Paso 4: Empaquetar componentes en formato legible
            # Formato: IV:Ciphertext:Signature (cada uno en base64)
            iv_b64 = base64.b64encode(iv).decode('utf-8')
            ciphertext_b64 = base64.b64encode(ciphertext).decode('utf-8')
            signature_b64 = base64.b64encode(signature).decode('utf-8')
            
            encrypted_package = f"{iv_b64}:{ciphertext_b64}:{signature_b64}"
            
            return encrypted_package
            
        except Exception as e:
            logger.error(f"Error encriptando datos: {e}")
            raise
    
    def decrypt(self, encrypted_package):
        """
        Desencripta paquete y verifica firma digital
        
        Proceso:
        1. Separa componentes (IV, Ciphertext, Signature)
        2. Verifica firma Ed25519 (rechaza si inválida)
        3. Desencripta con AES-128-CTR
        
        Args:
            encrypted_package: Paquete encriptado "IV:Ciphertext:Signature"
        
        Returns:
            str: Texto plano original
        
        Raises:
            ValueError: Si la firma es inválida (datos comprometidos)
        
        Tiempo: <0.1ms por operación
        """
        try:
            # Paso 1: Separar componentes del paquete
            parts = encrypted_package.split(':')
            if len(parts) != 3:
                raise ValueError("Formato de paquete inválido (esperado: IV:Ciphertext:Signature)")
            
            iv_b64, ciphertext_b64, signature_b64 = parts
            
            # Decodificar desde base64 a bytes
            iv = base64.b64decode(iv_b64)
            ciphertext = base64.b64decode(ciphertext_b64)
            signature = base64.b64decode(signature_b64)
            
            # Paso 2: Verificar firma digital ANTES de desencriptar
            # Esto previene ataques de manipulación de datos
            data_signed = iv + ciphertext
            
            try:
                self.verify_key.verify(data_signed, signature)
            except Exception as e:
                logger.error(f"Firma Ed25519 inválida: {e}")
                raise ValueError("Firma criptográfica inválida - datos comprometidos o modificados")
            
            # Paso 3: Desencriptar con AES-128-CTR
            # Solo llega aquí si la firma fue válida
            cipher = Cipher(
                algorithms.AES(self.aes_key),
                modes.CTR(iv),
                backend=self.backend
            )
            decryptor = cipher.decryptor()
            plaintext_bytes = decryptor.update(ciphertext) + decryptor.finalize()
            
            return plaintext_bytes.decode('utf-8')
            
        except Exception as e:
            logger.error(f"Error desencriptando datos: {e}")
            raise
    
    def get_public_key_hex(self):
        """
        Obtiene la clave pública Ed25519 en formato hexadecimal
        Útil para compartir con otros sistemas o para auditoría
        
        Returns:
            str: Clave pública con prefijo 0x (compatible con formato Ethereum)
        """
        public_key_bytes = bytes(self.verify_key)
        return '0x' + public_key_bytes.hex()
    
    def hash_sha256(self, data):
        """
        Genera hash SHA-256 de datos (compatible con Bitcoin/Solana)
        
        Args:
            data: Datos a hashear (string o bytes)
        
        Returns:
            str: Hash SHA-256 en formato hexadecimal con prefijo 0x
        """
        if isinstance(data, str):
            data = data.encode('utf-8')
        
        hash_bytes = hashlib.sha256(data).digest()
        return '0x' + hash_bytes.hex()


def encrypt_fields(data_dict, fields_to_encrypt, encryptor):
    """
    Encripta campos específicos de un diccionario
    Útil para encriptar solo datos sensibles manteniendo metadata en claro
    
    Args:
        data_dict: Diccionario con datos
        fields_to_encrypt: Lista de nombres de campos a encriptar
        encryptor: Instancia de DataEncryptor
    
    Returns:
        dict: Nuevo diccionario con campos especificados encriptados
    
    Ejemplo:
        data = {"nombre": "Juan", "edad": 25, "voto": "A"}
        encrypted = encrypt_fields(data, ["nombre", "voto"], encryptor)
        # Resultado: {"nombre": "IV:Cipher:Sig", "edad": 25, "voto": "IV:Cipher:Sig"}
    """
    encrypted_data = data_dict.copy()
    
    for field in fields_to_encrypt:
        if field in encrypted_data and encrypted_data[field]:
            # Convertir a string y encriptar
            encrypted_data[field] = encryptor.encrypt(str(encrypted_data[field]))
    
    return encrypted_data


def decrypt_fields(data_dict, fields_to_decrypt, encryptor):
    """
    Desencripta campos específicos de un diccionario
    
    Args:
        data_dict: Diccionario con campos encriptados
        fields_to_decrypt: Lista de nombres de campos a desencriptar
        encryptor: Instancia de DataEncryptor
    
    Returns:
        dict: Nuevo diccionario con campos especificados desencriptados
    
    Raises:
        ValueError: Si algún campo tiene firma inválida
    """
    decrypted_data = data_dict.copy()
    
    for field in fields_to_decrypt:
        if field in decrypted_data and decrypted_data[field]:
            # Desencriptar y verificar firma
            decrypted_data[field] = encryptor.decrypt(decrypted_data[field])
    
    return decrypted_data


def generate_new_ed25519_keypair():
    """
    Genera un nuevo par de claves Ed25519 (Solana-compatible)
    
    IMPORTANTE: Solo usar en desarrollo/setup inicial
    En producción, usar claves previamente generadas de forma segura
    
    Returns:
        tuple: (private_key_hex, public_key_hex)
    
    Ejemplo:
        priv, pub = generate_new_ed25519_keypair()
        print(f"ED25519_PRIVATE_KEY={priv}")
        print(f"ED25519_PUBLIC_KEY={pub}")
    """
    # Genera clave privada aleatoria de 32 bytes
    signing_key = SigningKey.generate()
    
    # Obtiene bytes de clave privada y pública
    private_key_bytes = bytes(signing_key)
    public_key_bytes = bytes(signing_key.verify_key)
    
    # Convierte a hexadecimal
    private_key_hex = private_key_bytes.hex()
    public_key_hex = public_key_bytes.hex()
    
    return private_key_hex, public_key_hex
