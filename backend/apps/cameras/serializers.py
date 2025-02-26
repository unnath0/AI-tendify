from rest_framework import serializers
from .models import Camera, EngagementRecord


class CameraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Camera
        fields = "__all__"


class EngagementRecordSerializer(serializers.ModelSerializer):
    engagement_percentage = serializers.ReadOnlyField()

    class Meta:
        model = EngagementRecord
        fields = "__all__"
