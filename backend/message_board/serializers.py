from rest_framework import serializers
from .models import Message

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'text', 'timestamp']
        read_only_fields = ['timestamp'] # 时间戳通常是只读的，由服务器设置 