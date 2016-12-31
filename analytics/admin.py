from django.contrib import admin

from .models import ClickEvent


class ClickEventAdmin(admin.ModelAdmin):
    list_display = ('product_hit', 'count')

admin.site.register(ClickEvent, ClickEventAdmin)
