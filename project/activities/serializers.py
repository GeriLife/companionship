from rest_framework import serializers
from .models import Activity


class ActivitySerializer(serializers.ModelSerializer):
    """Serializer for the Activities"""
    class Meta:
        model = Activity
        fields = '__all__'
