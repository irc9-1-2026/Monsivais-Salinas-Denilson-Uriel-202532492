# Práctica 3 — Diagnóstico de códigos de estado HTTP

Script que dispara una batería de solicitudes contra distintas APIs
externas, clasifica cada respuesta según el rango de su código de estado,
captura los errores de red que puedan aparecer, y guarda todo el resultado
en `diagnostico.json`.

## Puesta en marcha

### Instalar dependencias

```bash
python -m pip install -r requirements.txt
```

O de forma manual:

```bash
python -m pip install requests python-dotenv
```

### Configurar la API Key

Crea un archivo `.env` en la raíz del proyecto con tu clave de ReqRes:

```
API_KEY=TU_CLAVE_REAL_DE_REQRES
```

Debe ser la misma clave que ya usaste en Postman durante la práctica
anterior.

### Ejecutar

```bash
python diagnostico_http.py
```

Mientras corre, la consola muestra el método, el código de estado y la URL
de cada prueba. Al terminar, genera (o sobrescribe) `diagnostico.json`.

## Casos de prueba incluidos

| Método | URL                        | Código esperado |
|--------|----------------------------|------------------|
| GET    | ReqRes `/users/1`          | 200              |
| GET    | ReqRes `/users/9999`       | 404              |
| POST   | ReqRes `/users`            | 201              |
| DELETE | ReqRes `/users/2`          | 204              |
| GET    | httpstat.us/500            | 500              |
| GET    | httpstat.us/401            | 401              |

> El resultado real depende de la disponibilidad de estos servicios en el
> momento de la prueba, y de tener una API Key de ReqRes válida.

## Estructura del reporte `diagnostico.json`

- `total_pruebas`: cuántas solicitudes se ejecutaron.
- `exitosas`: cuántas respuestas cayeron en el rango 200–299.
- `fallidas`: el resto, incluyendo errores de conexión o configuración.
- `resultados`: detalle de cada solicitud individual.

Campos posibles dentro de cada resultado:

| Campo      | Qué representa                                       |
|------------|-------------------------------------------------------|
| `url`      | Dirección consultada                                   |
| `metodo`   | Verbo HTTP usado                                        |
| `status`   | Código de estado devuelto por el servidor              |
| `categoria`| Familia del código (1xx…5xx)                            |
| `tipo`     | Descripción del resultado                               |
| `accion`   | Sugerencia sobre cómo proceder                          |
| `exitoso`  | `true` solo si el código cayó en 2xx                    |
| `error`    | Nombre de la excepción, si no hubo respuesta            |
| `detalle`  | Información adicional de algunos errores                |

## Qué significa cada categoría

| Categoría | Significado                                             |
|-----------|-----------------------------------------------------------|
| 1xx       | Respuesta informativa                                      |
| 2xx       | La solicitud se procesó correctamente                       |
| 3xx       | Hay una redirección involucrada                             |
| 4xx       | Falla del cliente: datos, autenticación o permisos           |
| 5xx       | Falla ocurrida del lado del servidor                         |

El script fija `allow_redirects=False` para poder inspeccionar los códigos
3xx tal como llegan, sin que `requests` los siga automáticamente.

## Preguntas del checklist

**¿Por qué se separan `Timeout` y `ConnectionError`?**

Son fallas distintas. Un `Timeout` implica que sí hubo intento de conexión,
pero el servidor no respondió a tiempo. Un `ConnectionError` implica que la
conexión nunca llegó a establecerse — puede deberse a una URL mal escrita,
una falla de DNS, el servidor caído, o un problema de red local.

**¿Qué pasa si se prueba con una URL inexistente?**

Se agrega a la lista de casos:

```python
{"metodo": "GET", "url": "https://dominio-inexistente.xyz"},
```

Se espera que dispare `requests.exceptions.ConnectionError`, quedando algo
así en el JSON:

```json
{
  "error": "Sin conexión",
  "accion": "Confirmar la conexión de red y validar la URL",
  "exitoso": false
}
```

El resultado puede variar si hay un proxy corporativo o un filtro DNS de
por medio.

**¿Cómo se prueba el código 429?**

Se agrega:

```python
{"metodo": "GET", "url": "https://httpstat.us/429"},
```

Este servicio responde con el código indicado al final de la URL, así que
el diagnóstico debería verse así:

```json
{
  "status": 429,
  "categoria": "4xx",
  "tipo": "Too Many Requests",
  "accion": "Esperar antes de reintentar (rate limit)",
  "exitoso": false
}
```

## Problemas comunes

**Todo contra ReqRes devuelve 401**
Revisa que el `.env` tenga una API Key vigente y que sea la misma que
funcionó en Postman.

**`ModuleNotFoundError`**
Faltan dependencias: `python -m pip install requests python-dotenv`.

**`httpstat.us` da error de conexión**
Puede ser una caída temporal o un bloqueo de red. Si necesitas verificar
que el clasificador sigue funcionando mientras tanto, puedes usar de forma
temporal:

```
https://httpbin.org/status/500
https://httpbin.org/status/401
https://httpbin.org/status/429
```
