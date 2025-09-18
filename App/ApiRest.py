from flask import Flask, jsonify, request
from ApiRestModels import db, Producto, Orden
from database import seed_database
import json
import math
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tienda.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()
    seed_database(app)

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "oLa cara de bOla"})

# PRODUCTOS ENDPOINTS

@app.route('/productos', methods=['GET'])
def get_productos():
    """Obtener lista de productos con paginación y filtros"""
    page = request.args.get('page', 1, type=int)
    size = request.args.get('size', 10, type=int)
    
    categoria = request.args.get('categoria')
    precio_min = request.args.get('precio_min', type=float)
    precio_max = request.args.get('precio_max', type=float)
    
    if page < 1:
        page = 1
    if size < 1 or size > 100:
        size = 10
    
    if precio_min is not None and precio_max is not None and precio_max < precio_min:
        return jsonify({'error': 'precio_max debe ser mayor o igual a precio_min'}), 400
    
    query = Producto.query
    
    if categoria:
        query = query.filter(Producto.categoria.ilike(f'%{categoria}%'))
    
    if precio_min is not None:
        query = query.filter(Producto.precio >= precio_min)
    
    if precio_max is not None:
        query = query.filter(Producto.precio <= precio_max)
    
    paginated = query.paginate(page=page, per_page=size, error_out=False)
    
    if page > paginated.pages and paginated.pages != 0:
        return jsonify({'error': 'Página no encontrada'}), 404
    
    return jsonify({
        'items': [producto.to_dict() for producto in paginated.items],
        'page': paginated.page,
        'size': paginated.per_page,
        'total': paginated.total,
        'pages': paginated.pages,
        'has_next': paginated.has_next,
        'has_prev': paginated.has_prev
    })

@app.route('/productos/<int:producto_id>', methods=['GET'])
def get_producto(producto_id):
    """Obtener detalles de un producto específico"""
    producto = Producto.query.get(producto_id)
    if not producto:
        return jsonify({'error': 'Producto no encontrado'}), 404
    
    return jsonify(producto.to_dict())

@app.route('/productos', methods=['POST'])
def create_producto():
    """Crear un nuevo producto"""
    data = request.json
    
    if not data.get('nombre') or not data.get('categoria'):
        return jsonify({'error': 'Faltan campos obligatorios: nombre, categoria'}), 400
    
    precio = data.get('precio')
    if precio is None or precio <= 0:
        return jsonify({'error': 'El precio debe ser mayor a 0'}), 400
    
    stock = data.get('stock')
    if stock is None or stock < 0:
        return jsonify({'error': 'El stock debe ser mayor o igual a 0'}), 400
    
    existing = Producto.query.filter_by(nombre=data['nombre']).first()
    if existing:
        return jsonify({'error': 'Ya existe un producto con este nombre'}), 400
    
    nuevo_producto = Producto(
        nombre=data['nombre'],
        precio=precio,
        stock=stock,
        categoria=data['categoria']
    )
    
    db.session.add(nuevo_producto)
    db.session.commit()
    
    return jsonify({
        'message': 'Producto creado exitosamente',
        'producto': nuevo_producto.to_dict()
    }), 201

@app.route('/productos/<int:producto_id>', methods=['PUT'])
def update_producto(producto_id):
    """Actualizar completamente un producto existente"""
    producto = Producto.query.get(producto_id)
    if not producto:
        return jsonify({'error': 'Producto no encontrado'}), 404
    
    data = request.json
    
    if not data.get('nombre') or not data.get('categoria'):
        return jsonify({'error': 'Faltan campos obligatorios: nombre, categoria'}), 400
    
    precio = data.get('precio')
    if precio is None or precio <= 0:
        return jsonify({'error': 'El precio debe ser mayor a 0'}), 400
    
    stock = data.get('stock')
    if stock is None or stock < 0:
        return jsonify({'error': 'El stock debe ser mayor o igual a 0'}), 400
    
    existing = Producto.query.filter(
        Producto.nombre == data['nombre'],
        Producto.id != producto_id
    ).first()
    if existing:
        return jsonify({'error': 'Ya existe otro producto con este nombre'}), 400
    
    producto.nombre = data['nombre']
    producto.precio = precio
    producto.stock = stock
    producto.categoria = data['categoria']
    
    db.session.commit()
    
    return jsonify({
        'message': 'Producto actualizado exitosamente',
        'producto': producto.to_dict()
    })

