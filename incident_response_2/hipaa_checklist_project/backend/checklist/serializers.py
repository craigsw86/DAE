from rest_framework import serializers
from .models import RegulationUpdate, ChecklistItem

class RegulationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegulationUpdate
        fields = '__all__'
        depth = 1

class ChecklistItemSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    regulation_update_title = serializers.SerializerMethodField()
    likelihood = serializers.IntegerField()
    impact = serializers.IntegerField()
    mitigation_steps = serializers.CharField(allow_blank=True, allow_null=True, required=False)

    class Meta:
        model = ChecklistItem
        fields = '__all__'
        read_only_fields = ('user',)

    def get_user(self, obj):
        return obj.user.username if obj.user else None

    def get_regulation_update_title(self, obj):
        return obj.regulation_update.title if obj.regulation_update else None

    def create(self, validated_data):
        # Set the user from the request
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data) 