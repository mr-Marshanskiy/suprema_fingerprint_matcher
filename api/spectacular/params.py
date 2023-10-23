from drf_spectacular.utils import OpenApiParameter


auth_token = OpenApiParameter(
    name='AuthToken',
    description='Auth Token',
    required=True,
    type=str,
    location='header'
)
