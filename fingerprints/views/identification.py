from django.db.models import Q
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import status
from rest_framework.exceptions import ParseError
from rest_framework.generics import DestroyAPIView, GenericAPIView, \
    get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from fingerprints.models.enrollment import Finger
from fingerprints.serializers.api.identification import FingerDetailSerializer, \
    FingerIdentifySerializer, FingerVerifySerializer
from fingerprints.tools.board_sync import BoardSyncService

from fingerprints.tools.matcher.identification import FingerMatcher
from persons.models import Person


@extend_schema_view(
    post=extend_schema(summary='Identify', tags=['Fingerprints: Identification']),
)
class FingerIdentifyView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = FingerIdentifySerializer
    queryset = Finger.objects.all()

    def post(self, request, *args, **kwargs):
        template = request.data.get('template')
        status_data = request.data.get('status')
        templates = Finger.get_template_values(status_data)
        response, template_index = FingerMatcher().identify(
            template,
            templates
        )
        if template_index.value == -1:
            raise ParseError(
                'Not identified.'
            )
        if response == 0:
            qs = Finger.objects.filter(
                iso_fmr_data=templates[template_index.value],
            )
            instance = qs.first()
            serializer = FingerDetailSerializer(instance).data
            return Response(serializer, status=status.HTTP_200_OK)
        return Response(status.HTTP_400_BAD_REQUEST)


@extend_schema_view(
    post=extend_schema(summary='Verify', tags=['Fingerprints: Identification']),
)
class FingerVerifyView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = FingerVerifySerializer
    queryset = Finger.objects.all()

    def post(self, request, *args, **kwargs):
        template = request.data.get('template')
        status_data = request.data.get('status')
        board_id_data = request.data.get('board_id')
        templates = Finger.get_template_values(status_data, board_id_data)
        response, template_index = FingerMatcher().identify(
            template,
            templates
        )
        if template_index.value == -1:
            raise ParseError(
                'Not verified.'
            )
        if response == 0:
            return Response({'detail': 'Verified'}, status=status.HTTP_200_OK)
        return Response(status.HTTP_400_BAD_REQUEST)


#
@extend_schema_view(
    delete=extend_schema(summary='Destroy', tags=['Fingerprints: Identification']),
)
class PersonDestroyView(DestroyAPIView):
    permission_classes = [AllowAny]
    queryset = Person.objects.all()
    serializer_class = None

    def get_object(self):
        instance = get_object_or_404(
            Person,
            Q(
                status=self.request.data.get('status'),
                board_id=self.request.data.get('board_id'),
            )
        )
        return instance

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        BoardSyncService().destroy_in_board(instance)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
