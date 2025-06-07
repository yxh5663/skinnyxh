from rest_framework import serializers
from .models import TimelineEvent, CalendarEvent

class TimelineEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimelineEvent
        fields = ['id', 'date', 'title', 'details', 'created_at', 'updated_at'] # 指定需要序列化的字段
        # fields = '__all__' # 或者直接包含所有字段 

class CalendarEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = CalendarEvent
        fields = '__all__' # 包含所有字段，方便起见 