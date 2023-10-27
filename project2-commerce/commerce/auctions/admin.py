from django.contrib import admin

from .models import ListingModel, User


# Register your models here.
class UserAdmin(admin.ModelAdmin):
    filter_horizontal = ("watchlist",)


admin.site.register(ListingModel)
admin.site.register(User, UserAdmin)
