// blockchain/contracts/Votacion.sol

// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

// Contrato optimizado para eventos masivos
contract Votacion {
    // Evento para registrar batch de votos (muy barato en gas)
    event BatchRegistrado(
        string indexed hashBatch,
        uint256 cantidadVotos,
        uint256 anomaliasDetectadas,
        uint256 timestamp
    );
    
    // Storage mínimo: solo contador
    uint256 public totalBatches;
    uint256 public totalVotos;
    uint256 public totalAnomalias;
    
    // Función para registrar batch de 100 votos
    // Emite evento en lugar de escribir todos en storage
    function registrarBatch(
        string memory _hashBatch,
        uint256 _cantidadVotos,
        uint256 _anomaliasDetectadas
    ) public {
        // Actualizar contadores (barato porque son pocos)
        totalBatches++;
        totalVotos += _cantidadVotos;
        totalAnomalias += _anomaliasDetectadas;
        
        // Emitir evento: hash del batch verificable sin guardarlo en storage
        // Costo: ~300 gas vs ~20,000 gas si guardamos 100 votos
        emit BatchRegistrado(
            _hashBatch,
            _cantidadVotos,
            _anomaliasDetectadas,
            block.timestamp
        );
    }
    
    // Función view para obtener estadísticas
    function obtenerEstadisticas() public view returns (
        uint256 batches,
        uint256 votos,
        uint256 anomalias
    ) {
        return (totalBatches, totalVotos, totalAnomalias);
    }
}
