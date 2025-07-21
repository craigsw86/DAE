from rest_framework import serializers
from .models import ChecklistItem, RegulationUpdate

class RegulationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegulationUpdate
        fields = '__all__'

class ChecklistItemSerializer(serializers.ModelSerializer):
    regulation = RegulationUpdateSerializer(source='regulation_update', read_only=True)

    class Meta:
        model = ChecklistItem
        fields = ['id', 'regulation', 'completed', 'notes', 'last_updated']