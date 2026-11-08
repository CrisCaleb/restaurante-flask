from flask import g
from flask_appbuilder  import BaseView, ModelView, expose
from flask_appbuilder.models.sqla.interface import SQLAInterface
from . import appbuilder
from .extensions import db
from .models import (Categoria, Ingrediente, Plato, RecetaPlato, Mesa, Pedido, DetallePedido)


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

from flask import render_template_string
from sqlalchemy import func


class ReporteStockBajoView(BaseView):
    route_base = "/reporte-stock-bajo"
    default_view = "index"

    @expose("/")
    def index(self):
        # Consulta: Ingredientes donde la cantidad es menor o igual al stock mínimo
        ingredientes_bajos = db.session.query(Ingrediente).filter(
            Ingrediente.cantidad <= Ingrediente.stock_minimo,
            Ingrediente.activo == True
        ).all()
        
        html = """
        <h2>Reporte: Ingredientes con Stock Bajo o Crítico</h2>
        <table class="table table-bordered table-striped">
            <thead>
                <tr><th>Ingrediente</th><th>Categoría</th><th>Stock Actual</th><th>Stock Mínimo</th><th>Unidad</th></tr>
            </thead>
            <tbody>
                {% for ing in ingredientes %}
                <tr>
                    <td>{{ ing.nombre }}</td>
                    <td>{{ ing.categoria.nombre }}</td>
                    <td class="text-danger"><strong>{{ ing.cantidad }}</strong></td>
                    <td>{{ ing.stock_minimo }}</td>
                    <td>{{ ing.unidad_medida }}</td>
                </tr>
                {% else %}
                <tr><td colspan="5" class="text-center">No hay ingredientes con stock bajo. ¡Excelente gestión!</td></tr>
                {% endfor %}
            </tbody>
        </table>
        <a href="/" class="btn btn-primary">Volver al Inicio</a>
        """
        return render_template_string(html, ingredientes=ingredientes_bajos)


class ReporteVentasPorFechaView(BaseView):
    route_base = "/reporte-ventas"
    default_view = "index"

    @expose("/", methods=['GET', 'POST'])
    def index(self):
        from flask import request
        fecha_inicio = request.form.get('fecha_inicio')
        fecha_fin = request.form.get('fecha_fin')
        
        query = db.session.query(Pedido)
        if fecha_inicio and fecha_fin:
            query = query.filter(Pedido.fecha >= fecha_inicio, Pedido.fecha <= fecha_fin)
        
        pedidos = query.filter(Pedido.estado == 'cerrado').order_by(Pedido.fecha.desc()).all()
        total_ventas = sum(p.total for p in pedidos)

        html = """
        <h2>Reporte: Ventas por Rango de Fechas</h2>
        <form method="POST" class="form-inline mb-3">
            <input type="date" name="fecha_inicio" class="form-control mr-2" required>
            <input type="date" name="fecha_fin" class="form-control mr-2" required>
            <button type="submit" class="btn btn-success">Filtrar</button>
        </form>
        <h4 class="text-primary">Total Vendido en el período: Bs {{ total_ventas }}</h4>
        <table class="table table-bordered table-striped mt-3">
            <thead>
                <tr><th>ID Pedido</th><th>Fecha</th><th>Mesa</th><th>Atendido por</th><th>Total</th><th>Estado</th></tr>
            </thead>
            <tbody>
                {% for p in pedidos %}
                <tr>
                    <td>{{ p.id }}</td>
                    <td>{{ p.fecha.strftime('%d/%m/%Y %H:%M') }}</td>
                    <td>{{ p.mesa.numero }}</td>
                    <td>{{ p.usuario.first_name }} {{ p.usuario.last_name }}</td>
                    <td>Bs {{ p.total }}</td>
                    <td><span class="badge badge-success">{{ p.estado }}</span></td>
                </tr>
                {% else %}
                <tr><td colspan="6" class="text-center">No se encontraron ventas en ese rango.</td></tr>
                {% endfor %}
            </tbody>
        </table>
        <a href="/" class="btn btn-primary">Volver al Inicio</a>
        """
        return render_template_string(html, pedidos=pedidos, total_ventas=total_ventas)


class ReportePlatosMasVendidosView(BaseView):
    route_base = "/reporte-platos-vendidos"
    default_view = "index"

    @expose("/")
    def index(self):
        # Consulta: Agrupar por plato, sumar cantidades y ordenar descendente
        resultados = db.session.query(
            Plato.nombre,
            func.sum(DetallePedido.cantidad).label('total_vendido')
        ).join(
            DetallePedido, Plato.id == DetallePedido.plato_id
        ).group_by(
            Plato.id, Plato.nombre
        ).order_by(
            func.sum(DetallePedido.cantidad).desc()
        ).limit(10).all()

        html = """
        <h2>Reporte: Top 10 Platos Más Vendidos</h2>
        <table class="table table-bordered table-striped">
            <thead>
                <tr><th>Posición</th><th>Plato</th><th>Cantidad Total Vendida</th></tr>
            </thead>
            <tbody>
                {% for pos, (nombre, cantidad) in enumerate(resultados, start=1) %}
                <tr>
                    <td><strong>#{{ pos }}</strong></td>
                    <td>{{ nombre }}</td>
                    <td class="text-center"><span class="badge badge-info">{{ cantidad }} unidades</span></td>
                </tr>
                {% else %}
                <tr><td colspan="3" class="text-center">Aún no hay registros de ventas.</td></tr>
                {% endfor %}
            </tbody>
        </table>
        <a href="/" class="btn btn-primary">Volver al Inicio</a>
        """
        return render_template_string(html, resultados=resultados, enumerate=enumerate)


# ==========================================
# REGISTRO DE LAS VISTAS DE REPORTES EN EL MENÚ
# ==========================================
appbuilder.add_view(
    ReporteStockBajoView,
    "Stock Bajo",
    icon="fa-exclamation-triangle",
    category="Reportes"
)

appbuilder.add_view(
    ReporteVentasPorFechaView,
    "Ventas por Fecha",
    icon="fa-calendar",
    category="Reportes"
)

appbuilder.add_view(
    ReportePlatosMasVendidosView,
    "Platos Más Vendidos",
    icon="fa-bar-chart",
    category="Reportes"
)