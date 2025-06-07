from django.shortcuts import render
from rest_framework import generics, viewsets
from .models import Footprint
from .serializers import FootprintSerializer

# Create your views here.

class FootprintListView(generics.ListAPIView):
    queryset = Footprint.objects.all()
    serializer_class = FootprintSerializer

class FootprintViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Footprint.objects.all()
    serializer_class = FootprintSerializer
