from django.db import models

class Producto(models.Model):
    nombre = models.CharField(max_length=100, db_index=True)
    precio = models.DecimalField(max_digits=5, decimal_places=2)
    disponible = models.BooleanField(default=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['nombre'], name='idx_producto_nombre'),
        ]
    
    def __str__(self):
        return self.nombre