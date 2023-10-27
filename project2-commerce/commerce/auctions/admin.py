from django.contrib import admin

from .models import ListingModel, User

# Register your models here.
admin.site.register(ListingModel)
admin.site.register(User)
