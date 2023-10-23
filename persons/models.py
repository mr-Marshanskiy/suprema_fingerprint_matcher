from django.db import models

from common.models.mixins import DateMixin, DictBaseCodeMixin


class Status(DictBaseCodeMixin):
    class Meta:
        verbose_name = '[DICTS] Status'
        verbose_name_plural = '[DICTS] Statuses'


class Person(DateMixin):
    status = models.ForeignKey(
        Status, models.RESTRICT, 'persons',
        verbose_name='Status',
    )
    first_name = models.CharField('First name', max_length=31,)
    last_name = models.CharField('Last name', max_length=31,)
    board_id = models.PositiveBigIntegerField(null=True, blank=True,)

    class Meta:
        verbose_name = 'Person'
        verbose_name_plural = 'Persons'

    def __str__(self):
        return f'{self.full_name} (id: {self.pk})'

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'
