from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FootprintViewSet

router = DefaultRouter()
router.register(r'', FootprintViewSet, basename='footprint')

urlpatterns = [
    path('', include(router.urls)),
] 