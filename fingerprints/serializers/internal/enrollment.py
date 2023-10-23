from rest_framework import serializers


class EnrollmentPersonBoardCreateSerializer(serializers.Serializer):
    status = serializers.CharField(write_only=True)
    board_id = serializers.CharField(write_only=True)


class EnrollmentFingerBoardCreateSerializer(serializers.Serializer):
    finger = serializers.CharField(source='finger_type.code')
    image = serializers.CharField(source='image_data')
    template_uuid = serializers.CharField(source='finger_uuid')
