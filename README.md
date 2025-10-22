# 🐍 Django ORM - Guía Completa de Ejercicios

Repositorio con ejercicios prácticos para dominar el ORM de Django, desde consultas básicas hasta procedimientos almacenados.

## 📋 Tabla de Contenidos

- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Modelo Base](#modelo-base)
- [Ejercicios](#ejercicios)
  - [1. Recuperando Registros](#1-recuperando-registros-con-django-orm)
  - [2. Aplicando Filtros](#2-aplicando-filtros-en-recuperación-de-registros)
  - [3. Queries SQL con raw()](#3-ejecutando-queries-sql-desde-django)
  - [4. Mapeando Campos](#4-mapeando-campos-de-consultas-al-modelo)
  - [5. Índices](#5-realizando-búsquedas-de-índice)
  - [6. Exclusión de Campos](#6-exclusión-de-campos-del-modelo)
  - [7. Anotaciones](#7-añadiendo-anotaciones-en-consultas)
  - [8. Parámetros en raw()](#8-pasando-parámetros-a-raw)
  - [9. SQL Personalizado](#9-ejecutando-sql-personalizado-directamente)
  - [10. Conexiones y Cursores](#10-conexiones-y-cursores)
  - [11. Procedimientos Almacenados](#11-invocación-a-procedimientos-almacenados)
- [Recursos Adicionales](#recursos-adicionales)

## 🔧 Requisitos

- Python 3.8+
- Django 4.0+
- Base de datos (SQLite, PostgreSQL, MySQL)

```bash
pip install django
```

## 🚀 Instalación

1. **Clona el repositorio**
```bash
git clone https://github.com/moisesdatasci/django-orm-ejercicios.git
cd django-orm-ejercicios
```

2. **Crea un entorno virtual**
```bash
python -m venv venv
venv\Scripts\activate
```

3. **Instala las dependencias**
```bash
pip install -r requirements.txt
```

4. **Configura la base de datos**
```bash
python manage.py migrate
```

5. **Carga datos de ejemplo (opcional)**
```bash
python manage.py loaddata productos_iniciales.json
```

## 📦 Modelo Base

```python
# models.py
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
        return f"{self.nombre} - ${self.precio}"
```

## 📚 Ejercicios

### 1. Recuperando Registros con Django ORM

**Objetivo:** Obtener todos los registros de la tabla Producto.

```python
from productos.models import Producto

# Obtener todos los productos
productos = Producto.objects.all()

# Iterar sobre los resultados
for producto in productos:
    print(f"{producto.nombre} - ${producto.precio}")
```

**Comandos importantes:**
- `.all()` - Todos los registros
- `.count()` - Contar registros
- `.first()` - Primer registro
- `.last()` - Último registro

---

### 2. Aplicando Filtros en Recuperación de Registros

**Objetivo:** Filtrar productos según diferentes criterios.

```python
# Productos con precio mayor a 50
productos_caros = Producto.objects.filter(precio__gt=50)

# Productos cuyo nombre empiece con "A"
productos_con_a = Producto.objects.filter(nombre__startswith='A')

# Productos disponibles
productos_disponibles = Producto.objects.filter(disponible=True)

# Combinando filtros
productos_filtrados = Producto.objects.filter(
    precio__gte=20,
    precio__lte=100,
    disponible=True
)
```

**Operadores de filtro:**
- `__gt` - Mayor que (>)
- `__gte` - Mayor o igual que (>=)
- `__lt` - Menor que (<)
- `__lte` - Menor o igual que (<=)
- `__exact` - Igual exacto
- `__iexact` - Igual (case-insensitive)
- `__contains` - Contiene
- `__startswith` - Empieza con
- `__endswith` - Termina con

---

### 3. Ejecutando Queries SQL desde Django

**Objetivo:** Ejecutar consultas SQL personalizadas usando `raw()`.

```python
# Consulta SQL básica
productos = Producto.objects.raw('SELECT * FROM productos_producto WHERE precio < 100')

# Iterar sobre resultados
for producto in productos:
    print(f"{producto.nombre} - ${producto.precio}")
```

⚠️ **Nota:** Reemplaza `productos_producto` con el nombre real de tu tabla (formato: `app_modelo`).

---

### 4. Mapeando Campos de Consultas al Modelo

**Objetivo:** Mapear resultados SQL personalizados a instancias del modelo.

```python
# Consulta con campos específicos
query = '''
    SELECT id, nombre, precio, disponible 
    FROM productos_producto 
    WHERE precio BETWEEN %s AND %s
'''

productos = Producto.objects.raw(query, [20, 80])

# Django mapea automáticamente los campos
for producto in productos:
    print(f"ID: {producto.id}")
    print(f"Nombre: {producto.nombre}")
    print(f"Precio: ${producto.precio}")
```

🔑 **Importante:** La consulta SQL debe incluir el campo `id` (clave primaria).

---

### 5. Realizando Búsquedas de Índice

**Objetivo:** Crear índices para mejorar el rendimiento de búsquedas.

**¿Qué son los índices?**
Los índices son estructuras que aceleran las búsquedas en bases de datos, similar al índice de un libro.

```python
# En models.py
class Producto(models.Model):
    nombre = models.CharField(max_length=100, db_index=True)
    precio = models.DecimalField(max_digits=5, decimal_places=2)
    disponible = models.BooleanField(default=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['nombre'], name='idx_producto_nombre'),
            models.Index(fields=['precio', 'disponible'], name='idx_precio_disponible'),
        ]
```

**Aplicar cambios:**
```bash
python manage.py makemigrations
python manage.py migrate
```

**Verificar impacto:**
```python
# La búsqueda será más rápida con índice
productos = Producto.objects.filter(nombre__startswith='A')
```

---

### 6. Exclusión de Campos del Modelo

**Objetivo:** Optimizar consultas excluyendo campos innecesarios.

```python
# Excluir campo específico
productos = Producto.objects.defer('disponible')

# Incluir solo campos específicos
productos = Producto.objects.only('nombre', 'precio')

# Ejemplo de uso
for producto in productos:
    print(f"{producto.nombre}: ${producto.precio}")
    # ⚠️ Acceder a producto.disponible generará una consulta adicional
```

**Diferencias:**
- `defer()` - Excluye campos (carga diferida)
- `only()` - Solo carga los campos especificados
- `values()` - Retorna diccionarios en lugar de instancias
- `values_list()` - Retorna tuplas

---

### 7. Añadiendo Anotaciones en Consultas

**Objetivo:** Agregar campos calculados a las consultas.

```python
from django.db.models import F, DecimalField, ExpressionWrapper

# Calcular precio con 16% de impuesto
productos = Producto.objects.annotate(
    precio_con_impuesto=ExpressionWrapper(
        F('precio') * 1.16,
        output_field=DecimalField(max_digits=7, decimal_places=2)
    )
)

# Mostrar resultados
for producto in productos:
    print(f"{producto.nombre}")
    print(f"  Precio base: ${producto.precio}")
    print(f"  Con impuesto: ${producto.precio_con_impuesto}")
```

**Otras anotaciones útiles:**
```python
from django.db.models import Count, Sum, Avg, Max, Min

# Ejemplos con agregaciones
from django.db.models import Count
productos_stats = Producto.objects.aggregate(
    total=Count('id'),
    precio_promedio=Avg('precio'),
    precio_max=Max('precio')
)
```

---

### 8. Pasando Parámetros a `raw()`

**Objetivo:** Usar parámetros seguros en consultas SQL.

```python
# ❌ INCORRECTO - Vulnerable a SQL Injection
precio_limite = 50
productos = Producto.objects.raw(
    f'SELECT * FROM productos_producto WHERE precio < {precio_limite}'
)

# ✅ CORRECTO - Usando parámetros seguros
precio_limite = 50
productos = Producto.objects.raw(
    'SELECT * FROM productos_producto WHERE precio < %s',
    [precio_limite]
)

# Con múltiples parámetros
precio_min = 20
precio_max = 100
productos = Producto.objects.raw(
    'SELECT * FROM productos_producto WHERE precio BETWEEN %s AND %s',
    [precio_min, precio_max]
)
```

**Beneficios:**
- ✅ Previene SQL Injection
- ✅ Django escapa automáticamente los valores
- ✅ Código más seguro y mantenible

---

### 9. Ejecutando SQL Personalizado Directamente

**Objetivo:** Ejecutar operaciones SQL complejas con `cursor()`.

```python
from django.db import connection

def operaciones_sql():
    with connection.cursor() as cursor:
        # INSERT
        cursor.execute(
            "INSERT INTO productos_producto (nombre, precio, disponible) VALUES (%s, %s, %s)",
            ["Laptop", 999.99, True]
        )
        
        # UPDATE
        cursor.execute(
            "UPDATE productos_producto SET precio = %s WHERE nombre = %s",
            [899.99, "Laptop"]
        )
        
        # DELETE
        cursor.execute(
            "DELETE FROM productos_producto WHERE precio > %s",
            [1000]
        )
        
        # SELECT personalizado
        cursor.execute(
            "SELECT nombre, precio FROM productos_producto WHERE disponible = %s",
            [True]
        )
        rows = cursor.fetchall()
        
        for row in rows:
            print(f"{row[0]}: ${row[1]}")
```

**Cuándo usar:**
- Consultas muy complejas
- Operaciones en lote masivas
- Funciones específicas de la BD
- Máximo rendimiento requerido

---

### 10. Conexiones y Cursores

**Objetivo:** Trabajar directamente con cursores de base de datos.

```python
from django.db import connection

def consulta_con_cursor():
    with connection.cursor() as cursor:
        # Ejecutar consulta
        cursor.execute(
            "SELECT * FROM productos_producto WHERE precio < %s",
            [100]
        )
        
        # Obtener nombres de columnas
        columns = [col[0] for col in cursor.description]
        
        # Obtener todas las filas
        rows = cursor.fetchall()
        
        # Convertir a diccionarios
        for row in rows:
            producto_dict = dict(zip(columns, row))
            print(producto_dict)
```

**Métodos del cursor:**
- `cursor.execute()` - Ejecutar SQL
- `cursor.fetchone()` - Obtener una fila
- `cursor.fetchall()` - Obtener todas las filas
- `cursor.fetchmany(size)` - Obtener N filas
- `cursor.description` - Metadatos de las columnas

**Ventajas vs Desventajas:**

| Ventajas | Desventajas |
|----------|-------------|
| Control total sobre SQL | Código menos portable |
| Mejor rendimiento en operaciones masivas | Sin validación de modelos |
| Acceso a funciones específicas de BD | Más propenso a errores |
| | Pierdes funcionalidades del ORM |

---

### 11. Invocación a Procedimientos Almacenados

**Objetivo:** Llamar procedimientos almacenados desde Django.

**Crear procedimiento (PostgreSQL):**
```sql
CREATE OR REPLACE PROCEDURE actualizar_precio_producto(
    p_id INTEGER,
    p_nuevo_precio DECIMAL
)
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE productos_producto 
    SET precio = p_nuevo_precio 
    WHERE id = p_id;
END;
$$;
```

**Invocar desde Django:**
```python
from django.db import connection

def llamar_procedimiento():
    with connection.cursor() as cursor:
        # Llamar procedimiento almacenado
        cursor.callproc('actualizar_precio_producto', [1, 149.99])
        
        print("✅ Procedimiento ejecutado correctamente")

# Para procedimientos que retornan datos
def obtener_datos_procedimiento():
    with connection.cursor() as cursor:
        cursor.callproc('obtener_productos_caros', [100])
        results = cursor.fetchall()
        
        for row in results:
            print(row)
```

**¿Qué son los procedimientos almacenados?**
Rutinas SQL guardadas en la base de datos que se pueden reutilizar, ofreciendo:
- ✅ Mejor rendimiento
- ✅ Lógica centralizada
- ✅ Reducción de tráfico de red
- ✅ Seguridad mejorada

---

## 🧪 Script de Prueba Completo

```python
# test_orm.py
from django.db import connection
from productos.models import Producto
from django.db.models import F, DecimalField, ExpressionWrapper

def demo_completo():
    print("🚀 Iniciando demostración completa\n")
    
    # Limpiar datos anteriores
    Producto.objects.all().delete()
    
    # 1. Crear productos de ejemplo
    productos_ejemplo = [
        Producto(nombre="Laptop Dell", precio=850.00, disponible=True),
        Producto(nombre="Mouse Logitech", precio=25.50, disponible=True),
        Producto(nombre="Teclado Mecánico", precio=45.00, disponible=False),
        Producto(nombre="Monitor Samsung", precio=320.00, disponible=True),
        Producto(nombre="Auriculares Sony", precio=75.00, disponible=True),
    ]
    Producto.objects.bulk_create(productos_ejemplo)
    print("✅ Productos creados\n")
    
    # 2. Recuperar todos
    todos = Producto.objects.all()
    print(f"📦 Total productos: {todos.count()}\n")
    
    # 3. Filtros
    caros = Producto.objects.filter(precio__gt=50)
    print(f"💰 Productos > $50: {caros.count()}")
    for p in caros:
        print(f"   - {p.nombre}: ${p.precio}")
    
    # 7. Anotaciones
    con_impuesto = Producto.objects.annotate(
        precio_con_impuesto=ExpressionWrapper(
            F('precio') * 1.16,
            output_field=DecimalField(max_digits=7, decimal_places=2)
        )
    )
    
    print("\n📊 Precios con 16% de impuesto:")
    for p in con_impuesto:
        print(f"   {p.nombre}: ${p.precio} → ${p.precio_con_impuesto}")
    
    print("\n✨ Demostración completada")

if __name__ == '__main__':
    demo_completo()
```

**Ejecutar:**
```bash
python manage.py shell < test_orm.py
```

---

## 📊 Comparativa de Métodos

| Método | Uso | Ventajas | Desventajas |
|--------|-----|----------|-------------|
| ORM (.filter, .all) | Consultas estándar | Seguro, portable, pythonic | Menos control |
| .raw() | SQL personalizado simple | Más control, sigue usando modelos | SQL directo |
| cursor() | Operaciones complejas | Control total, máximo rendimiento | Sin ORM, menos seguro |
| Procedimientos | Lógica compleja en BD | Muy rápido, reutilizable | Específico de BD |

---

## 🎯 Mejores Prácticas

1. **Seguridad**
   - ✅ Siempre usa parámetros en consultas SQL
   - ✅ Nunca concatenes valores directamente en SQL
   - ✅ Valida datos antes de guardar

2. **Rendimiento**
   - ✅ Usa `select_related()` y `prefetch_related()` para optimizar relaciones
   - ✅ Crea índices en campos de búsqueda frecuente
   - ✅ Usa `only()` y `defer()` cuando no necesites todos los campos

3. **Mantenibilidad**
   - ✅ Prefiere el ORM sobre SQL directo cuando sea posible
   - ✅ Documenta consultas SQL complejas
   - ✅ Escribe tests para tus consultas

4. **Optimización**
   ```python
   # ❌ Malo: N+1 queries
   productos = Producto.objects.all()
   for p in productos:
       print(p.categoria.nombre)  # Query por cada producto
   
   # ✅ Bueno: 1 query
   productos = Producto.objects.select_related('categoria').all()
   for p in productos:
       print(p.categoria.nombre)
   ```

---

## 🛠️ Comandos Útiles

```bash
# Abrir shell de Django
python manage.py shell

# Ver SQL generado por el ORM
python manage.py shell
>>> from django.db import connection
>>> from productos.models import Producto
>>> productos = Producto.objects.filter(precio__gt=50)
>>> print(productos.query)

# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Ver migraciones
python manage.py showmigrations

# Ver SQL de una migración
python manage.py sqlmigrate productos 0001
```

---

## 📖 Recursos Adicionales

- [Documentación Oficial de Django ORM](https://docs.djangoproject.com/en/stable/topics/db/queries/)
- [Django Database API Reference](https://docs.djangoproject.com/en/stable/ref/models/querysets/)
- [Making Queries - Django Docs](https://docs.djangoproject.com/en/stable/topics/db/queries/)
- [Query Expressions](https://docs.djangoproject.com/en/stable/ref/models/expressions/)

---

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add: nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

---

## ✨ Autor

Tu Nombre - [@tu_usuario](https://github.com/tu-usuario)

Proyecto: [https://github.com/tu-usuario/django-orm-ejercicios](https://github.com/tu-usuario/django-orm-ejercicios)

---

## ⭐ Agradecimientos

- Documentación oficial de Django
- Comunidad de Django en español
- Todos los contribuidores

---

**¿Encontraste útil este repositorio? ¡Dale una ⭐️ en GitHub!**
