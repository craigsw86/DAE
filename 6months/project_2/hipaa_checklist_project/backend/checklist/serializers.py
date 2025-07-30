from rest_framework import serializers
from .models import RegulationUpdate, ChecklistItem

class RegulationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegulationUpdate
        fields = '__all__'

class ChecklistItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChecklistItem
        fields = '__all__' 