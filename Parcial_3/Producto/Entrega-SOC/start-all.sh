#!/bin/bash

echo "🛡️  Security Operations Center - Inicio"
echo "======================================"

BASE_DIR="/root/Documents/security-dashboard"
cd $BASE_DIR

# Matar procesos previos
pkill -f node 2>/dev/null
sleep 2

# Crear logs
mkdir -p logs

# Iniciar servicios
echo "🔍 Iniciando VirusTotal Service..."
cd $BASE_DIR/virustotal-service
node app.js > $BASE_DIR/logs/virustotal.log 2>&1 &
VT_PID=$!
echo "   PID: $VT_PID"

echo "🌐 Iniciando Shodan Service..."
cd $BASE_DIR/shodan-service
node app.js > $BASE_DIR/logs/shodan.log 2>&1 &
SHODAN_PID=$!
echo "   PID: $SHODAN_PID"

echo "🖥️  Iniciando Servidor Principal..."
cd $BASE_DIR/server
node app.js > $BASE_DIR/logs/server.log 2>&1 &
SERVER_PID=$!
echo "   PID: $SERVER_PID"

cd $BASE_DIR

echo ""
echo "⏳ Esperando 5 segundos..."
sleep 5

echo ""
echo "🔍 Verificando servicios:"
curl -s http://localhost:3001/health > /dev/null && echo "✅ VirusTotal OK" || echo "❌ VirusTotal ERROR"
curl -s http://localhost:3002/health > /dev/null && echo "✅ Shodan OK" || echo "❌ Shodan ERROR"
curl -s http://localhost:3000/health > /dev/null && echo "✅ Servidor OK" || echo "❌ Servidor ERROR"

echo ""
echo "📊 Dashboard: http://localhost:3000"
echo "🌐 Acceso en red: http://$(hostname -I | awk '{print $1}'):3000"
echo ""
echo "📋 Ver logs: tail -f logs/*.log"
echo "🛑 Detener: pkill -f node"
