from app import app, db
from app.models import (Categoria, Ingrediente, Plato, RecetaPlato, Mesa, Pedido, DetallePedido)

with app.app_context():
    metadata = Categoria.metadata
    engine = db.engine
    for tabla in metadata.sorted_tables:
        print("--", tabla.name)
        
    metadata.create_all(bind=engine)
    print("creado correctamente")