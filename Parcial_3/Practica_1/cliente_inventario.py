import json
import requests

URL_BASE = "http://localhost:5000/equipos"


class ClienteInventario:
    """Pequeño wrapper sobre requests para hablar con la API de equipos."""

    def __init__(self, url_base=URL_BASE):
        self.url_base = url_base

    def obtener_todos(self):
        resp = requests.get(self.url_base)
        if resp.status_code == 200:
            return resp.json()
        return {"error": resp.status_code}

    def obtener_uno(self, id_equipo):
        resp = requests.get(f"{self.url_base}/{id_equipo}")
        return resp.json(), resp.status_code

    def crear(self, nombre, categoria, direccion_ip, estado="en linea"):
        payload = {
            "nombre": nombre,
            "categoria": categoria,
            "direccion_ip": direccion_ip,
            "estado": estado,
        }
        resp = requests.post(self.url_base, json=payload)
        return resp.json(), resp.status_code

    def actualizar(self, id_equipo, nombre, categoria, direccion_ip, estado):
        payload = {
            "nombre": nombre,
            "categoria": categoria,
            "direccion_ip": direccion_ip,
            "estado": estado,
        }
        resp = requests.put(f"{self.url_base}/{id_equipo}", json=payload)
        return resp.json(), resp.status_code

    def eliminar(self, id_equipo):
        resp = requests.delete(f"{self.url_base}/{id_equipo}")
        if resp.status_code == 204:
            return {"eliminado": True, "id": id_equipo}
        return resp.json(), resp.status_code


def mostrar(titulo, contenido):
    print(f"\n--- {titulo} ---")
    print(json.dumps(contenido, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    cliente = ClienteInventario()

    mostrar("Inventario completo", cliente.obtener_todos())

    datos, status = cliente.obtener_uno(101)
    print(f"\n--- Consulta puntual (status {status}) ---")
    mostrar("Equipo 101", datos)

    creado, status = cliente.crear("AP-Sala3", "access-point", "192.168.20.15")
    print(f"\nCreado con status {status}")
    mostrar("Equipo creado", creado)

    actualizado, status = cliente.actualizar(102, "Edge-RT-A-v2", "router", "192.168.10.99", "en linea")
    print(f"\nActualizado con status {status}")
    mostrar("Equipo actualizado", actualizado)

    resultado_baja = cliente.eliminar(103)
    print("\n--- Baja de equipo ---")
    print(resultado_baja)

    mostrar("Inventario final", cliente.obtener_todos())
