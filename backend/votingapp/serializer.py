# Serializers para validación de datos (sin usar Django ORM)
from rest_framework import serializers

class VotoSerializer(serializers.Serializer):
    """
    Serializer para validar estructura de un voto
    """
    # Datos del votante (van encriptados a MongoDB)
    cvr_id = serializers.IntegerField(required=True)
    precinct_medst = serializers.CharField(max_length=200, required=True)
    precinct_cvr = serializers.CharField(max_length=200, required=True)
    office = serializers.CharField(max_length=100, required=True)
    district = serializers.CharField(max_length=100, required=False, allow_null=True)
    candidate = serializers.CharField(max_length=200, required=True)
    magnitude = serializers.CharField(max_length=10, required=False, allow_null=True)
    party = serializers.CharField(max_length=100, required=False, allow_null=True, allow_blank=True)
    party_detailed = serializers.CharField(max_length=100, required=False, allow_null=True)
    state = serializers.CharField(max_length=100, required=True)
    county = serializers.CharField(max_length=100, required=True)
    voting_hour = serializers.CharField(max_length=50, required=True)
    
    # Candidato (va a blockchain) junto con id y tiempo de voto
    candidato_id = serializers.IntegerField(required=True, min_value=0)
    
    def validate_candidato_id(self, value):
        """
        Valida que el candidato exista en el rango permitido
        """
        # Suponiendo que tienes 5 candidatos (0-4)
        if value < 0 or value > 18:
            raise serializers.ValidationError("El candidato debe estar entre 0 y 4")
        return value
    
    def validate_cvr_id(self, value):
        """
        Valida que el CVR ID sea positivo
        """
        if value <= 0:
            raise serializers.ValidationError("CVR ID debe ser positivo")
        return value

class PadronElectoralSerializer(serializers.Serializer):
    """
    Serializer para autenticación con padrón electoral
    """
    no_cuenta = serializers.CharField(max_length=20, required=True)
    clave_elector = serializers.CharField(max_length=50, required=True)
    
    def validate_no_cuenta(self, value):
        """
        Valida formato de cédula
        """
        if not value.isalnum():
            raise serializers.ValidationError("Cédula debe ser alfanumérica")
        return value