@app.route('/productos/<int:producto_id>', methods=['DELETE'])
def delete_producto(producto_id):
    """Eliminar un producto"""
    producto = Producto.query.get(producto_id)
    if not producto:
        return jsonify({'error': 'Producto no encontrado'}), 404
    
    db.session.delete(producto)
    db.session.commit()
    
    return jsonify({'message': 'Producto eliminado exitosamente'})

# ÓRDENES ENDPOINTS

@app.route('/ordenes', methods=['POST'])
def create_orden():
    """Crear una nueva orden"""
    data = request.json
    
    if not data.get('cliente') or not data.get('items'):
        return jsonify({'error': 'Faltan campos obligatorios: cliente, items'}), 400
    
    cliente = data['cliente']
    items = data['items']
    
    if not isinstance(items, list) or len(items) == 0:
        return jsonify({'error': 'Items debe ser una lista no vacía'}), 400
    
    total_calculado = 0.0
    
    for item in items:
        if not item.get('producto_id') or not item.get('cantidad'):
            return jsonify({'error': 'Cada item debe tener producto_id y cantidad'}), 400
        
        producto_id = item['producto_id']
        cantidad = item['cantidad']
        
        if cantidad <= 0:
            return jsonify({'error': 'La cantidad debe ser mayor a 0'}), 400
        
        producto = Producto.query.get(producto_id)
        if not producto:
            return jsonify({'error': f'Producto con ID {producto_id} no encontrado'}), 404
        
        if producto.stock < cantidad:
            return jsonify({
                'error': f'Stock insuficiente para {producto.nombre}. Disponible: {producto.stock}, Solicitado: {cantidad}'
            }), 409
        
        item_total = producto.precio * cantidad
        total_calculado += item_total
    
    for item in items:
        producto = Producto.query.get(item['producto_id'])
        producto.stock -= item['cantidad']
    
    nueva_orden = Orden(
        cliente=cliente,
        items=json.dumps(items),
        total_calculado=total_calculado
    )
    
    db.session.add(nueva_orden)
    db.session.commit()
    
    return jsonify({
        'message': 'Orden creada exitosamente',
        'orden': nueva_orden.to_dict()
    }), 201

@app.route('/ordenes', methods=['GET'])
def get_ordenes():
    """Obtener lista de órdenes con paginación y filtros"""
    page = request.args.get('page', 1, type=int)
    size = request.args.get('size', 10, type=int)
    
    cliente = request.args.get('cliente')
    fecha_desde_str = request.args.get('fecha_desde')
    fecha_hasta_str = request.args.get('fecha_hasta')
    
    if page < 1:
        page = 1
    if size < 1 or size > 100:
        size = 10
    
    fecha_desde = None
    fecha_hasta = None
    
    if fecha_desde_str:
        try:
            fecha_desde = datetime.fromisoformat(fecha_desde_str.replace('Z', '+00:00'))
        except ValueError:
            return jsonify({'error': 'Formato de fecha_desde inválido. Usa formato ISO'}), 400
    
    if fecha_hasta_str:
        try:
            fecha_hasta = datetime.fromisoformat(fecha_hasta_str.replace('Z', '+00:00'))
        except ValueError:
            return jsonify({'error': 'Formato de fecha_hasta inválido. Usa formato ISO'}), 400
    
    if fecha_desde and fecha_hasta and fecha_hasta < fecha_desde:
        return jsonify({'error': 'fecha_hasta debe ser mayor o igual a fecha_desde'}), 400
    
    query = Orden.query
    
    if cliente:
        query = query.filter(Orden.cliente.ilike(f'%{cliente}%'))
    
    if fecha_desde:
        query = query.filter(Orden.fecha >= fecha_desde)
    
    if fecha_hasta:
        query = query.filter(Orden.fecha <= fecha_hasta)
    
    paginated = query.paginate(page=page, per_page=size, error_out=False)
    
    if page > paginated.pages and paginated.pages != 0:
        return jsonify({'error': 'Página no encontrada'}), 404
    
    return jsonify({
        'items': [orden.to_dict() for orden in paginated.items],
        'page': paginated.page,
        'size': paginated.per_page,
        'total': paginated.total,
        'pages': paginated.pages,
        'has_next': paginated.has_next,
        'has_prev': paginated.has_prev
    })

@app.route('/ordenes/<int:orden_id>', methods=['GET'])
def get_orden(orden_id):
    """Obtener detalles de una orden específica"""
    orden = Orden.query.get(orden_id)
    if not orden:
        return jsonify({'error': 'Orden no encontrada'}), 404
    
    return jsonify(orden.to_dict())

if __name__ == '__main__':
    app.run(debug=True)