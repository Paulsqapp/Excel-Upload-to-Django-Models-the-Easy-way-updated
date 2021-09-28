from django.contrib import admin
from .models import Staff, Sales

# Register your models here.

class StaffAdmin(admin.ModelAdmin):
    list_display = ['name', 'display_name', 'designation']


class SalesAdmin(admin.ModelAdmin): #add list filter
    list_display = ['staff', 'item_sold', 'quantity', 'unit_price', ]

admin.site.register(Staff, StaffAdmin)
admin.site.register(Sales, SalesAdmin)
