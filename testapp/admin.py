from django.contrib import admin
from testapp.models import student

# Register your models here.
class studentadmin(admin.ModelAdmin):
    list_display=('id','sName','sSex','sBrithday','sEmail','sPhone','sAddress')
    list_filter=('sName','sPhone')
    search_fields=('sName',)
    ordering=('id',)

admin.site.register(student,studentadmin)