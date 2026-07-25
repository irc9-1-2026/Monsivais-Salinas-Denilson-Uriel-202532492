import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

URL_BASE = os.getenv("REQRES_URL")
CLAVE_API = os.getenv("REQRES_KEY")


def construir_headers():
    """Arma los headers comunes para toda petición a la API."""
    return {
        "x-api-key": CLAVE_API,
        "Content-Type": "application/json",
    }


def listar_usuarios(pagina=1):
    resp = requests.get(
        f"{URL_BASE}/users",
        params={"page": pagina},
        headers=construir_headers(),
    )
    if resp.status_code != 200:
        return {"error": resp.status_code}
    return resp.json()


def registrar_usuario(nombre_completo, cargo):
    resp = requests.post(
        f"{URL_BASE}/users",
        json={"name": nombre_completo, "job": cargo},
        headers=construir_headers(),
    )
    if resp.status_code != 201:
        return {"error": resp.status_code}
    return resp.json()


def modificar_usuario(user_id, nombre_completo, cargo):
    resp = requests.put(
        f"{URL_BASE}/users/{user_id}",
        json={"name": nombre_completo, "job": cargo},
        headers=construir_headers(),
    )
    if resp.status_code != 200:
        return {"error": resp.status_code}
    return resp.json()


def dar_de_baja_usuario(user_id):
    resp = requests.delete(
        f"{URL_BASE}/users/{user_id}",
        headers=construir_headers(),
    )
    if resp.status_code != 204:
        return {"error": resp.status_code}
    return {"eliminado": True, "id": user_id}


def imprimir(etiqueta, contenido):
    print(f"\n{etiqueta}:")
    print(json.dumps(contenido, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    imprimir("Listado de usuarios", listar_usuarios())
    imprimir("Usuario registrado", registrar_usuario("Marcos Delgado", "Ingeniero de Redes"))
    imprimir("Usuario modificado", modificar_usuario(2, "Marcos Delgado", "Ingeniero de Redes Sr."))
    imprimir("Baja de usuario", dar_de_baja_usuario(2))
