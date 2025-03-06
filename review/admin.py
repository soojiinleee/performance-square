from django.contrib import admin
from .models import ReviewReport

@admin.register(ReviewReport)
class ReviewReportAdmin(admin.ModelAdmin):
    list_display = ('review', 'user', 'get_reason_display', 'created_at', 'updated_at')

    def get_reason_display(self, obj):
        return obj.get_reason_display()

    get_reason_display.short_description = '신고 사유'
