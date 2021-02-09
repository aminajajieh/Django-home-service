from django.contrib import admin
from .models import Notification


class NotificationAdmin(admin.ModelAdmin):
    raw_id_fields = ["user"]
    search_fields = ["user"]

    def get_queryset(self, request):
        qs = super(NotificationAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)
    
    def get_list_display(self, request):

        return ['content', "send_date",
                    "get_link"]

        
    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return []
        else:
            return ["user", "icon", "color", "content", "url", "seen_date",
                    "send_date"]

    def has_change_permission(self, request, obj=Notification):
        return False

    def has_add_permission(self, request, obj=Notification):
        return False
      
            
    
admin.site.register(Notification, NotificationAdmin)
