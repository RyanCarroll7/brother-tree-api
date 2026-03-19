from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import BrotherViewSet

router = DefaultRouter()
router.register(r'brothers', BrotherViewSet, "brother")

urlpatterns = [
    path('', include(router.urls))
]