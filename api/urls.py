from django.urls import path, include

from api.spectacular.urls import urlpatterns as doc_urls
from fingerprints.urls import urlpatterns as fingerprints_urls
app_name = 'api'

urlpatterns = [
    path('auth/', include('djoser.urls.jwt')),
]

urlpatterns += doc_urls
urlpatterns += fingerprints_urls
