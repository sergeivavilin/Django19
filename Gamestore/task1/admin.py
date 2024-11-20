from django.contrib import admin

from .models import Buyer, Game


@admin.register(Buyer)
class BuyerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'balance', 'age')
    list_display_links = ('id',)
    search_fields = ('name', )
    list_filter = ('name', 'age')

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'cost', 'age_limited')
    list_display_links = ('id', 'title', )
    search_fields = ('title', )
    list_filter = ('title', 'age_limited')
