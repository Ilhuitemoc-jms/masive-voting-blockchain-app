# Utilidades criptográficas usando Ed25519 + AES-128-GCM
# Ed25519: Firma digital para autenticación (Solana-compatible)
# AES-128-GCM: Encriptación AEAD (confidencialidad + integridad integrada)
# Arquitectura: Encrypt-then-Sign para máxima seguridad

from nacl.signing import SigningKey, VerifyKey
from nacl.utils import random
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.exceptions import InvalidTag
import os
import base64
import logging

logger = logging.getLogger(__name__)


class DataEncryptor:
    """
    Encriptador hibrido que combina:
    - AES-128-GCM para datos (AEAD: confidencialidad + integridad en una sola operacion)
    - Ed25519 para firmas (asimetrico, no repudio verificable publicamente)
    """

    def __init__(self):
        """
        Inicializa el encriptador con claves desde variables de entorno.
        Requiere: ED25519_PRIVATE_KEY (64 hex) y AES_ENCRYPTION_KEY (base64)
        """
        # Carga la clave privada Ed25519 para firmar desde variables de entorno
        private_key_hex = os.environ.get('ED25519_PRIVATE_KEY')
        if not private_key_hex:
            raise ValueError("ED25519_PRIVATE_KEY no definida en variables de entorno")

        # Elimina prefijo 0x si existe para normalizar el formato
        if private_key_hex.startswith('0x'):
            private_key_hex = private_key_hex[2:]

        # Valida que la longitud sea exactamente 32 bytes (64 caracteres hex)
        if len(private_key_hex) != 64:
            raise ValueError("ED25519_PRIVATE_KEY debe tener 64 caracteres hex")

        try:
            # Convierte hex a bytes y crea la instancia de firma Ed25519
            private_key_bytes = bytes.fromhex(private_key_hex)
            self.signing_key = SigningKey(private_key_bytes)
            self.verify_key = self.signing_key.verify_key

            # Carga la clave AES-128 para encriptar desde variables de entorno
            aes_key_b64 = os.environ.get('AES_ENCRYPTION_KEY')
            if not aes_key_b64:
                raise ValueError("AES_ENCRYPTION_KEY no definida en variables de entorno")

            self.aes_key = base64.b64decode(aes_key_b64)

            # Valida que la clave AES sea exactamente 16 bytes (128 bits)
            if len(self.aes_key) != 16:
                raise ValueError("AES_ENCRYPTION_KEY debe ser de 16 bytes")

            logger.info("DataEncryptor inicializado correctamente con Ed25519 + AES-128-GCM")

        except Exception as e:
            logger.error(f"Error inicializando DataEncryptor: {e}")
            raise

    def encrypt(self, plaintext):
        """
        Encripta texto plano y lo firma digitalmente.

        Proceso:
        1. Genera Nonce aleatorio de 12 bytes (NIST SP 800-38D para GCM)
        2. Encripta con AES-128-GCM obteniendo ciphertext + tag de autenticacion
        3. Firma Nonce + Ciphertext + Tag con Ed25519 (autenticidad y no repudio)

        Args:
            plaintext: Texto a encriptar (string)

        Returns:
            str: Paquete en formato "Nonce:Ciphertext:GCMTag:Signature" (base64)

        Tiempo: <0.1ms por operacion
        """
        try:
            # Paso 1: Generar Nonce aleatorio para AES-GCM
            # GCM opera de forma optima con nonces de 12 bytes segun NIST SP 800-38D
            # El nonce debe ser unico por cada encriptacion para garantizar seguridad
            nonce = random(12)

            # Paso 2: Encriptar con AES-128-GCM
            # GCM no requiere padding, permite procesamiento paralelo del CTR interno
            # y genera automaticamente un tag de autenticacion de 16 bytes (AEAD)
            plaintext_bytes = plaintext.encode('utf-8')

            encryptor = Cipher(
                algorithms.AES(self.aes_key),
                modes.GCM(nonce),
            ).encryptor()
            ciphertext = encryptor.update(plaintext_bytes) + encryptor.finalize()

            # El tag de autenticacion GCM solo esta disponible despues de finalize()
            # Protege la integridad del ciphertext a nivel del algoritmo de cifrado
            gcm_tag = encryptor.tag

            # Paso 3: Firmar Nonce + Ciphertext + Tag con Ed25519
            # Incluir el tag en la firma garantiza que cubre el paquete completo
            # Esto provee no repudio: solo quien tenga la clave privada pudo firmar
            data_to_sign = nonce + ciphertext + gcm_tag
            signed = self.signing_key.sign(data_to_sign)
            signature = signed.signature

            # Paso 4: Empaquetar componentes en formato legible
            # Formato: Nonce:Ciphertext:GCMTag:Signature (cada uno en base64)
            nonce_b64      = base64.b64encode(nonce).decode('utf-8')
            ciphertext_b64 = base64.b64encode(ciphertext).decode('utf-8')
            gcm_tag_b64    = base64.b64encode(gcm_tag).decode('utf-8')
            signature_b64  = base64.b64encode(signature).decode('utf-8')

            encrypted_package = f"{nonce_b64}:{ciphertext_b64}:{gcm_tag_b64}:{signature_b64}"

            return encrypted_package

        except Exception as e:
            logger.error(f"Error encriptando datos: {e}")
            raise

    def decrypt(self, encrypted_package):
        """
        Desencripta paquete y verifica firma digital.

        Proceso:
        1. Separa los 4 componentes (Nonce, Ciphertext, GCMTag, Signature)
        2. Verifica firma Ed25519 ANTES de desencriptar (rechaza si invalida)
        3. Desencripta con AES-128-GCM que verifica el tag internamente

        Args:
            encrypted_package: Paquete encriptado "Nonce:Ciphertext:GCMTag:Signature"

        Returns:
            str: Texto plano original

        Raises:
            ValueError: Si la firma Ed25519 es invalida (datos comprometidos)
            InvalidTag: Si el tag GCM no coincide (ciphertext modificado a nivel de cifrado)

        Tiempo: <0.1ms por operacion
        """
        try:
            # Paso 1: Separar los 4 componentes del paquete
            parts = encrypted_package.split(':')
            if len(parts) != 4:
                raise ValueError(
                    "Formato de paquete invalido (esperado: Nonce:Ciphertext:GCMTag:Signature)"
                )

            nonce_b64, ciphertext_b64, gcm_tag_b64, signature_b64 = parts

            # Decodifica cada componente de base64 a bytes para procesamiento
            nonce      = base64.b64decode(nonce_b64)
            ciphertext = base64.b64decode(ciphertext_b64)
            gcm_tag    = base64.b64decode(gcm_tag_b64)
            signature  = base64.b64decode(signature_b64)

            # Paso 2: Verificar firma Ed25519 ANTES de desencriptar
            # Verificar primero es mas eficiente: rechaza datos invalidos sin gastar
            # CPU en descifrado; previene ataques de manipulacion del ciphertext
            data_signed = nonce + ciphertext + gcm_tag

            try:
                self.verify_key.verify(data_signed, signature)
            except Exception as e:
                logger.error(f"Firma Ed25519 invalida: {e}")
                raise ValueError("Firma criptografica invalida - datos comprometidos o modificados")

            # Paso 3: Desencriptar con AES-128-GCM
            # Solo llega aqui si la firma Ed25519 fue valida
            # GCM recibe el tag en su constructor y lo verifica al llamar finalize()
            # Si el tag no coincide, finalize() lanza InvalidTag automaticamente
            decryptor = Cipher(
                algorithms.AES(self.aes_key),
                modes.GCM(nonce, gcm_tag),
            ).decryptor()
            plaintext_bytes = decryptor.update(ciphertext) + decryptor.finalize()

            return plaintext_bytes.decode('utf-8')

        except (ValueError, InvalidTag):
            raise
        except Exception as e:
            logger.error(f"Error desencriptando datos: {e}")
            raise

    def get_public_key_hex(self):
        """
        Obtiene la clave publica Ed25519 en formato hexadecimal.
        Util para compartir con otros sistemas o para auditoria.

        Returns:
            str: Clave publica con prefijo 0x (compatible con formato Ethereum)
        """
        # Convierte la clave publica a bytes y la representa en hexadecimal
        public_key_bytes = bytes(self.verify_key)
        return '0x' + public_key_bytes.hex()

