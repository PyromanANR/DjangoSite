from django.contrib import admin
from .models import Category, Product, Profile

# Register your models here.
admin.site.register(Category)
admin.site.register(Profile)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_filter = ('category',)
    list_display = ('name', 'cost', 'category')
    search_fields = ('name',)