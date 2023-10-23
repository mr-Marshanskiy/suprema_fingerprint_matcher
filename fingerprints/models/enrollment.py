import uuid

from django.db import models

from common.models.mixins import DateMixin


class Enrollment(DateMixin):
    person = models.ForeignKey(
        'persons.Person', models.CASCADE, 'enrollment',
        verbose_name='Person'
    )
    capture_mode = models.ForeignKey(
        'CaptureMode', models.RESTRICT, 'enrollment',
        verbose_name='Capture mode'
    )
    capture_type = models.ForeignKey(
        'CaptureType', models.RESTRICT, 'enrollment',
        verbose_name='Capture type'
    )

    class Meta:
        verbose_name = 'Enrollment'
        verbose_name_plural = 'Enrollment'


class Slap(DateMixin):
    enrollment = models.ForeignKey(
        Enrollment, models.CASCADE, 'slaps',
        verbose_name='Enrollment'
    )
    slap_type = models.ForeignKey(
        'SlapType', models.RESTRICT, 'slaps',
        verbose_name='Slap type'
    )
    image_type = models.CharField('Image Type', max_length=15)
    image_data = models.TextField('Image Data')
    iso_fir_type = models.CharField('ISO FIR Type', max_length=15)
    iso_fir_data = models.TextField('ISO FIR Data')
    wsq_data = models.TextField('WSQ Data')

    class Meta:
        verbose_name = 'Slap'
        verbose_name_plural = 'Slaps'


class Finger(DateMixin):
    enrollment = models.ForeignKey(
        Enrollment, models.CASCADE, 'fingers',
        verbose_name='Enrollment'
    )
    finger_type = models.ForeignKey(
        'FingerType', models.RESTRICT, 'fingers',
        verbose_name='Finger type'
    )
    image_type = models.CharField('Image Type', max_length=15)
    image_data = models.TextField('Image Data')
    image_quality = models.PositiveSmallIntegerField('Image Quality')
    iso_fir_type = models.CharField('ISO FIR Type', max_length=15)
    iso_fir_data = models.TextField('ISO FIR Data')
    iso_fmr_type = models.CharField('ISO FMR Type', max_length=15)
    iso_fmr_data = models.TextField('ISO FMR Data')
    wsq_data = models.TextField('WSQ Data')
    finger_uuid = models.CharField('UUID', default=uuid.uuid4, blank=True)

    class Meta:
        verbose_name = 'Finger'
        verbose_name_plural = 'Fingers'

    @staticmethod
    def get_template_values(status=None, board_id=None):
        qs = Finger.objects.values_list('iso_fmr_data', flat=True)
        if status:
            qs = qs.filter(enrollment__person__status_id=status)
        if board_id:
            qs = qs.filter(enrollment__person__board_id=board_id)
        return qs
