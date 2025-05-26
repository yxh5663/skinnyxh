from django.contrib import admin
from .models import Message

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('text', 'timestamp') # 显示文本和时间戳
    list_filter = ('timestamp',)       # 可以按时间戳过滤
    search_fields = ('text',)          # 可以搜索文本内容

# 或者使用更简单的方式注册，如果不需要自定义显示：
# admin.site.register(Message)
