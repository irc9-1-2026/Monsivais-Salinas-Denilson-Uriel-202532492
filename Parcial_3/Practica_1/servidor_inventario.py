from flask import Flask, jsonify, request

app = Flask(__name__)

# ------------------------------------------------------------------
# "Base de datos" simulada con una lista de diccionarios en memoria
# ------------------------------------------------------------------
inventario_red = [
    {"id": 101, "nombre": "Core-SW-A", "categoria": "switch",   "direccion_ip": "192.168.10.1", "estado": "en linea"},
    {"id": 102, "nombre": "Edge-RT-A", "categoria": "router",   "direccion_ip": "192.168.10.2", "estado": "en linea"},
    {"id": 103, "nombre": "Perimetral-FW", "categoria": "firewall", "direccion_ip": "192.168.10.3", "estado": "fuera de linea"},
]
contador_id = 104  # próximo id disponible


def buscar_por_id(id_buscado):
    """Devuelve el equipo con ese id, o None si no existe."""
    for equipo in inventario_red:
        if equipo["id"] == id_buscado:
            return equipo
    return None


# ── Listar todo el inventario ───────────────────────────────────
@app.route("/equipos", methods=["GET"])
def get_equipos():
    return jsonify(inventario_red), 200


# ── Consultar un equipo puntual ─────────────────────────────────
@app.route("/equipos/<int:id_equipo>", methods=["GET"])
def get_equipo(id_equipo):
    equipo = buscar_por_id(id_equipo)
    if equipo is None:
        return jsonify({"mensaje": f"No existe un equipo con id {id_equipo}"}), 404
    return jsonify(equipo), 200


# ── Registrar un equipo nuevo ────────────────────────────────────
@app.route("/equipos", methods=["POST"])
def crear_equipo():
    global contador_id
    body = request.get_json(silent=True) or {}

    equipo_nuevo = {
        "id": contador_id,
        "nombre": body.get("nombre", "equipo-sin-nombre"),
        "categoria": body.get("categoria", "sin-categoria"),
        "direccion_ip": body.get("direccion_ip", "0.0.0.0"),
        "estado": body.get("estado", "en linea"),
    }

    inventario_red.append(equipo_nuevo)
    contador_id += 1
    return jsonify(equipo_nuevo), 201


# ── Reemplazar los datos de un equipo existente ─────────────────
@app.route("/equipos/<int:id_equipo>", methods=["PUT"])
def editar_equipo(id_equipo):
    equipo = buscar_por_id(id_equipo)
    if equipo is None:
        return jsonify({"mensaje": "Ese equipo no existe"}), 404

    body = request.get_json(silent=True) or {}
    for campo in ("nombre", "categoria", "direccion_ip", "estado"):
        if campo in body:
            equipo[campo] = body[campo]

    return jsonify(equipo), 200


# ── Dar de baja un equipo ───────────────────────────────────────
@app.route("/equipos/<int:id_equipo>", methods=["DELETE"])
def borrar_equipo(id_equipo):
    global inventario_red
    total_antes = len(inventario_red)
    inventario_red = [e for e in inventario_red if e["id"] != id_equipo]

    if len(inventario_red) == total_antes:
        return jsonify({"mensaje": "Ese equipo no existe"}), 404
    return "", 204


if __name__ == "__main__":
    app.run(debug=True, port=5000)
