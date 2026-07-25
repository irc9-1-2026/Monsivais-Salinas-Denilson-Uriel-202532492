# Ficha Técnica: Integración de la API de Shodan

## Security Operations Center (SOC) Dashboard

---

### Datos Generales

| Campo | Valor |
|-------|-------|
| **Título del Proyecto** | Security Operations Center (SOC) Dashboard - Módulo de Enriquecimiento con API de Shodan |
| **Autor** | Denilson Uriel Monsivais Salinas |
| **Institución** | Universidad Tecnológica de San Luis Potosí (UTSLP) |
| **Docente** | Omar Cruz Gutierrez |
| **Fecha** | 19 de Julio de 2026 |
| **Materia** | Ciberseguridad |
| **Versión** | 1.0 |

---

### 1. Objetivo General

Desarrollar un dashboard de seguridad que integre la API de Shodan para consultar y visualizar información contextual sobre direcciones IP, servicios expuestos, geolocalización y vulnerabilidades potenciales en una interfaz unificada.

### 2. Objetivos Específicos

1. Implementar una arquitectura de microservicios para separar las responsabilidades de seguridad.
2. Desarrollar un dashboard profesional con tema oscuro estilo Security Operations Center (SOC).
3. Integrar la API de Shodan para enriquecer datos de IPs.
4. Asegurar las credenciales mediante variables de entorno.
5. Proporcionar acceso en red para consultas desde múltiples dispositivos.
6. Implementar historial de búsquedas persistente.

---

### 3. Metodología y Herramientas

#### 3.1. Arquitectura

El desarrollo se basa en una arquitectura de microservicios:

- **Servidor Principal (Puerto 3000):** Sirve el frontend y actúa como proxy.
- **Microservicio VirusTotal (Puerto 3001):** Maneja consultas a VirusTotal.
- **Microservicio Shodan (Puerto 3002):** Maneja consultas a Shodan.

#### 3.2. Tecnologías Utilizadas

| Categoría | Tecnología | Versión |
|-----------|------------|---------|
| **Backend** | Node.js | v18+ |
| **Backend** | Express.js | v4.18+ |
| **Frontend** | HTML5 | - |
| **Frontend** | CSS3 | - |
| **Frontend** | JavaScript | ES6+ |
| **UI Framework** | Bootstrap 5 | v5.3+ |
| **UI Framework** | Font Awesome | v6.5+ |
| **API Client** | Axios | v1.6+ |
| **Container** | Docker | v24+ |
| **Orquestación** | Docker Compose | v2.20+ |

#### 3.3. Estructura del Proyecto

```
security-dashboard/
├── frontend/
│   ├── index.html
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── app.js
├── server/
│   ├── app.js
│   ├── routes/
│   │   └── api.js
│   └── .env
├── virustotal-service/
│   ├── app.js
│   ├── routes/
│   │   └── virustotal.js
│   ├── controllers/
│   │   └── virustotalController.js
│   └── .env
├── shodan-service/
│   ├── app.js
│   ├── routes/
│   │   └── shodan.js
│   ├── controllers/
│   │   └── shodanController.js
│   └── .env
├── docker-compose.yml
├── README.md
├── LICENSE
└── package.json
```

---

### 4. Configuración de la API de Shodan

#### 4.1. Obtención de la API Key

