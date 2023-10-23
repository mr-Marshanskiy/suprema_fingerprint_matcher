from rest_framework import serializers

from fingerprints.models.enrollment import Finger
from persons.serializers.nested.persons import PersonShortSerializer


class FingerIdentifySerializer(serializers.Serializer):
    template = serializers.CharField()
    status = serializers.CharField()


class FingerVerifySerializer(serializers.Serializer):
    template = serializers.CharField()
    status = serializers.CharField()
    board_id = serializers.CharField()


class FingerDetailSerializer(serializers.ModelSerializer):
    person = PersonShortSerializer(source='enrollment.person')

    class Meta:
        model = Finger
        fields = (
            'id',
            'person',
        )
