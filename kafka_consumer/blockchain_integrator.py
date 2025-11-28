# Integración con Ganache para enviar votos al blockchain
from web3 import Web3
import os
import json


class BlockchainIntegrator:
    """
    Clase que gestiona la comunicación con Ganache
    """
    
    def __init__(self):
        # Conectar a Ganache
        ganache_url = os.environ.get('GANACHE_URL', 'http://ganache:8545')
        self.web3 = Web3(Web3.HTTPProvider(ganache_url))
        
        if not self.web3.is_connected():
            raise ConnectionError(f"No se pudo conectar a Ganache: {ganache_url}")
        
        print(f"Conectado a Ganache: {ganache_url}")
        
        # TODO: Cargar contrato (ABI y address)
        # self.contract = self.web3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)
    
    def enviar_voto(self, votante_hash, candidato_id):
        """
        Envía un voto al smart contract en Ganache
        
        Returns:
            str: Transaction hash
        """
        # TODO: Implementar llamada al contrato
        # tx_hash = self.contract.functions.votar(candidato_id).transact({
        #     'from': self.web3.eth.accounts[0],
        #     'gas': 100000
        # })
        
        # Por ahora, simulación
        print(f"  → Enviando voto a blockchain (votante: {votante_hash[:8]}..., candidato: {candidato_id})")
        
        # Simular TX hash
        import hashlib
        tx_hash = '0x' + hashlib.sha256(f"{votante_hash}{candidato_id}".encode()).hexdigest()
        
        return tx_hash
