from django.contrib import admin

from src.profiles.models import UserNet
# Register your models here.

@admin.register(UserNet)
class UserNetAdmin(admin.ModelAdmin):
    list_display = ('username', 'id', )
    
