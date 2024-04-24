from django.contrib import admin
from .models import Category, Product, Profile

class ProductAdmin(admin.ModelAdmin):
    list_filter = ('category',)


# Register your models here.
admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(Profile)
