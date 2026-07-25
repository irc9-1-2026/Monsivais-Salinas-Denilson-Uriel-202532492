import json
import os
from urllib.parse import urlparse

import requests
from dotenv import load_dotenv

load_dotenv()

CLAVE_REQRES = os.getenv("API_KEY")
SEGUNDOS_ESPERA = 8

# ------------------------------------------------------------------
# Tabla de códigos puntuales que necesitan un mensaje específico.
# Todo lo que no aparezca aquí se resuelve por rango en clasificar_status().
# ------------------------------------------------------------------
CODIGOS_ESPECIFICOS = {
    400: ("Bad Request", "Revisar parámetros, body y formato JSON enviados"),
    401: ("Unauthorized", "Confirmar que la API Key o token sean válidos"),
    403: ("Forbidden", "Revisar los permisos asociados al usuario o token"),
    404: ("Not Found", "Revisar que el ID o la ruta consultada sean correctos"),
    429: ("Too Many Requests", "Esperar antes de reintentar (rate limit)"),
}

RANGOS_GENERICOS = [
    (100, 199, "Respuesta informativa", "Esperar a que el servidor complete la respuesta"),
    (200, 299, "Solicitud exitosa", "Continuar con el flujo normal de la respuesta"),
    (300, 399, "Redirección", "Actualizar la URL o seguir la redirección manualmente"),
    (400, 499, "Error del cliente", "Revisar la solicitud y la documentación de la API"),
    (500, 599, "Error del servidor", "La falla es del lado del servidor; conviene reportarla"),
]


def clasificar_status(codigo):
    """Devuelve (categoria, tipo, accion) para un código de estado HTTP."""
    if codigo in CODIGOS_ESPECIFICOS:
        tipo, accion = CODIGOS_ESPECIFICOS[codigo]
        return f"{codigo // 100}xx", tipo, accion

    for inicio, fin, tipo, accion in RANGOS_GENERICOS:
        if inicio <= codigo <= fin:
            return f"{inicio // 100}xx", tipo, accion

    return "desconocido", "?", "Consultar la documentación correspondiente"


def necesita_autenticacion_reqres(url):
    return urlparse(url).netloc.lower().endswith("reqres.in")


def preparar_headers(url, headers_usuario=None):
    headers = dict(headers_usuario or {})

    if necesita_autenticacion_reqres(url):
        if not CLAVE_REQRES:
            raise ValueError(
                "Falta API_KEY en el .env. Agrega tu clave de ReqRes antes de continuar."
            )
        headers.setdefault("x-api-key", CLAVE_REQRES)
        headers.setdefault("Content-Type", "application/json")
        headers.setdefault("User-Agent", "diagnostico-http-cliente/1.0")

    return headers


def ejecutar_prueba(metodo, url, **kwargs):
    """Ejecuta una solicitud HTTP y devuelve un diccionario de diagnóstico."""
    metodo = metodo.upper()

    try:
        headers = preparar_headers(url, kwargs.pop("headers", None))
        kwargs.setdefault("allow_redirects", False)

        respuesta = requests.request(
            metodo, url, headers=headers, timeout=SEGUNDOS_ESPERA, **kwargs
        )
        categoria, tipo, accion = clasificar_status(respuesta.status_code)

        return {
            "url": url,
            "metodo": metodo,
            "status": respuesta.status_code,
            "categoria": categoria,
            "tipo": tipo,
            "accion": accion,
            "exitoso": 200 <= respuesta.status_code <= 299,
        }

    except ValueError as error:
        return {
            "url": url, "metodo": metodo, "error": "Configuración",
            "detalle": str(error), "accion": "Revisar el archivo .env",
            "exitoso": False,
        }
    except requests.exceptions.Timeout:
        return {
            "url": url, "metodo": metodo, "error": "Timeout",
            "accion": "Reintentar más tarde y confirmar que el servidor esté disponible",
            "exitoso": False,
        }
    except requests.exceptions.ConnectionError:
        return {
            "url": url, "metodo": metodo, "error": "Sin conexión",
            "accion": "Confirmar la conexión de red y validar la URL",
            "exitoso": False,
        }
    except requests.exceptions.RequestException as error:
        return {
            "url": url, "metodo": metodo, "error": "Error de petición",
            "detalle": str(error), "accion": "Revisar la solicitud y la configuración de red",
            "exitoso": False,
        }


def correr_bateria_pruebas(casos, archivo_salida="diagnostico.json"):
    """Ejecuta todos los casos, imprime avance en consola y guarda el reporte."""
    resultados = []

    for caso in casos:
        metodo = caso["metodo"]
        url = caso["url"]
        extras = {k: v for k, v in caso.items() if k not in ("metodo", "url")}

        resultado = ejecutar_prueba(metodo, url, **extras)
        resultados.append(resultado)

        marca = "OK " if resultado.get("exitoso") else "FAIL"
        status_mostrado = resultado.get("status", "ERR")
        print(f"[{marca}] {resultado['metodo']:6} {status_mostrado} -> {resultado['url']}")

    exitosas = sum(1 for r in resultados if r.get("exitoso") is True)

    reporte = {
        "total_pruebas": len(resultados),
        "exitosas": exitosas,
        "fallidas": len(resultados) - exitosas,
        "resultados": resultados,
    }

    with open(archivo_salida, "w", encoding="utf-8") as f:
        json.dump(reporte, f, indent=2, ensure_ascii=False)

    return reporte


if __name__ == "__main__":
    casos_de_prueba = [
        {"metodo": "GET", "url": "https://reqres.in/api/users/1"},
        {"metodo": "GET", "url": "https://reqres.in/api/users/9999"},
        {
            "metodo": "POST",
            "url": "https://reqres.in/api/users",
            "json": {"name": "Marcos Delgado", "job": "Network Engineer"},
        },
        {"metodo": "DELETE", "url": "https://reqres.in/api/users/2"},
        {"metodo": "GET", "url": "https://httpstat.us/500"},
        {"metodo": "GET", "url": "https://httpstat.us/401"},

        # Casos opcionales del checklist:
        # {"metodo": "GET", "url": "https://httpstat.us/429"},
        # {"metodo": "GET", "url": "https://dominio-inexistente.xyz"},
    ]

    reporte_final = correr_bateria_pruebas(casos_de_prueba)

    print("\nResumen final:", json.dumps({
        "total": reporte_final["total_pruebas"],
        "exitosas": reporte_final["exitosas"],
        "fallidas": reporte_final["fallidas"],
    }, indent=2, ensure_ascii=False))
