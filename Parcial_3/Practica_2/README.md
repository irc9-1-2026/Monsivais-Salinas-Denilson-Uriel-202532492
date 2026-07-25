# Autenticación con REST APIs (Postman + Python)

Script en Python que automatiza las 4 operaciones CRUD sobre la API pública
**ReqRes**, enviando la autenticación por API Key a través de variables de
entorno (nunca hardcodeadas en el código).

## Requisitos

- Python 3.8 o superior
- pip

## Instalación

```bash
cd practica2
python3 -m venv .venv
source .venv/bin/activate
pip install requests python-dotenv
```

## Configuración de variables de entorno

1. Copia la plantilla a un archivo real:
   ```bash
   cp .env.example .env
   ```
2. `.env.example` ya trae los valores de la API pública de pruebas:
   ```
   REQRES_URL=https://reqres.in/api
   REQRES_KEY=reqres-free-v1
   ```
3. El `.env` real está listado en `.gitignore`, así que nunca se sube al
   control de versiones aunque contenga una key real en otro contexto.

## Ejecución

```bash
python3 usuarios_reqres.py
```

El script imprime en consola el resultado de listar, crear, modificar y dar
de baja un usuario contra la API.

## Estructura del proyecto

```
practica2/
├── usuarios_reqres.py   ← script con las 4 operaciones y autenticación
├── .env                 ← variables reales (NO se versiona)
├── .env.example         ← plantilla sin secretos (sí se versiona)
├── .gitignore           ← ignora .env, entornos virtuales y cachés
├── capturas/            ← evidencias de Postman (GET, POST, PUT, DELETE)
└── README.md
```

## Notas del checklist de la práctica

**Sobre Postman:**
- `GET /users` debe responder `200 OK` y `POST /users` responde
  `201 Created`.
- Si se omite el header `x-api-key`, el nivel gratuito de ReqRes puede
  devolver `401 Unauthorized` o simplemente ignorarlo; conviene capturar el
  código real que se obtenga en la prueba propia, ya que puede variar.
- Usar una variable de entorno para la URL base (`base_url`) evita repetirla
  en cada petición y facilita cambiar entre ambientes (dev/test/prod) sin
  tocar cada request individualmente.

**Sobre el script en Python:**
- `os.getenv(...)` devuelve `None` cuando la variable no está definida en el
  `.env`, en vez de lanzar una excepción.
- Se pasan los parámetros de consulta con `params=` en lugar de armar la
  URL a mano, porque `requests` construye el query string, escapa caracteres
  especiales y deja un código más limpio.
- Los status codes y cuerpos de respuesta del script deben coincidir con lo
  observado en Postman (los IDs pueden variar porque ReqRes los simula).
