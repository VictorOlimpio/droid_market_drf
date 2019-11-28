from django.contrib import admin
from demands.models import Demand

class DemandAdmin(admin.ModelAdmin):
    list_display = ['owner', 'piece', 'status']

admin.site.register(Demand, DemandAdmin)