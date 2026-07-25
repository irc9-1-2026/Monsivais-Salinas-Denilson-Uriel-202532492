#!/bin/bash

echo "🔍 Verificando servicios..."
echo "=========================="

echo ""
echo "📌 Procesos:"
ps aux | grep node | grep -v grep

echo ""
echo "📌 Puertos:"
sudo netstat -tulpn | grep -E '3000|3001|3002'

echo ""
echo "📌 Estado:"
curl -s http://localhost:3001/health > /dev/null && echo "✅ VirusTotal: OK" || echo "❌ VirusTotal: No responde"
curl -s http://localhost:3002/health > /dev/null && echo "✅ Shodan: OK" || echo "❌ Shodan: No responde"
curl -s http://localhost:3000/health > /dev/null && echo "✅ Servidor: OK" || echo "❌ Servidor: No responde"
