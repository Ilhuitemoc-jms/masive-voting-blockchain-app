#file de prueba
FROM trufflesuite/ganache:latest

# Exponer puerto RPC
EXPOSE 8545

# Comando para iniciar Ganache con configuración básica
CMD ["node", "/app/ganache-core.docker.cli.js", \
     "--host", "0.0.0.0", \
     "--port", "8545", \
     "--networkId", "5777", \
     "--accounts", "10", \
     "--defaultBalanceEther", "1000", \
     "--gasLimit", "10000000"]
