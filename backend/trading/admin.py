from django.contrib import admin
from . import models


admin.site.register(models.Trade)
# class TradeAdmin(admin.ModelAdmin):
#     list_display = ('id', 'title')


admin.site.register(models.Summary)
# class SummaryAdmin(admin.ModelAdmin):
#     list_display = ('id', 'item')