# API REST - Catálogo y Órdenes
# Pablo Urbina Macip - 198055
# 18/09/2025
## Descripción
Microservicio REST API para gestión de productos y órdenes de una tienda simple. Construido con Flask y Flask-SQLAlchemy con base de datos SQLite.

## Características
- CRUD completo de productos con paginación y filtros
- Gestión de órdenes con validación de stock
- Base de datos SQLite con datos semilla
- Validación de datos y manejo de errores
- API similar a la de referencia en la carpeta "anterior"

## Entidades

### Producto
- `id`: Identificador único (int)
- `nombre`: Nombre del producto (string, requerido)
- `precio`: Precio del producto (float, > 0)
- `stock`: Cantidad disponible (int, >= 0)
- `categoria`: Categoría del producto (string, requerido)

### Orden
- `id`: Identificador único (int)
- `fecha`: Fecha de creación (datetime)
- `cliente`: Nombre del cliente (string, requerido)
- `items`: Lista de productos y cantidades
- `total_calculado`: Total calculado automáticamente (float)

## Instalación y Configuración

### Prerrequisitos
- Python 3.8+
- pip

### Pasos de instalación

1. **Clonar el repositorio**
```bash
git clone <repository-url>
cd PrimerParcial_PabloUrbina
```

2. **Crear entorno virtual (recomendado)**
```bash
python -m venv venv
venv\Scripts\activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Inicializar base de datos**
```bash
cd App
python database.py
```

5. **Ejecutar la aplicación**
```bash
python ApiRest.py
```

La API estará disponible en: `http://localhost:5000`

## Endpoints

### Productos

#### GET /productos
Obtener lista de productos con paginación y filtros

**Parámetros de consulta:**
- `page` (int, opcional): Número de página (default: 1)
- `size` (int, opcional): Tamaño de página (default: 10, max: 100)
- `categoria` (string, opcional): Filtrar por categoría
- `precio_min` (float, opcional): Precio mínimo
- `precio_max` (float, opcional): Precio máximo

**Ejemplo de petición:**
```
GET /productos?page=1&size=5&categoria=Electrónicos&precio_min=100&precio_max=500
```

**Ejemplo de respuesta:**
```json
{
  "items": [
    {
      "id": 1,
      "nombre": "Laptop Dell XPS 13",
      "precio": 1299.99,
      "stock": 15,
      "categoria": "Electrónicos"
    }
  ],
  "page": 1,
  "size": 5,
  "total": 25,
  "pages": 5,
  "has_next": true,
  "has_prev": false
}
```

#### GET /productos/{id}
Obtener detalles de un producto específico

**Ejemplo de respuesta:**
```json
{
  "id": 1,
  "nombre": "Laptop Dell XPS 13",
  "precio": 1299.99,
  "stock": 15,
  "categoria": "Electrónicos"
}
```

#### POST /productos
Crear un nuevo producto

**Cuerpo de la petición:**
```json
{
  "nombre": "Nuevo Producto",
  "precio": 99.99,
  "stock": 10,
  "categoria": "Categoría"
}
```

**Ejemplo de respuesta:**
```json
{
  "message": "Producto creado exitosamente",
  "producto": {
    "id": 26,
    "nombre": "Nuevo Producto",
    "precio": 99.99,
    "stock": 10,
    "categoria": "Categoría"
  }
}
```

#### PUT /productos/{id}
Actualizar completamente un producto existente

**Cuerpo de la petición:**
```json
{
  "nombre": "Producto Actualizado",
  "precio": 149.99,
  "stock": 5,
  "categoria": "Nueva Categoría"
}
```

#### DELETE /productos/{id} (BONUS)
Eliminar un producto

**Ejemplo de respuesta:**
```json
{
  "message": "Producto eliminado exitosamente"
}
```

### Órdenes

#### POST /ordenes
Crear una nueva orden

**Cuerpo de la petición:**
```json
{
  "cliente": "Juan Pérez",
  "items": [
    {
      "producto_id": 1,
      "cantidad": 2
    },
    {
      "producto_id": 3,
      "cantidad": 1
    }
  ]
}
```

**Ejemplo de respuesta:**
```json
{
  "message": "Orden creada exitosamente",
  "orden": {
    "id": 1,
    "fecha": "2024-01-15T10:30:00.123456",
    "cliente": "Juan Pérez",
    "items": [
      {
        "producto_id": 1,
        "cantidad": 2
      },
      {
        "producto_id": 3,
        "cantidad": 1
      }
    ],
    "total_calculado": 2899.97
  }
}
```

#### GET /ordenes
Obtener lista de órdenes con paginación y filtros

**Parámetros de consulta:**
- `page` (int, opcional): Número de página
- `size` (int, opcional): Tamaño de página
- `cliente` (string, opcional): Filtrar por cliente
- `fecha_desde` (datetime ISO, opcional): Fecha desde
- `fecha_hasta` (datetime ISO, opcional): Fecha hasta

**Ejemplo de petición:**
```
GET /ordenes?page=1&size=10&cliente=Juan&fecha_desde=2024-01-01T00:00:00&fecha_hasta=2024-12-31T23:59:59
```

#### GET /ordenes/{id}
Obtener detalles de una orden específica

## Validaciones y Errores

### Códigos de estado HTTP
- `200`: Operación exitosa
- `201`: Recurso creado exitosamente
- `400`: Error de validación o datos inválidos
- `404`: Recurso no encontrado
- `409`: Conflicto (ej: stock insuficiente)

### Ejemplos de errores

**Stock insuficiente (409):**
```json
{
  "error": "Stock insuficiente para Laptop Dell XPS 13. Disponible: 5, Solicitado: 10"
}
```

**Producto no encontrado (404):**
```json
{
  "error": "Producto no encontrado"
}
```

**Validación de precio (400):**
```json
{
  "error": "precio_max debe ser mayor o igual a precio_min"
}
```

## Estructura del Proyecto

```
App/
├── ApiRest.py          # Aplicación principal Flask
├── ApiRestModels.py    # Modelos SQLAlchemy
├── database.py         # Configuración de BD y datos semilla
└── tienda.db          # Base de datos SQLite (se crea automáticamente)

requirements.txt        # Dependencias del proyecto
README.md              # Este archivo
```

## Datos Semilla

La aplicación incluye 25 productos de ejemplo en diferentes categorías:
- Electrónicos (laptops, teléfonos, tablets, etc.)
- Accesorios (teclados, ratones, mochilas, etc.)
- Muebles (sillas, escritorios)
- Audio (audífonos, altavoces)
- Fotografía (cámaras, lentes)
- Y más...

## Tecnologías Utilizadas

- **Flask**: Framework web ligero para Python
- **Flask-SQLAlchemy**: ORM para manejo de base de datos
- **SQLite**: Base de datos ligera
- **JSON**: Para serialización de datos
- **datetime**: Para manejo de fechas
- **math**: Para cálculos de paginación

## Pruebas

Para probar la API, puedes usar herramientas como:
- Postman
- curl
- Navegador web (para endpoints GET)

## Contribución

1. Fork el proyecto
2. Crear una rama para la nueva característica
3. Commit de los cambios
4. Push a la rama
5. Crear un Pull Request

## Licencia

Este proyecto es parte de un examen académico.