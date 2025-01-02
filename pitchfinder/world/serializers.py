from world.models import Pitch
from rest_framework import serializers

class PitchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pitch
        fields = ("id", "name", "address", "location")
        extra_kwargs = {"location": {"read_only": True}}
