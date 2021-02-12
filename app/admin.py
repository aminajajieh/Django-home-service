from django.contrib import admin
from django.contrib.auth.models import Group
from .models import *

from django.contrib import admin
from .models import *
from django.contrib.auth.models import Group
from django.contrib import admin
from .models import *
# Register your models here.from
from admin_auto_filters.filters import AutocompleteFilter
from django.contrib.admin.actions import delete_selected
from django.contrib.auth import get_permission_codename
from rangefilter.filter import DateRangeFilter, DateTimeRangeFilter
from django.db.models import Sum
from django.contrib import admin
from background_task.models import *
from background_task.admin import *
from django.contrib.sites.models import Site
from django.contrib.sites.admin import SiteAdmin

from django.db.models import Sum, Avg

# Register your models here.
class CategoryFilter(AutocompleteFilter):
    title = 'نوع الخدمه'  # display title
    field_name = 'category'
class ClientFilter(AutocompleteFilter):
    title = 'العميل'  # display title
    field_name = 'client'
class ServiceFilter(AutocompleteFilter):
    title = ' الخدمه'  # display title
    field_name = 'service'

class WorkerFilter(AutocompleteFilter):
    title = ' الموظف المسؤل'  # display title
    field_name = 'worker'


class Inline(admin.TabularInline):
    model = ClientService
    extra = 0
    autocomplete_fields = ['service','worker']


class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['title']
    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}


class ServiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'price','category']
    search_fields = ['title']
    autocomplete_fields = ['category']
    list_filter = [CategoryFilter]



class ClientAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone','email']
    search_fields = ['title','phone']
    inlines = [Inline]


class ClientServiceAdmin(admin.ModelAdmin):
    list_display = ['client', 'service', 'price','active']
    search_fields = ['client']
    autocomplete_fields = ['service','client','worker']
    list_filter = [ClientFilter,ServiceFilter,WorkerFilter,'label']





class HelpAdmin(admin.ModelAdmin):
    def has_change_permission(self, request, obj=Help):
        return False
    def has_add_permission(self, request, obj=Help):
        return False
    def a(self, request, object):
        object.update(label='A')
    def b(self, request, object):
        object.update(label='B')
    def c(self, request, object):
        object.update(label='C')

    a.short_description = 'تغيير الحاله الى قيد الانتظار'
    b.short_description = 'تغيير الحاله الى تم التواصل '
    c.short_description = 'تغيير الحاله الى مغلق'

    list_display = ['name', 'email','date']
    search_fields = ['name']
    list_filter = ['label']
    actions = [a,b,c]

class WorkerAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone','email']
    search_fields = ['title','phone']

class BondAdmin(admin.ModelAdmin):
    list_display = ['title','price','id']
    search_fields = ['title','id']

class PostsAdmin(admin.ModelAdmin):
    def a(self, request, object):
        object.update(active = True)
    def b(self, request, object):
        object.update(active = False)


    a.short_description = 'تفعيل المقالات المحدده'
    b.short_description = 'الغاء تفعيل المقالات المحدده'
    list_display = ['title', 'date', 'active']
    search_fields = ['title']
    actions = [a,b]
class SiteEditAdmin(admin.ModelAdmin):
    fieldsets = (
        ("اساسي", {
            'classes': ('collapse',),
            "fields": ['title','img2','content','small','script','active']}),
        ("الرئيسيه", {
            'classes': ('collapse',),
            "fields": ['img3','img4','img5','img6','whyus1', 'whyus2', 'whyus3']
        }),
        ("من نحن", {
            "description": "تعديل صفحة من نحن",
            'classes': ('collapse',),
            "fields": ['about','img','roya','resala','hadaf']
        }),
        ("معلومات التواصل", {
            "description": "تعديل معلومات التواصل",
            'classes': ('collapse',),
            "fields": ['email', 'phone', 'address', 'facebook', 'instagram', 'twitter','whatsapp']
        }),

    )

    if SiteEdit.objects.count() >=1:
        def has_add_permission(self, request):
            return False
    def has_delete_permission(self, request, obj=None):
        False
    pass


class TAS(TaskAdmin):
    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}
class TAS2(CompletedTaskAdmin):
    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}
class SiteeAdmin(admin.ModelAdmin):
    list_display = ('domain', 'name')

    def has_delete_permission(self, request, obj=Site):
        return False

    def has_add_permission(self, request, obj=Site):
        return False
    pass
#------------------------------------------
admin.site.unregister(Group)
admin.site.unregister(CompletedTask)
admin.site.unregister(Task)
admin.site.unregister(Site)
###########################################
admin.site.register(Category,CategoryAdmin)
admin.site.register(Service,ServiceAdmin)
admin.site.register(Client,ClientAdmin)
admin.site.register(ClientService,ClientServiceAdmin)
admin.site.register(Help,HelpAdmin)
admin.site.register(Worker,WorkerAdmin)
admin.site.register(Bond,BondAdmin)
admin.site.register(Posts,PostsAdmin)
admin.site.register(SiteEdit,SiteEditAdmin)
admin.site.register(Site,SiteeAdmin)
admin.site.register(Task,TAS )
admin.site.register(CompletedTask,TAS2)







###########################################
admin.site.site_header = 'لوحة التحكم'
admin.site.site_title = 'لوحة التحكم'
admin.site.index_title = ''