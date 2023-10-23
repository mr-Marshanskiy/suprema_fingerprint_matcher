from django.db import models

from common.models.mixins import DictBaseCodeMixin


class CaptureMode(DictBaseCodeMixin):
    class Meta:
        verbose_name = '[DICTS] Capture mode'
        verbose_name_plural = '[DICTS] Capture modes'


class CaptureType(DictBaseCodeMixin):
    class Meta:
        verbose_name = '[DICTS] Capture type'
        verbose_name_plural = '[DICTS] Capture types'


class FingerType(DictBaseCodeMixin):
    number = models.PositiveSmallIntegerField(unique=True, default=1)

    class Meta:
        verbose_name = '[DICTS] Finger type'
        verbose_name_plural = '[DICTS] Finger types'


class SlapType(DictBaseCodeMixin):
    class Meta:
        verbose_name = '[DICTS] Slap type'
        verbose_name_plural = '[DICTS] Slap types'
