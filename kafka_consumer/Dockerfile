FROM python:3.11-slim

# Evitar que Python buffere la salida (logs inmediatos en Docker)
ENV PYTHONUNBUFFERED=1

# Establecer directorio de trabajo
WORKDIR /app

# Copiar requirements
COPY requirements.txt .

# Instalar dependencias Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el código
COPY . .

# Comando para correr el consumer
CMD ["python", "consumer.py"]
