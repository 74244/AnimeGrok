from django.contrib import admin
from src.subscriptions.models import Subscription


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('article', 'get_subs_count')
    search_fields = ('article', )
    save_as = True
    save_on_top = True

    def get_subs_count(self, obj):
        return obj.users.count()
