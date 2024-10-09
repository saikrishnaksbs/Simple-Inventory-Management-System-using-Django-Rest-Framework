from django.contrib import admin

# Register your models here.
from .models import Item, CustomUser

admin.site.register(Item)
admin.site.register(CustomUser)