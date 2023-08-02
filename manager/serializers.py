from rest_framework import serializers
from .models import Elevator, Request

# ElevatorInitializationSerializer
class ElevatorInitializationSerializer(serializers.Serializer):
    number_of_elevators = serializers.IntegerField(min_value=1)

class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = ('direction','floor')
    

class ElevatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Elevator
        fields = '__all__'
    