1. Crear cuenta en [Shodan](https://www.shodan.io/)
2. Acceder al panel de control
3. Ubicar el apartado "API Key"
4. Copiar la clave generada

#### 4.2. Variables de Entorno

Archivo `.env` en `shodan-service/`:

```env
PORT=3002
SHODAN_API_KEY=TU_API_KEY_AQUI
SHODAN_API_URL=https://api.shodan.io
NODE_ENV=development
```

#### 4.3. Endpoints de la API

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | /api/:query | Análisis automático (IP o búsqueda) |
| GET | /api/host/:ip | Información detallada de IP |
| GET | /api/search/:query | Búsqueda avanzada |

---

### 5. Implementación Técnica

#### 5.1. Controlador Principal

```javascript
const axios = require('axios');
const SHODAN_API_KEY = process.env.SHODAN_API_KEY;
const SHODAN_API_URL = 'https://api.shodan.io';

async function analyze(req, res) {
    try {
        const { query } = req.params;
        const decodedQuery = decodeURIComponent(query);
        const isIP = /^(\d{1,3}\.){3}\d{1,3}$/.test(decodedQuery);

        if (isIP) {
            const result = await callShodanAPI(`/shodan/host/${decodedQuery}`);
            res.json({ type: 'host', query: decodedQuery, data: result });
        } else {
            const result = await callShodanAPI('/shodan/host/search', {
                query: decodedQuery,
                limit: 10
            });
            res.json({ type: 'search', query: decodedQuery, data: result });
        }
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
}
```

#### 5.2. Función de Petición

```javascript
async function callShodanAPI(endpoint, params = {}) {
    try {
        const response = await axios.get(`${SHODAN_API_URL}${endpoint}`, {
            params: {
                key: SHODAN_API_KEY,
                ...params
            },
            timeout: 10000
        });
        return response.data;
    } catch (error) {
        console.error('❌ Error en Shodan API:', error.message);
        if (error.response) {
            throw new Error(error.response.data?.error || `Error ${error.response.status}`);
        }
        throw new Error(error.message);
    }
}
```

---

### 6. Resultados Obtenidos

#### 6.1. Información de IP (8.8.8.8)

```json
{
  "type": "host",
  "query": "8.8.8.8",
  "data": {
    "ip_str": "8.8.8.8",
    "org": "Google LLC",
    "isp": "Google LLC",
    "country_name": "United States",
    "ports": [53, 443],
    "hostnames": ["dns.google"],
    "os": null
  }
}
```

#### 6.2. Datos Visualizados

| Campo | Descripción |
|-------|-------------|
| Organización | Propietario del rango de IPs |
| ISP | Proveedor de servicios de Internet |
| País | Ubicación geográfica |
| Puertos | Servicios expuestos |
| Hostnames | Nombres asociados |
| Vulnerabilidades | CVEs detectados |

---

### 7. Pruebas Realizadas

#### 7.1. Pruebas de Funcionalidad

| Prueba | Resultado |
|--------|-----------|
| Consulta de IP válida | ✅ Éxito |
| Consulta de IP inválida | ❌ Error controlado |
| Búsqueda por texto | ✅ Éxito |
| Búsqueda por puerto | ✅ Éxito |
| Rate limiting | ✅ Implementado |

#### 7.2. Pruebas de Seguridad

| Prueba | Resultado |
|--------|-----------|
| API Key expuesta | ❌ No expuesta |
| Validación de entrada | ✅ Implementada |
| CORS configurado | ✅ Configurado |
| Timeout de peticiones | ✅ Configurado |

---

### 8. Conclusión

La integración de la API de Shodan en el dashboard de seguridad ha sido exitosa, demostrando:

- **Seguridad:** Las credenciales se mantienen seguras en el servidor.
- **Funcionalidad:** El sistema responde correctamente a consultas de IPs.
- **Usabilidad:** La interfaz es intuitiva y profesional.
- **Escalabilidad:** La arquitectura permite agregar más APIs fácilmente.
- **Accesibilidad:** El dashboard es accesible desde cualquier dispositivo.

#### Recomendaciones Futuras

- Implementar caché de resultados
- Agregar más fuentes de inteligencia (AlienVault, MISP, etc.)
- Desarrollar sistema de alertas
- Implementar autenticación de usuarios
- Crear informes en PDF

---

### 9. Anexos

**Anexo A: Capturas de Pantalla**
- Dashboard Principal
- Resultados VirusTotal
- Resultados Shodan
- Historial de Búsquedas
- Configuración de APIs

**Anexo B: Enlaces de Interés**
- Documentación Shodan
- Documentación VirusTotal
- Repositorio GitHub

---

### 10. Firmas

| Rol | Nombre | Firma |
|-----|--------|-------|
| Autor | Denilson Uriel Monsivais Salinas | _________________ |
| Docente | Omar Cruz Gutierrez | _________________ |

**Fecha de Entrega:** 19 de Julio de 2026

**Lugar:** San Luis Potosí, S.L.P., México
