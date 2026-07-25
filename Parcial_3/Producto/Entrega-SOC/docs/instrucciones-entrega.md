# 📦 INSTRUCCIONES DE ENTREGA

## Archivos a Entregar

### 1. Código Fuente (Carpeta: src/)
- frontend/
  - index.html
  - css/style.css
  - js/app.js
- server/
  - app.js
  - routes/api.js
  - package.json
- virustotal-service/
  - app.js
  - routes/virustotal.js
  - controllers/virustotalController.js
  - package.json
- shodan-service/
  - app.js
  - routes/shodan.js
  - controllers/shodanController.js
  - package.json

### 2. Documentación (Carpeta: docs/)
- README.md
- LICENSE
- ficha-tecnica.md
- manual-usuario.md
- capturas/
  - dashboard.png
  - virustotal-results.png
  - shodan-results.png

### 3. Scripts de Instalación
- install.sh
- start-all.sh
- stop.sh
- check.sh

### 4. Configuración
- docker-compose.yml
- package.json (raíz)
- .gitignore

## Formato de Entrega

### Opción 1: Archivo ZIP
1. Comprimir toda la carpeta `security-dashboard/`
2. Nombrar: `MonsivaisSalinas_DenilsonUriel_SOC_Dashboard.zip`
3. Enviar por correo o plataforma

### Opción 2: Repositorio GitHub
1. Crear repositorio: `security-dashboard`
2. Subir todos los archivos
3. Enviar enlace al repositorio

### Opción 3: CD/DVD
1. Copiar toda la carpeta
2. Etiquetar con nombre y fecha
3. Entregar físicamente

## Lista de Verificación

- [ ] Código fuente completo
- [ ] README.md actualizado
- [ ] Ficha técnica incluida
- [ ] Capturas de pantalla
- [ ] Scripts funcionando
- [ ] Licencia incluida
- [ ] Sin API Keys expuestas
- [ ] Comentarios en código
- [ ] Estructura de carpetas correcta

## 🚀 Comandos para Generar Todo

```bash
# Copiar todos los archivos a un directorio de entrega
mkdir -p /root/Entrega-SOC
cp -r ~/Documents/security-dashboard/* /root/Entrega-SOC/

# Crear archivos de documentación
cd /root/Entrega-SOC
mkdir -p docs/capturas

# Generar ZIP de entrega
zip -r MonsivaisSalinas_DenilsonUriel_SOC_Dashboard.zip *
```
