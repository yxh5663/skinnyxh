# This is an empty urls.py file. 

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TimelineEventList, CalendarEventViewSet, AuthStatusAPIView

# 创建一个路由器并注册我们的 ViewSet
router = DefaultRouter()
router.register(r'calendar-events', CalendarEventViewSet, basename='calendarevent')

urlpatterns = [
    path('timeline-events/', TimelineEventList.as_view(), name='timeline-event-list'),
    path('auth-status/', AuthStatusAPIView.as_view(), name='auth-status'),
    # 在这里添加你的URL模式
    path('', include(router.urls)),
] 