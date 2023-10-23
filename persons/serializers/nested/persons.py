from rest_framework.serializers import ModelSerializer

from persons.models import Person


class PersonShortSerializer(ModelSerializer):
    class Meta:
        model = Person
        fields = (
            'full_name',
            'status',
            'board_id',
        )
