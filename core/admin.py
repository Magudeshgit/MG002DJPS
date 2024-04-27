from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register([stock,
                     client,
                     bill,
                     labor,
                     attendance,
                     salarymanagement
                     ])