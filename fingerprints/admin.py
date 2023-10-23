from django.contrib import admin

from common.models.mixins import DateModelAdminMixin
from fingerprints.models import dicts, enrollment


class SlapInline(admin.TabularInline):
    model = enrollment.Slap
    fields = ('id', 'slap_type',)
    readonly_fields = ('id', 'slap_type',)
    show_change_link = True
    extra = 0


class FingerInline(admin.TabularInline):
    model = enrollment.Finger
    fields = ('id', 'finger_type',)
    readonly_fields = ('id', 'finger_type',)
    show_change_link = True
    extra = 0


@admin.register(
    dicts.FingerType,
    dicts.SlapType,
    dicts.CaptureMode,
    dicts.CaptureType
)
class DictAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')


@admin.register(enrollment.Enrollment)
class EnrollmentAdmin(DateModelAdminMixin):
    list_display = ('id', 'person', 'capture_mode', 'capture_type',)
    search_fields = ('person__id', 'person__last_name', 'person__first_name')
    filter_fields = ('capture_mode', 'capture_type')
    inlines = (
        SlapInline,
        FingerInline,
    )


@admin.register(enrollment.Slap)
class SlapAdmin(DateModelAdminMixin):
    list_display = ('id', 'enrollment', 'slap_type',)
    search_fields = ('enrollment__id',)
    filter_fields = ('slap_type',)


@admin.register(enrollment.Finger)
class FingerAdmin(DateModelAdminMixin):
    list_display = ('id', 'enrollment', 'finger_type',)
    search_fields = ('enrollment__id',)
    filter_fields = ('finger_type',)
