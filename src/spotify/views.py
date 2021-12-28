from django.http import JsonResponse
from rest_framework.viewsets import ViewSet


class SpotifyTokenViewSet(ViewSet):
    @staticmethod
    def create(request):
        return JsonResponse({
            "token": "abc"
        })
