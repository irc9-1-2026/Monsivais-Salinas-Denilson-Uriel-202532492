# Security Operations Center (SOC) Dashboard

## 🔒 Sistema de Inteligencia de Amenazas con VirusTotal y Shodan

Dashboard profesional para análisis de ciberseguridad que integra las APIs de VirusTotal y Shodan en una arquitectura de microservicios.

---

## 📋 Tabla de Contenidos

- [Características](#características)
- [Arquitectura](#arquitectura)
- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Configuración](#configuración)
- [Ejecución](#ejecución)
- [Uso](#uso)
- [APIs Integradas](#apis-integradas)
- [Capturas de Pantalla](#capturas-de-pantalla)
- [Créditos](#créditos)
- [Licencia](#licencia)

---

## ✨ Características

### 🔍 Búsqueda Inteligente
- **VirusTotal**: IPs, dominios, hashes SHA256 y URLs
- **Shodan**: IPs y búsquedas avanzadas
- **Detección automática** del tipo de indicador

### 🎨 Dashboard Profesional
- Tema oscuro estilo Security Operations Center (SOC)
- Diseño responsivo con Bootstrap 5
- Animaciones suaves y transiciones
- Iconos Font Awesome
- Tarjetas de estadísticas en tiempo real

### 🔒 Seguridad
- API Keys almacenadas en variables de entorno
- Microservicios aislados
- Validación de entradas
- Rate limiting para APIs externas
- CORS configurado

### 📊 Visualización de Datos
- **VirusTotal**: Reputación, detecciones, WHOIS, categorías
- **Shodan**: Organización, ISP, puertos, vulnerabilidades (CVEs)
- Historial de búsquedas persistente
- Notificaciones en tiempo real
- Loader durante consultas

### 🌐 Acceso en Red
- Servidor escucha en todas las interfaces (0.0.0.0)
- Acceso desde cualquier dispositivo en la red local
- Dashboard accesible desde navegadores móviles

---

## 🏗️ Arquitectura

```
┌─────────────────────────────────────────────────────────────┐
│                         Navegador                            │
│                  http://localhost:3000                       │
└───────────────────────────┬───────────────────────────────────┘
                             │
┌───────────────────────────▼───────────────────────────────────┐
│                     Servidor Principal                        │
│                      (Puerto 3000)                            │
│           Express.js + CORS + Archivos Estáticos               │
└───────────┬───────────────────────────┬───────────────────────┘
            │                           │
┌───────────▼────────────┐ ┌────────────▼────────────────────┐
│  VirusTotal Service     │ │       Shodan Service            │
│    (Puerto 3001)        │ │        (Puerto 3002)            │
│  Express.js + Axios     │ │      Express.js + Axios         │
│  API Key en .env        │ │      API Key en .env            │
└──────────────────────────┘ └─────────────────────────────────┘
```

---

## 📋 Requisitos del Sistema

### Software Necesario
- **Node.js** (v18 o superior)
- **npm** (v9 o superior)
- **Git** (para clonar el repositorio)

### Sistemas Operativos Soportados
- Kali Linux ✅
- Ubuntu/Debian ✅
- Windows (con WSL) ✅
- macOS ✅

### Hardware Recomendado
- RAM: 2GB mínimo, 4GB recomendado
- Almacenamiento: 1GB libre
- Procesador: Dual-core 2.0GHz

---

## 🚀 Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/security-dashboard.git
cd security-dashboard
```

### 2. Instalar dependencias

```bash
# Instalar dependencias del proyecto raíz
npm install

# Instalar dependencias de cada servicio
cd server && npm install
cd ../virustotal-service && npm install
cd ../shodan-service && npm install
cd ..
```

### 3. Configurar variables de entorno

Crear los siguientes archivos `.env`:

**server/.env**
```env
PORT=3000
VIRUSTOTAL_SERVICE_URL=http://localhost:3001
SHODAN_SERVICE_URL=http://localhost:3002
NODE_ENV=development
```

**virustotal-service/.env**
```env
PORT=3001
VT_API_KEY=tu_api_key_aqui
VT_API_URL=https://www.virustotal.com/api/v3
NODE_ENV=development
```

**shodan-service/.env**
```env
PORT=3002
SHODAN_API_KEY=tu_api_key_aqui
SHODAN_API_URL=https://api.shodan.io
NODE_ENV=development
```

---

## ▶️ Ejecución

### Desarrollo (con nodemon)
```bash
# En una terminal
cd server && npm run dev

# En otra terminal
cd virustotal-service && npm run dev

# En otra terminal
cd shodan-service && npm run dev
```

### Producción
```bash
# Usar el script de inicio
./start-all.sh

# O iniciar servicios en segundo plano
nohup ./start-all.sh > dashboard.log 2>&1 &
```

### Sistema (con systemd)
```bash
# Crear servicios systemd
systemctl start virustotal
systemctl start shodan
systemctl start dashboard-server

# Habilitar inicio automático
systemctl enable virustotal
systemctl enable shodan
systemctl enable dashboard-server
```

---

## 🎯 Uso del Dashboard

### 1. Acceso al Dashboard
```
http://localhost:3000
```

O desde cualquier máquina en la red:
```
http://[IP_DEL_SERVIDOR]:3000
```

### 2. Búsquedas en VirusTotal

| Tipo | Ejemplo | Descripción |
|------|---------|-------------|
| IP | 8.8.8.8 | Analiza una dirección IP |
| Dominio | google.com | Analiza un dominio |
| Hash SHA256 | e3b0c44298fc1c... | Analiza un hash |
| URL | https://example.com | Analiza una URL |

### 3. Búsquedas en Shodan

| Tipo | Ejemplo | Descripción |
|------|---------|-------------|
| IP | 8.8.8.8 | Información de una IP |
| Búsqueda | apache | Servidores Apache |
| Búsqueda | port:22 | Puertos SSH |
| Búsqueda | country:MX | Servidores en México |

---

## 🔌 APIs Integradas

### VirusTotal API
Endpoint Base: `https://www.virustotal.com/api/v3`

Endpoints implementados:
- `GET /api/virustotal/:query` - Análisis automático
- `GET /api/virustotal/ip/:ip` - Información de IP
- `GET /api/virustotal/domain/:domain` - Información de dominio
- `GET /api/virustotal/hash/:hash` - Información de hash
- `GET /api/virustotal/url/:url` - Información de URL

### Shodan API
Endpoint Base: `https://api.shodan.io`

Endpoints implementados:
- `GET /api/shodan/:query` - Análisis automático
- `GET /api/shodan/host/:ip` - Información de host
- `GET /api/shodan/search/:query` - Búsqueda avanzada

---

## 📊 Capturas de Pantalla

_(Ver carpeta `docs/capturas/` para las imágenes correspondientes: dashboard principal, resultados de VirusTotal y resultados de Shodan.)_

---

## 👨‍💻 Créditos

**Autor:** Denilson Uriel Monsivais Salinas

**Institución:** Universidad Tecnológica de San Luis Potosí (UTSLP)

**Docente:** Omar Cruz Gutierrez

**Materia:** Ciberseguridad

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo `LICENSE` para más detalles.

---

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork del proyecto
2. Crear una rama (`git checkout -b feature/nueva-funcionalidad`)
3. Commit de cambios (`git commit -m 'Agregar funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abrir un Pull Request

---

## 📞 Soporte

Para soporte, crear un issue en el repositorio o contactar al autor.

---

_Última Actualización: 19 de Julio de 2026_
