import pdb

from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

from fingerprints.models.enrollment import Enrollment
from fingerprints.serializers.api.enrollment import EnrollmentCreateSerializer


@extend_schema_view(
    post=extend_schema(summary='Create enrollment', tags=['Fingerprints: Enrollment']),
)
class EnrollmentCreateView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = EnrollmentCreateSerializer
    queryset = Enrollment.objects.all()
