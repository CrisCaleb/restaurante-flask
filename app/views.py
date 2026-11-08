from flask import g
from flask_appbuilder  import BaseView, ModelView, expose
from flask_appbuilder.models.sqla.interface import SQLAInterface
from . import appbuilder
from .models import (Categoria, Ingrediente, Plato, RecetaPlato,
                     Mesa, Pedido, DetallePedido)


class CategoriaView(ModelView):
    datamodel = SQLAInterface(Categoria)

    label_columns = {"nombre": "Nombre",
                     "descripcion": "Descripcion",
                     "tipo": "Tipo",
                     "activo": "Activo",
                     "ingredientes": "Ingredientes",
                     "platos": "Platos"
                    }

    list_columns = ["nombre", "descripcion", "tipo", "activo"]

    show_columns = ["id", "nombre", "descripcion", "tipo", "activo", "ingredientes", "platos"]

    add_columns = ["nombre", "descripcion", "tipo", "activo"]

    edit_columns = ["nombre", "descripcion", "tipo", "activo"]

    search_columns = ["nombre", "tipo"]
    order_columns = ["nombre"]


class IngredienteView(ModelView):
    datamodel = SQLAInterface(Ingrediente)

    label_columns = {"nombre": "Nombre",
                     "categoria": "Categoria",
                     "cantidad": "Cantidad",
                     "unidad_medida": "Unidad de Medida",
                     "costo_unitario": "Costo Unitario",
                     "stock_minimo": "Stock Minimo",
                     "fecha_vencimiento": "Fecha de Vencimiento",
                     "activo": "Activo"
                    }

    list_columns = ["nombre",
                    "categoria",
                    "cantidad",
                    "unidad_medida",
                    "costo_unitario",
                    "stock_minimo",
                    "fecha_vencimiento",
                    "activo"]

    show_columns = ["id", "nombre",
                    "categoria",
                    "cantidad",
                    "unidad_medida",
                    "costo_unitario",
                    "stock_minimo",
                    "fecha_vencimiento",
                    "activo"]

    add_columns = ["nombre",
                   "categoria",
                   "cantidad",
                   "unidad_medida",
                   "costo_unitario",
                   "stock_minimo",
                   "fecha_vencimiento",
                   "activo"]

    edit_columns = add_columns
    search_columns = ["nombre", "categoria"]
    order_columns = ["nombre"]


class PlatoView(ModelView):
    datamodel = SQLAInterface(Plato)

    label_columns = {"nombre": "Nombre",
                     "descripcion": "Descripcion",
                     "precio": "Precio",
                     "categoria": "Categoria",
                     "activo": "Activo",
                     "receta": "Receta"
                    }

    list_columns = ["nombre", "categoria", "precio", "activo"]

    show_columns = ["id", "nombre", "descripcion", "categoria", "precio", "activo"]

    add_columns = ["nombre", "descripcion", "categoria", "precio", "activo"]

    edit_columns = add_columns
    search_columns = ["nombre", "categoria"]
    order_columns = ["nombre", "precio"]


class RecetaPlatoView(ModelView):
    datamodel = SQLAInterface(RecetaPlato)

    label_columns = {"plato": "Plato",
                     "ingrediente": "Ingrediente",
                     "cantidad_requerida": "Cantidad Requerida"
                    }

    list_columns = ["plato", "ingrediente", "cantidad_requerida"]

    show_columns = ["id", "plato", "ingrediente", "cantidad_requerida"]

    add_columns = ["plato", "ingrediente", "cantidad_requerida"]

    edit_columns = add_columns
    search_columns = ["plato", "ingrediente"]


class MesaView(ModelView):
    datamodel = SQLAInterface(Mesa)

    label_columns = {"numero": "Numero",
                     "capacidad": "Capacidad",
                     "estado": "Estado"
                    }

    list_columns = ["numero", "capacidad", "estado"]

    show_columns = ["id", "numero", "capacidad", "estado"]

    add_columns = ["numero", "capacidad", "estado"]

    edit_columns = add_columns
    search_columns = ["numero", "estado"]
    order_columns = ["numero"]


class DetallePedidoView(ModelView):
    datamodel = SQLAInterface(DetallePedido)

    label_columns = {"pedido": "Pedido",
                     "plato": "Plato",
                     "cantidad": "Cantidad",
                     "precio_unitario": "Precio Unitario"
                    }

    list_columns = ["pedido", "plato", "cantidad", "precio_unitario"]

    show_columns = ["id", "pedido", "plato", "cantidad", "precio_unitario"]

    add_columns = ["pedido", "plato", "cantidad"]

    edit_columns = add_columns
    search_columns = ["pedido", "plato"]

    def _recalcular_total(self, item):
        session = self.datamodel.session
        pedido = session.query(Pedido).get(item.pedido_id)
        detalles = session.query(DetallePedido).filter_by(pedido_id=item.pedido_id).all()
        pedido.total = sum(d.cantidad * d.precio_unitario for d in detalles)
        session.commit()

    def pre_add(self, item):
        item.precio_unitario = item.plato.precio

    def pre_update(self, item):
        item.precio_unitario = item.plato.precio

    def post_add(self, item):
        self._recalcular_total(item)

    def post_update(self, item):
        self._recalcular_total(item)

    def post_delete(self, item):
        self._recalcular_total(item)


class PedidoView(ModelView):
    datamodel = SQLAInterface(Pedido)

    related_views = [DetallePedidoView]

    label_columns = {"fecha": "Fecha",
                     "mesa": "Mesa",
                     "usuario": "Atendido por",
                     "estado": "Estado",
                     "total": "Total"
                    }

    list_columns = ["id", "fecha", "mesa", "usuario", "estado", "total"]

    show_columns = ["id", "fecha", "mesa", "usuario", "estado", "total"]

    add_columns = ["mesa", "estado"]

    edit_columns = ["mesa", "estado"]

    search_columns = ["mesa", "estado", "fecha"]
    order_columns = ["fecha", "total"]

    def pre_add(self, item):
        item.usuario_id = g.user.id


# Registro
appbuilder.add_view(
        CategoriaView,
        "Modulo categorias",
        icon = "fa-tags",
        category = "Inventario"
)

appbuilder.add_view(
        IngredienteView,
        "Modulo Ingredientes",
        icon = "fa-cubes",
        category = "Inventario"
)

appbuilder.add_view(
        PlatoView,
        "Modulo Platos",
        icon = "fa-cutlery",
        category = "Menu"
)

appbuilder.add_view(
        RecetaPlatoView,
        "Modulo Recetas",
        icon = "fa-book",
        category = "Menu"
)

appbuilder.add_view(
        MesaView,
        "Modulo Mesas",
        icon = "fa-table",
        category = "Ventas"
)

appbuilder.add_view(
        PedidoView,
        "Modulo Pedidos",
        icon = "fa-shopping-cart",
        category = "Ventas"
)

appbuilder.add_view(
        DetallePedidoView,
        "Modulo Detalle Pedidos",
        icon = "fa-list",
        category = "Ventas"
)


class DashboardView(BaseView):
    route_base = "/dashboard"
    default_view= "index"

    @expose("/")
    def index(self):
        return self.render_template('dashboard.html')

appbuilder.add_view(
    DashboardView,
    "Dashboard",
    icon = "fa-dashboard",
    category = "Menu principal"
)