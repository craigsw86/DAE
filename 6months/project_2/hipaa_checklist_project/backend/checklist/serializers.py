from rest_framework import serializers
from .models import RegulationUpdate, ChecklistItem

class RegulationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegulationUpdate
        fields = '__all__'
        depth = 1

class ChecklistItemSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    regulation_update = serializers.SerializerMethodField()

    class Meta:
        model = ChecklistItem
        fields = '__all__'

    def get_user(self, obj):
        return obj.user.username if obj.user else None

    def get_regulation_update(self, obj):
        return obj.regulation_update.title if obj.regulation_update else None 