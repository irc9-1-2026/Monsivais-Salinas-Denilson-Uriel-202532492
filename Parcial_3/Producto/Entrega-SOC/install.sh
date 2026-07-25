#!/bin/bash

echo "🛡️  Instalando Security Dashboard"
echo "================================"

# Actualizar repositorios
echo "📦 Actualizando repositorios..."
sudo apt update

# Instalar Node.js y npm
echo "📦 Instalando Node.js..."
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs

# Instalar herramientas adicionales
echo "📦 Instalando herramientas..."
sudo apt install -y git curl wget screen htop

# Verificar versiones
echo ""
echo "✅ Versiones instaladas:"
node --version
npm --version

echo ""
echo "📦 Instalando dependencias del proyecto..."
cd ~/Documents/security-dashboard
npm install

# Instalar dependencias de servicios
echo "📦 Instalando dependencias de servicios..."
cd server && npm install
cd ../virustotal-service && npm install
cd ../shodan-service && npm install
cd ..

echo ""
echo "✅ Instalación completada"
echo ""
echo "📝 Pasos siguientes:"
echo "1. Configurar API Keys en los archivos .env"
echo "2. Ejecutar: ./start-all.sh"
echo "3. Abrir navegador: http://localhost:3000"
