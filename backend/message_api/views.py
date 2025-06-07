from django.shortcuts import render
from rest_framework import generics, viewsets
from .models import TimelineEvent, CalendarEvent
from .serializers import TimelineEventSerializer, CalendarEventSerializer
from .permissions import IsSuperuserOrReadOnly

# For AuthStatusAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class TimelineEventList(generics.ListAPIView):
    queryset = TimelineEvent.objects.all()
    serializer_class = TimelineEventSerializer
    # Note: TimelineEventList is read-only by default with ListAPIView.
    # If it needs write access, it would also need permission_classes.

# Create your views here.
class CalendarEventViewSet(viewsets.ModelViewSet):
    queryset = CalendarEvent.objects.all()
    serializer_class = CalendarEventSerializer
    permission_classes = [IsSuperuserOrReadOnly]
    # 可以稍后添加过滤等

class AuthStatusAPIView(APIView):
    def get(self, request, *args, **kwargs):
        return Response({
            'is_authenticated': request.user.is_authenticated,
            'is_superuser': request.user.is_superuser,
            'username': request.user.username if request.user.is_authenticated else None
        }, status=status.HTTP_200_OK)
