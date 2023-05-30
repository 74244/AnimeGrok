from django.contrib import admin
from .models import Subscription


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('article', 'user')
    search_fields = ('article', 'user')
    save_as = True
    save_on_top = True