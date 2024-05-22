from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin   

# Register your models here.

class stockexport(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'productname', 'maximumstock', 'quantity','price')

admin.site.register([client,
                     bill,
                     labor,
                     attendance,
                     salarymanagement
                     ])

admin.site.register(stock,stockexport)