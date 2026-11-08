from datetime import datetime
from flask_appbuilder import Model
from sqlalchemy import Boolean, Column, Date, DateTime, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship


class Categoria(Model):
    __tablename__ = "categorias"
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), unique=True, nullable=False)
    descripcion = Column(String(250), nullable=True)
    tipo = Column(String(20), default="Plato", nullable=False)  
    activo = Column(Boolean, default=True, nullable=False)

    ingredientes = relationship(
        "Ingrediente",
        back_populates="categoria"
    )
    platos = relationship(
        "Plato",
        back_populates="categoria"
    )

    def __repr__(self):
        return self.nombre


class Ingrediente(Model):
    __tablename__ = "ingredientes"
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), unique=True, nullable=False)
    categoria_id = Column(Integer, ForeignKey("categorias.id"), nullable=False)
    cantidad = Column(Numeric(12, 2), default=0, nullable=False)
    unidad_medida = Column(String(20), nullable=False)
    costo_unitario = Column(Numeric(12, 2), default=0, nullable=False)
    stock_minimo = Column(Numeric(12, 2), default=0, nullable=False)
    fecha_vencimiento = Column(Date, nullable=False)
    activo = Column(Boolean, default=True, nullable=False)

    categoria = relationship(
        "Categoria",
        back_populates="ingredientes"
    )
    recetas = relationship(
        "RecetaPlato",
        back_populates="ingrediente"
    )

    def __repr__(self):
        return self.nombre


class Plato(Model):
    __tablename__ = "platos"
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), unique=True, nullable=False)
    descripcion = Column(String(250), nullable=True)
    precio = Column(Numeric(12, 2), default=0, nullable=False)
    categoria_id = Column(Integer, ForeignKey("categorias.id"), nullable=False)
    activo = Column(Boolean, default=True, nullable=False)

    categoria = relationship(
        "Categoria",
        back_populates="platos"
    )
    receta = relationship(
        "RecetaPlato",
        back_populates="plato"
    )
    detalles = relationship(
        "DetallePedido",
        back_populates="plato"
    )

    def __repr__(self):
        return self.nombre


class RecetaPlato(Model):
    __tablename__ = "recetas_platos"
    id = Column(Integer, primary_key=True)
    plato_id = Column(Integer, ForeignKey("platos.id"), nullable=False)
    ingrediente_id = Column(Integer, ForeignKey("ingredientes.id"), nullable=False)
    cantidad_requerida = Column(Numeric(12, 2), nullable=False)

    plato = relationship(
        "Plato",
        back_populates="receta"
    )
    ingrediente = relationship(
        "Ingrediente",
        back_populates="recetas"
    )

    def __repr__(self):
        return f"{self.plato} - {self.ingrediente}"


class Mesa(Model):
    __tablename__ = "mesas"
    id = Column(Integer, primary_key=True)
    numero = Column(Integer, unique=True, nullable=False)
    capacidad = Column(Integer, default=4, nullable=False)
    estado = Column(String(20), default="libre", nullable=False)  

    pedidos = relationship(
        "Pedido",
        back_populates="mesa"
    )

    def __repr__(self):
        return f"Mesa {self.numero}"


class Pedido(Model):
    __tablename__ = "pedidos"
    id = Column(Integer, primary_key=True)
    fecha = Column(DateTime, default=datetime.now, nullable=False)
    estado = Column(String(20), default="abierto", nullable=False)  
    total = Column(Numeric(12, 2), default=0, nullable=False)
    mesa_id = Column(Integer, ForeignKey("mesas.id"), nullable=False)
    usuario_id = Column(Integer, ForeignKey("ab_user.id"), nullable=False)

    mesa = relationship(
        "Mesa",
        back_populates="pedidos"
    )
    usuario = relationship("User")
    detalles = relationship(
        "DetallePedido",
        back_populates="pedido"
    )

    def __repr__(self):
        return f"Pedido #{self.id}"


class DetallePedido(Model):
    __tablename__ = "detalles_pedido"
    id = Column(Integer, primary_key=True)
    pedido_id = Column(Integer, ForeignKey("pedidos.id"), nullable=False)
    plato_id = Column(Integer, ForeignKey("platos.id"), nullable=False)
    cantidad = Column(Integer, default=1, nullable=False)
    precio_unitario = Column(Numeric(12, 2), nullable=False)

    pedido = relationship(
        "Pedido",
        back_populates="detalles"
    )
    plato = relationship(
        "Plato",
        back_populates="detalles"
    )

    def subtotal(self):
        return self.cantidad * self.precio_unitario

    def __repr__(self):
        return f"{self.plato} x{self.cantidad}"