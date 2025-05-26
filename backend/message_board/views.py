from django.shortcuts import render
from rest_framework import generics
from .models import Message
from .serializers import MessageSerializer

# Create your views here.

class MessageListCreateView(generics.ListCreateAPIView):
    queryset = Message.objects.all().order_by('-timestamp') # 按时间倒序排列
    serializer_class = MessageSerializer
