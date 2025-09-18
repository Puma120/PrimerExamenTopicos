from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class Producto(db.Model):
    __tablename__ = "productos"
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), nullable=False, index=True)
    precio = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)
    categoria = db.Column(db.String(100), nullable=False, index=True)
    
    def __init__(self, nombre, precio, stock, categoria):
        self.nombre = nombre
        self.precio = precio
        self.stock = stock
        self.categoria = categoria
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'precio': self.precio,
            'stock': self.stock,
            'categoria': self.categoria
        }
    
    def __repr__(self):
        return f'<Producto {self.nombre}>'

class Orden(db.Model):
    __tablename__ = "ordenes"
    
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    cliente = db.Column(db.String(200), nullable=False, index=True)
    items = db.Column(db.Text, nullable=False)  
    total_calculado = db.Column(db.Float, nullable=False)
    
    def __init__(self, cliente, items, total_calculado):
        self.cliente = cliente
        self.items = items
        self.total_calculado = total_calculado
        self.fecha = datetime.now()
    
    def to_dict(self):
        return {
            'id': self.id,
            'fecha': self.fecha.isoformat(),
            'cliente': self.cliente,
            'items': json.loads(self.items),
            'total_calculado': self.total_calculado
        }
    
    def __repr__(self):
        return f'<Orden {self.id} - {self.cliente}>'