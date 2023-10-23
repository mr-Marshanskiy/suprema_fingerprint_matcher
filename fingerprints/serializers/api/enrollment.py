import json
import pdb

import requests
from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ParseError

from config.settings import BOARD_API_URL, BOARD_API_TOKEN
from fingerprints.models.dicts import CaptureMode, CaptureType
from fingerprints.models.enrollment import Enrollment, Finger, Slap

from fingerprints.serializers.nested import enrollment as nested
from fingerprints.tools.board_sync import BoardSyncService
from persons.models import Person


class EnrollmentCreateSerializer(serializers.ModelSerializer):
    person = nested.EnrollmentPersonCreateSerializer(write_only=True)
    captureMode = serializers.CharField(write_only=True)
    captureType = serializers.CharField(write_only=True)
    errCode = serializers.IntegerField(write_only=True)
    errMsg = serializers.CharField(write_only=True, allow_blank=True)

    fingers = nested.EnrollmentFingerCreateSerializer(many=True, write_only=True)
    slaps = nested.EnrollmentSlapCreateSerializer(many=True, write_only=True)

    class Meta:
        model = Enrollment
        fields = (
            'id',
            'person',
            'captureMode',
            'captureType',
            'errCode',
            'errMsg',
            'fingers',
            'slaps',
        )

    def validate_captureMode(self, value):
        return CaptureMode.objects.filter(code=value.lower()).first()

    def validate_captureType(self, value):
        return CaptureType.objects.filter(code=value.lower()).first()

    def validate_errMsg(self, value):
        if value not in ['', None]:
            raise ParseError(value)
        return value

    def validate(self, attrs):
        attrs['capture_mode'] = attrs.pop('captureMode')
        attrs['capture_type'] = attrs.pop('captureType')
        attrs['error_code'] = attrs.pop('errCode')
        attrs['error_message'] = attrs.pop('errMsg')
        return attrs

    def create(self, validated_data):
        with transaction.atomic():
            person_data = validated_data.pop('person', None)
            fingers_data = validated_data.pop('fingers', None)
            slaps_data = validated_data.pop('slaps', None)
            error_code = validated_data.pop('error_code')
            error_message = validated_data.pop('error_message')

            person = Person.objects.create(**person_data)
            validated_data['person'] = person
            enrollment = super().create(validated_data)

            for obj in fingers_data:
                Finger.objects.create(enrollment=enrollment, **obj)
            for obj in slaps_data:
                Slap.objects.create(enrollment=enrollment, **obj)
        BoardSyncService().create_in_board(person_data, enrollment)
        return enrollment


class FingerTemplateIdentifySerializer(serializers.Serializer):
    template = serializers.CharField()
