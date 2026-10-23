from rest_framework import serializers
from core.models import Cliente, Animal, Veterinario, Consulta
class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'

class ClienteSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ["id", "nome", "cpf"]

class AnimalSerializer(serializers.ModelSerializer):
    doneo = ClienteSimpleSerializer(read_only=True)
    especie_nome = serializers.CharField(source='get_especie_nome', read_only=True)
    class Meta:
        model = Animal
        fields = ("id", "nome", "especie", "especie_nome", "raca", "idade", "peso", "doneo")

class VeterinarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Veterinario
        fields = '__all__'

class ConsultaSerializer(serializers.ModelSerializer):
    animal = AnimalSerializer(read_only=True)
    veterinario = VeterinarioSerializer(read_only=True)
    class Meta:
        model = Consulta
        fields = '__all__'

class ConsultaAddSerializer(serializers.ModelSerializer):
                         
    animal = serializers.PrimaryKeyRelatedField(
        queryset = Animal.objects.all(), write_only=True
    )
                              
    veterinario = serializers.PrimaryKeyRelatedField(
        queryset = Veterinario.objects.all(), write_only=True
    )

    class Meta:
        model = Consulta
        fields = '__all__'