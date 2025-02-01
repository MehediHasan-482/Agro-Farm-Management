from django.contrib import admin

# Register your models here.
from .models import Portfolio

class PortfolioAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at')
    search_fields = ('title', 'description', 'vision', 'mission')
    list_filter = ('created_at', 'updated_at')
    ordering = ('-created_at',)
    fields = ('title', 'description', 'vision', 'mission', 'document', 'framework_image', 'health_monitoring_document', 'health_monitoring_image')

admin.site.register(Portfolio, PortfolioAdmin)