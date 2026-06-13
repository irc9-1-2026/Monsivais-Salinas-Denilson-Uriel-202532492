from flask import Flask, render_template, jsonify, request
import psutil
import platform
import datetime
import json
import os

app = Flask(__name__)

TOP_PROCESOS  = 10
LOG_DIR       = os.path.join(os.path.dirname(__file__), "datos")   # ./datos/
INTERVALO_LOG = 60   # segundos entre snapshots guardados (el front lo llama)

os.makedirs(LOG_DIR, exist_ok=True)


# ── Helpers ─────────────────────────────────────────────────────────

def log_path(fecha: str) -> str:
    """Ruta al archivo JSON del día: datos/YYYY-MM-DD.json"""
    return os.path.join(LOG_DIR, f"{fecha}.json")


def snapshot() -> dict:
    """Recolecta todas las métricas en un dict."""
    cpu_pct   = psutil.cpu_percent(interval=1)
    cpu_freq  = psutil.cpu_freq()
    ram       = psutil.virtual_memory()
    disco     = psutil.disk_usage('/')
    net_antes = psutil.net_io_counters()

    # Procesos top N
    procs = []
    for p in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            procs.append({
                "pid":    p.info['pid'],
                "nombre": p.info['name'],
                "cpu":    round(p.info['cpu_percent'] or 0, 1),
                "ram":    round(p.info['memory_percent'] or 0, 2),
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    top = sorted(procs, key=lambda x: x['cpu'], reverse=True)[:TOP_PROCESOS]

    return {
        "timestamp": datetime.datetime.now().strftime("%H:%M:%S"),
        "os": {
            "sistema":      platform.system(),
            "release":      platform.release(),
            "hostname":     platform.node(),
            "arquitectura": platform.machine(),
            "python":       platform.python_version(),
        },
        "cpu": {
            "porcentaje": cpu_pct,
            "nucleos":    psutil.cpu_count(logical=True),
            "fisicos":    psutil.cpu_count(logical=False),
            "freq_mhz":   round(cpu_freq.current, 0) if cpu_freq else None,
            "alerta":     cpu_pct >= 85,
        },
        "memoria": {
            "total_gb":   round(ram.total    / (1024**3), 1),
            "usada_gb":   round(ram.used     / (1024**3), 1),
            "libre_gb":   round(ram.available / (1024**3), 1),
            "porcentaje": ram.percent,
            "alerta":     ram.percent >= 85,
        },
        "disco": {
            "total_gb": round(disco.total / (1024**3), 1),
            "usado_gb": round(disco.used  / (1024**3), 1),
            "libre_gb": round(disco.free  / (1024**3), 1),
            "porcentaje": disco.percent,
        },
        "red": {
            "enviado_mb":   round(net_antes.bytes_sent / (1024**2), 1),
            "recibido_mb":  round(net_antes.bytes_recv / (1024**2), 1),
        },
        "procesos": top,
    }


def guardar_snapshot(data: dict):
    """Agrega el snapshot al log JSON del día."""
    fecha = datetime.date.today().isoformat()
    path  = log_path(fecha)

    registros = []
    if os.path.exists(path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                registros = json.load(f)
        except Exception:
            registros = []

    registros.append(data)

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(registros, f, ensure_ascii=False, indent=2)


# ── Rutas ────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/datos")
def datos():
    """Métricas en vivo + guarda snapshot."""
    data = snapshot()
    guardar_snapshot(data)
    return jsonify(data)


@app.route("/historial")
def historial():
    """Devuelve los registros guardados de un día.
       ?fecha=YYYY-MM-DD  (defecto: hoy)
    """
    fecha = request.args.get("fecha", datetime.date.today().isoformat())
    path  = log_path(fecha)
    if not os.path.exists(path):
        return jsonify([])
    with open(path, 'r', encoding='utf-8') as f:
        return jsonify(json.load(f))


@app.route("/dias")
def dias():
    """Lista de fechas con registro disponible."""
    archivos = sorted(
        [f.replace(".json", "") for f in os.listdir(LOG_DIR) if f.endswith(".json")],
        reverse=True
    )
    return jsonify(archivos)


if __name__ == "__main__":
    app.run(debug=True)