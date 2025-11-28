# Utilidades para encriptar/desencriptar datos sensibles
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding as sym_padding
from cryptography.hazmat.backends import default_backend
import os
import base64

class DataEncryptor:
    """
    Encripta y desencripta datos usando AES-256-CBC
    """
    
    def __init__(self):
        # Obtiene la clave de encriptación desde variables de entorno
        key_b64 = os.environ.get('ENCRYPTION_KEY')
        if not key_b64:
            raise ValueError("ENCRYPTION_KEY no definida en variables de entorno")
        
        # Decodifica la clave desde base64
        self.key = base64.b64decode(key_b64)
        
        if len(self.key) != 32:
            raise ValueError("La clave debe ser de 32 bytes (256 bits)")
    
    def encrypt(self, plaintext):
        """
        Encripta texto plano y retorna base64
        """
        # Genera un IV aleatorio de 16 bytes
        iv = os.urandom(16)
        
        # Crea el cipher AES en modo CBC
        cipher = Cipher(
            algorithms.AES(self.key),
            modes.CBC(iv),
            backend=default_backend()
        )
        encryptor = cipher.encryptor()
        
        # Agrega padding al texto plano
        padder = sym_padding.PKCS7(128).padder()
        padded_data = padder.update(plaintext.encode('utf-8')) + padder.finalize()
        
        # Encripta
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()
        
        # Retorna IV + ciphertext codificado en base64
        return base64.b64encode(iv + ciphertext).decode('utf-8')
    
    def decrypt(self, encrypted_b64):
        """
        Desencripta desde base64 y retorna texto plano
        """
        # Decodifica desde base64
        encrypted_data = base64.b64decode(encrypted_b64)
        
        # Extrae IV (primeros 16 bytes) y ciphertext
        iv = encrypted_data[:16]
        ciphertext = encrypted_data[16:]
        
        # Crea el cipher AES en modo CBC
        cipher = Cipher(
            algorithms.AES(self.key),
            modes.CBC(iv),
            backend=default_backend()
        )
        decryptor = cipher.decryptor()
        
        # Desencripta
        padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()
        
        # Remueve padding
        unpadder = sym_padding.PKCS7(128).unpadder()
        plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()
        
        return plaintext.decode('utf-8')


# Función helper para encriptar diccionarios completos
def encrypt_fields(data_dict, fields_to_encrypt, encryptor):
    """
    Encripta campos específicos de un diccionario
    """
    encrypted_data = data_dict.copy()
    
    for field in fields_to_encrypt:
        if field in encrypted_data and encrypted_data[field]:
            encrypted_data[field] = encryptor.encrypt(str(encrypted_data[field]))
    
    return encrypted_data


# Función helper para desencriptar diccionarios
def decrypt_fields(data_dict, fields_to_decrypt, encryptor):
    """
    Desencripta campos específicos de un diccionario
    """
    decrypted_data = data_dict.copy()
    
    for field in fields_to_decrypt:
        if field in decrypted_data and decrypted_data[field]:
            decrypted_data[field] = encryptor.decrypt(decrypted_data[field])
    
    return decrypted_data