def encrypt_fields(data_dict, fields_to_encrypt, encryptor):
    """
    Encripta campos especificos de un diccionario.
    Util para encriptar solo datos sensibles manteniendo metadata en claro.

    Args:
        data_dict: Diccionario con datos
        fields_to_encrypt: Lista de nombres de campos a encriptar
        encryptor: Instancia de DataEncryptor

    Returns:
        dict: Nuevo diccionario con campos especificados encriptados

    Ejemplo:
        data = {"nombre": "Juan", "edad": 25, "voto": "A"}
        encrypted = encrypt_fields(data, ["nombre", "voto"], encryptor)
        # Resultado: {"nombre": "Nonce:Cipher:Tag:Sig", "edad": 25, "voto": "Nonce:Cipher:Tag:Sig"}
    """
    # Copia el diccionario original para no modificar la estructura de entrada
    encrypted_data = data_dict.copy()

    for field in fields_to_encrypt:
        if field in encrypted_data and encrypted_data[field]:
            # Convierte el valor a string y encripta el campo indicado
            encrypted_data[field] = encryptor.encrypt(str(encrypted_data[field]))

    return encrypted_data

def decrypt_fields(data_dict, fields_to_decrypt, encryptor):
    """
    Desencripta campos especificos de un diccionario.

    Args:
        data_dict: Diccionario con campos encriptados
        fields_to_decrypt: Lista de nombres de campos a desencriptar
        encryptor: Instancia de DataEncryptor

    Returns:
        dict: Nuevo diccionario con campos especificados desencriptados

    Raises:
        ValueError: Si algún campo tiene firma Ed25519 invalida
        InvalidTag: Si algun campo tiene tag GCM invalido
    """
    # Copia el diccionario original para no modificar la estructura de entrada
    decrypted_data = data_dict.copy()

    for field in fields_to_decrypt:
        if field in decrypted_data and decrypted_data[field]:
            # Desencripta y verifica firma; propaga excepcion si el campo esta comprometido
            decrypted_data[field] = encryptor.decrypt(decrypted_data[field])

    return decrypted_data

def generate_new_ed25519_keypair():
    """
    Genera un nuevo par de claves Ed25519 (Solana-compatible).

    IMPORTANTE: Solo usar en desarrollo o setup inicial.
    En produccion, usar claves previamente generadas de forma segura.

    Returns:
        tuple: (private_key_hex, public_key_hex)

    Ejemplo:
        priv, pub = generate_new_ed25519_keypair()
        print(f"ED25519_PRIVATE_KEY={priv}")
        print(f"ED25519_PUBLIC_KEY={pub}")
    """
    # Genera un par de claves Ed25519 aleatorio usando libsodium via PyNaCl
    signing_key = SigningKey.generate()

    # Extrae los bytes de clave privada y publica por separado
    private_key_bytes = bytes(signing_key)
    public_key_bytes = bytes(signing_key.verify_key)

    # Convierte ambas claves a formato hexadecimal para almacenamiento en variables de entorno
    private_key_hex = private_key_bytes.hex()
    public_key_hex = public_key_bytes.hex()

    return private_key_hex, public_key_hex
