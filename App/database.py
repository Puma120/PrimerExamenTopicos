from ApiRestModels import db, Producto

def seed_database(app):
    with app.app_context():
        existing_products = Producto.query.count()
        if existing_products > 0:
            print(f"Database already has {existing_products} products. Skipping seed.")
            return
        
        productos_seed = [
            {"nombre": "Laptop Dell XPS 13", "precio": 1299.99, "stock": 15, "categoria": "Electrónicos"},
            {"nombre": "iPhone 14 Pro", "precio": 999.99, "stock": 25, "categoria": "Electrónicos"},
            {"nombre": "Audífonos Sony WH-1000XM4", "precio": 299.99, "stock": 40, "categoria": "Electrónicos"},
            {"nombre": "Teclado Mecánico Logitech", "precio": 149.99, "stock": 30, "categoria": "Accesorios"},
            {"nombre": "Mouse Gaming Razer", "precio": 79.99, "stock": 50, "categoria": "Accesorios"},
            {"nombre": "Monitor Samsung 27\"", "precio": 329.99, "stock": 20, "categoria": "Electrónicos"},
            {"nombre": "Silla de Oficina Ergonómica", "precio": 299.99, "stock": 12, "categoria": "Muebles"},
            {"nombre": "Escritorio de Madera", "precio": 199.99, "stock": 8, "categoria": "Muebles"},
            {"nombre": "Lámpara LED Escritorio", "precio": 45.99, "stock": 35, "categoria": "Iluminación"},
            {"nombre": "Cargador Inalámbrico", "precio": 39.99, "stock": 60, "categoria": "Accesorios"},
            {"nombre": "Tablet iPad Air", "precio": 599.99, "stock": 18, "categoria": "Electrónicos"},
            {"nombre": "Smartwatch Apple Watch", "precio": 399.99, "stock": 22, "categoria": "Electrónicos"},
            {"nombre": "Cámara Canon EOS R6", "precio": 2499.99, "stock": 5, "categoria": "Fotografía"},
            {"nombre": "Lente Canon 50mm f/1.8", "precio": 125.99, "stock": 10, "categoria": "Fotografía"},
            {"nombre": "Trípode Manfrotto", "precio": 89.99, "stock": 15, "categoria": "Fotografía"},
            {"nombre": "Mochila para Laptop", "precio": 59.99, "stock": 45, "categoria": "Accesorios"},
            {"nombre": "Disco Duro Externo 1TB", "precio": 79.99, "stock": 28, "categoria": "Almacenamiento"},
            {"nombre": "SSD Samsung 1TB", "precio": 109.99, "stock": 33, "categoria": "Almacenamiento"},
            {"nombre": "Router WiFi 6", "precio": 179.99, "stock": 16, "categoria": "Redes"},
            {"nombre": "Switch Ethernet 8 puertos", "precio": 29.99, "stock": 25, "categoria": "Redes"},
            {"nombre": "Webcam Logitech 4K", "precio": 199.99, "stock": 20, "categoria": "Accesorios"},
            {"nombre": "Micrófono Blue Yeti", "precio": 99.99, "stock": 14, "categoria": "Audio"},
            {"nombre": "Altavoces Bluetooth JBL", "precio": 79.99, "stock": 32, "categoria": "Audio"},
            {"nombre": "Cable USB-C 2m", "precio": 19.99, "stock": 100, "categoria": "Cables"},
            {"nombre": "Adaptador HDMI", "precio": 24.99, "stock": 55, "categoria": "Cables"}
        ]
        
        try:
            for producto_data in productos_seed:
                producto = Producto(**producto_data)
                db.session.add(producto)
            
            db.session.commit()
            print(f"Successfully seeded database with {len(productos_seed)} products")
            
        except Exception as e:
            db.session.rollback()
            print(f"Error seeding database: {e}")

if __name__ == "__main__":
    from flask import Flask
    
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tienda.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    with app.app_context():
        print("Creating tables...")
        db.create_all()
        print("Seeding database...")
        seed_database(app)
        print("Database setup complete!")