from django.urls import include, path
from rest_framework.routers import DefaultRouter

from fingerprints.views import enrollment, identification

router = DefaultRouter()

urlpatterns = [
    path('fingerprints/identify/', identification.FingerIdentifyView.as_view(), name='identify'),
    path('fingerprints/verify/', identification.FingerVerifyView.as_view(), name='verify'),
    path('fingerprints/destroy/', identification.PersonDestroyView.as_view(), name='destroy'),
    # path('templates/<str:pk>/', views.TemplateDestroyView.as_view(), name='template-destroy'),
    path('fingerprints/enrollment/', enrollment.EnrollmentCreateView.as_view(), name='enrollment-create'),
]
