# Ejemplo mínimo de Dockerfile para Ganache
FROM node:16

RUN npm install -g ganache

EXPOSE 8545

CMD ["ganache", "--db=./db", "--host=0.0.0.0", "--port=8545"]
