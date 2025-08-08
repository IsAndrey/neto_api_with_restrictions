from django.contrib import admin
from .models import Advertisement, FavoriteAdvertisement
# Register your models here.

@admin.register(Advertisement)
class AdvertAdmin(admin.ModelAdmin):
    pass

@admin.register(FavoriteAdvertisement)
class AdvertAdmin(admin.ModelAdmin):
    pass