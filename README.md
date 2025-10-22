# Django ORM - Ejercicios Prácticos

Guía práctica para aprender a usar el ORM de Django, desde consultas básicas hasta SQL personalizado.

## Instalación

```bash
# Clonar repositorio
git clone https://github.com/moisesdatasci/django-orm-ejercicios.git
cd django-orm-ejercicios

# Instalar dependencias
pip install django

# Aplicar migraciones
python manage.py migrate
```

## Modelo

```python
class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=5, decimal_places=2)
    disponible = models.BooleanField(default=True)
```

## Ejercicios

### 1. Obtener todos los registros
```python
productos = Producto.objects.all()
```

### 2. Filtrar registros
```python
# Precio mayor a 50
productos = Producto.objects.filter(precio__gt=50)

# Nombre empieza con "A"
productos = Producto.objects.filter(nombre__startswith='A')

# Productos disponibles
productos = Producto.objects.filter(disponible=True)
```

### 3. Consultas SQL con raw()
```python
productos = Producto.objects.raw('SELECT * FROM app_producto WHERE precio < 100')
```

### 4. SQL con parámetros
```python
productos = Producto.objects.raw(
    'SELECT * FROM app_producto WHERE precio < %s',
    [100]
)
```

### 5. Agregar índices
```python
class Producto(models.Model):
    nombre = models.CharField(max_length=100, db_index=True)
    # ...
```

### 6. Excluir campos
```python
# Solo nombre y precio
productos = Producto.objects.only('nombre', 'precio')

# Todo excepto disponible
productos = Producto.objects.defer('disponible')
```

### 7. Anotaciones (campos calculados)
```python
from django.db.models import F, DecimalField, ExpressionWrapper

productos = Producto.objects.annotate(
    precio_con_impuesto=ExpressionWrapper(
        F('precio') * 1.16,
        output_field=DecimalField(max_digits=7, decimal_places=2)
    )
)
```

### 8. SQL personalizado con cursor
```python
from django.db import connection

with connection.cursor() as cursor:
    cursor.execute("SELECT * FROM app_producto WHERE precio < %s", [100])
    rows = cursor.fetchall()
```

### 9. Llamar procedimientos almacenados
```python
with connection.cursor() as cursor:
    cursor.callproc('nombre_procedimiento', [parametro1, parametro2])
```

## Comandos útiles

```bash
# Abrir shell de Django
python manage.py shell

# Ver SQL generado
python manage.py shell
>>> productos = Producto.objects.filter(precio__gt=50)
>>> print(productos.query)

# Crear y aplicar migraciones
python manage.py makemigrations
python manage.py migrate
```

## Recursos

- [Documentación Django ORM](https://docs.djangoproject.com/en/stable/topics/db/queries/)
- [QuerySet API Reference](https://docs.djangoproject.com/en/stable/ref/models/querysets/)
