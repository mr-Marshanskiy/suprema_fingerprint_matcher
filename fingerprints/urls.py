from django.urls import path
from rest_framework.routers import DefaultRouter

from fingerprints.views import enrollment, identification

router = DefaultRouter()

urlpatterns = [
    path('fingerprints/identify/', identification.FingerIdentifyView.as_view(), name='identify'),
    path('fingerprints/verify/', identification.FingerVerifyView.as_view(), name='verify'),
    path('fingerprints/destroy/<int:board_id>/', identification.PersonDestroyView.as_view(), name='destroy'),
    path('fingerprints/enrollment/', enrollment.EnrollmentCreateView.as_view(), name='enrollment-create'),
]
