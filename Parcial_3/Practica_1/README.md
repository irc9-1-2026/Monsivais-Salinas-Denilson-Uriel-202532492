# Inventario de Equipos de Red — API REST

Pequeño proyecto con una API en Flask para administrar un inventario de
equipos de red (switches, routers, firewalls, etc.) y un cliente en Python
que la consume usando `requests`.

## Requisitos previos
- Python 3.8 o superior
- pip

## Paso 1 — Crear el entorno virtual (Terminal 1)

```bash
cd practica1
python3 -m venv venv
source venv/bin/activate
pip install flask requests
```

## Paso 2 — Iniciar el servidor (Terminal 1)

```bash
python servidor_inventario.py
```

El servidor queda escuchando en `http://localhost:5000`. Deja esta terminal
abierta mientras trabajas.

## Paso 3 — Correr el cliente (Terminal 2)

Abre otra terminal:

```bash
cd practica1
source venv/bin/activate
python cliente_inventario.py
```

Vas a ver en consola cómo se ejecutan las operaciones de consulta, alta,
modificación y baja contra el servidor.

## Paso 4 — Probar la API a mano (opcional)

```bash
curl http://localhost:5000/equipos
curl http://localhost:5000/equipos/101

curl -X POST http://localhost:5000/equipos \
     -H "Content-Type: application/json" \
     -d '{"nombre":"AP-Prueba","categoria":"access-point","direccion_ip":"192.168.1.99"}'

curl -X DELETE http://localhost:5000/equipos/103
```

## Endpoints disponibles

| Método | Ruta                | Descripción                       |
|--------|---------------------|------------------------------------|
| GET    | /equipos             | Lista todo el inventario           |
| GET    | /equipos/<id>        | Consulta un equipo puntual         |
| POST   | /equipos             | Registra un equipo nuevo           |
| PUT    | /equipos/<id>        | Reemplaza los datos de un equipo   |
| DELETE | /equipos/<id>        | Da de baja un equipo               |

## Estructura del proyecto

```
practica1/
├── servidor_inventario.py   # API Flask con los 5 endpoints
├── cliente_inventario.py    # Cliente basado en requests
└── README.md
```
