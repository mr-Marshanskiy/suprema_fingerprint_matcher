from rest_framework import serializers
from rest_framework.exceptions import ParseError

from fingerprints.models.dicts import FingerType, SlapType
from fingerprints.models.enrollment import Finger, Slap
from fingerprints.tools.matcher.identification import FingerMatcher
from persons.models import Person


class EnrollmentPersonCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Person
        exclude = ('created_at', 'updated_at',)


class EnrollmentFingerCreateSerializer(serializers.Serializer):
    fingerNo = serializers.CharField(write_only=True)
    imgQuality = serializers.IntegerField(write_only=True)
    wsqData = serializers.CharField(write_only=True)
    imgType = serializers.CharField(write_only=True)
    imgData = serializers.CharField(write_only=True)
    isoFMRType = serializers.CharField(write_only=True)
    isoFMRData = serializers.CharField(write_only=True)
    isoFIRType = serializers.CharField(write_only=True)
    isoFIRData = serializers.CharField(write_only=True)

    def validate_fingerNo(self, value):
        return FingerType.objects.filter(number=value).first()

    def validate_isoFMRData(self, value):
        templates = Finger.get_template_values()
        response, template_index = FingerMatcher().identify(
            value,
            templates
        )
        if response == 0:
            if template_index.value != -1:
                finger = Finger.objects.filter(iso_fmr_data=templates[template_index.value]).first()
                person = finger.enrollment.person
                raise ParseError(
                    f' Attention! A match has been found for one of the fingerprints. '
                    f'Match with person {person.full_name} ({person.pk}).'
                )
            return value
        raise ParseError(f'Error with matcher: code {response}')

    def validate(self, attrs):
        attrs = {
            'finger_type': attrs['fingerNo'],
            'image_quality': attrs['imgQuality'],
            'wsq_data': attrs['wsqData'],
            'image_type': attrs['imgType'],
            'image_data': attrs['imgData'],
            'iso_fmr_type': attrs['isoFMRType'],
            'iso_fmr_data': attrs['isoFMRData'],
            'iso_fir_type': attrs['isoFIRType'],
            'iso_fir_data': attrs['isoFIRData'],
        }
        return attrs


class EnrollmentSlapCreateSerializer(serializers.Serializer):
    slapType = serializers.CharField(write_only=True)
    wsqData = serializers.CharField(write_only=True)
    imgType = serializers.CharField(write_only=True)
    imgData = serializers.CharField(write_only=True)
    isoFIRType = serializers.CharField(write_only=True)
    isoFIRData = serializers.CharField(write_only=True)

    def validate_slapType(self, value):
        return SlapType.objects.filter(code=value.lower()).first()

    def validate(self, attrs):
        attrs = {
            'slap_type': attrs['slapType'],
            'wsq_data': attrs['wsqData'],
            'image_type': attrs['imgType'],
            'image_data': attrs['imgData'],
            'iso_fir_type': attrs['isoFIRType'],
            'iso_fir_data': attrs['isoFIRData'],
        }
        return attrs
