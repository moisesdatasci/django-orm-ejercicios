from django.contrib import admin
from .models import Producto

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'precio', 'disponible']
    list_filter = ['disponible']
    search_fields = ['nombre']