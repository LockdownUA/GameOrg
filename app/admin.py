from django.contrib import admin
from .models import Item, Profile, Genre
# Register your models here.

admin.site.register(Item)
admin.site.register(Profile)
admin.site.register(Genre)