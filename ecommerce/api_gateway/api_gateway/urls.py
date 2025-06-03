from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

def test_graphql(request):
    return JsonResponse({
        'message': 'GraphQL endpoint is working!',
        'status': 'success'
    })

urlpatterns = [
    path('admin/', admin.site.urls),
    path('graphql/', test_graphql),
]
