import os
import logging
from datetime import date, timedelta
from flask import Blueprint, request, jsonify
from flask_login import login_required
from openai import OpenAI

from ..extensions import db
from ..models import Plato, Ingrediente

logger = logging.getLogger(__name__)

asistente_bp = Blueprint(
    "asistente_ai",
    __name__,
    url_prefix="/api"
)


def obtener_cliente():
    """Crea el cliente de conexión con la API de IA."""
    api_key = os.getenv("AI_API_KEY")
    base_url = os.getenv("AI_URL")

    if not api_key:
        raise RuntimeError("No se configuró AI_API_KEY.")

    if not base_url:
        raise RuntimeError("No se configuró AI_URL.")

    return OpenAI(
        api_key=api_key,
        base_url=base_url
    )


def contexto_restaurante():
    """Resume el menú y el inventario actual para dárselo a la IA."""
    try:
        hoy = date.today()
        limite = hoy + timedelta(days=7)

        platos = db.session.query(Plato).filter_by(activo=True).limit(40).all()
        ingredientes = db.session.query(Ingrediente).filter_by(activo=True).all()

        menu = [f"{p.nombre} (Bs {p.precio})" for p in platos]

        stock_bajo = [
            f"{i.nombre}: {i.cantidad} {i.unidad_medida} (mínimo {i.stock_minimo})"
            for i in ingredientes
            if i.cantidad <= i.stock_minimo
        ]

        por_vencer = [
            f"{i.nombre} vence el {i.fecha_vencimiento}"
            for i in ingredientes
            if i.fecha_vencimiento <= limite
        ]

        return (
            "\n\nDatos actuales del restaurante:\n"
            f"- Menú: {', '.join(menu) or 'sin platos registrados'}\n"
            f"- Ingredientes con stock bajo: {'; '.join(stock_bajo) or 'ninguno'}\n"
            f"- Ingredientes por vencer (7 días): {'; '.join(por_vencer) or 'ninguno'}"
        )
    except Exception:
        logger.exception("No se pudo armar el contexto del restaurante.")
        return ""


@asistente_bp.post("/asistente")
@login_required
def consultar_asistente():
    try:
        data = request.get_json(silent=True)

        if not isinstance(data, dict):
            return jsonify({
                "error": "Se esperaba una solicitud JSON válida."
            }), 400

        mensaje = data.get("message", "").strip()
        historial = data.get("history", [])

        if not mensaje:
            return jsonify({
                "error": "Debes escribir un mensaje."
            }), 400

        if not isinstance(historial, list):
            return jsonify({
                "error": "El historial debe ser una lista."
            }), 400

        mensajes = [
            {
                "role": "system",
                "content": (
                    "Eres un asistente de inteligencia artificial "
                    "especializado en la gestión de un restaurante: "
                    "cocina, recetas, menú, ingredientes, sustituciones, "
                    "aprovechamiento de productos próximos a vencer, "
                    "control de inventario y sugerencias para el servicio. "
                    "Responde en español, de forma clara, práctica y "
                    "ordenada. Cuando sea pertinente, indica cantidades, "
                    "porciones, tiempos y pasos. Si la pregunta se relaciona "
                    "con el menú o el inventario, apóyate en los datos "
                    "actuales del restaurante que se te proporcionan."
                    + contexto_restaurante()
                )
            }
        ]

        for item in historial[-20:]:
            if not isinstance(item, dict):
                continue

            rol = item.get("role")
            contenido = item.get("content")

            if (
                rol in ("user", "assistant")
                and isinstance(contenido, str)
                and contenido.strip()
            ):
                mensajes.append({
                    "role": rol,
                    "content": contenido.strip()
                })

        mensajes.append({
            "role": "user",
            "content": mensaje
        })

        cliente = obtener_cliente()

        respuesta = cliente.chat.completions.create(
            model=os.getenv("AI_MODEL", "gpt-4o-mini"),
            messages=mensajes,
            temperature=0.7
        )

        contenido = respuesta.choices[0].message.content

        if not contenido:
            contenido = "No se recibió una respuesta de la IA."

        return jsonify({
            "respuesta": contenido
        }), 200

    except Exception:
        logger.exception("Error al consultar el asistente de IA.")

        return jsonify({
            "error": (
                "No se pudo obtener una respuesta. "
                "Verifica la configuración de la API e inténtalo nuevamente."
            )
        }), 500