import importlib, subprocess, sys, platform, datetime, time, os

# =====================================================================
# LIBRERÍAS
# =====================================================================
LIBRERIAS = [
    "psutil",
    "flask",
    "requests",
]

EXTRAS = {
    "python-dotenv": "dotenv",
}

faltantes = []
for lib in LIBRERIAS:
    try:
        importlib.import_module(lib)
        print(f"  ✓  {lib}")
    except ImportError:
        print(f"  ✗  {lib}  ← falta")
        faltantes.append(lib)

for paquete, modulo in EXTRAS.items():
    try:
        importlib.import_module(modulo)
        print(f"  ✓  {modulo}")
    except ImportError:
        print(f"  ✗  {modulo}  ← falta")
        faltantes.append(paquete)

if faltantes:
    print(f"\nInstalando: {', '.join(faltantes)}\n")
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install"] + faltantes
    )

for lib in LIBRERIAS:
    globals()[lib] = importlib.import_module(lib)

globals()["dotenv"] = importlib.import_module("dotenv")

print("\n✓ Listo, todo importado.\n")

# =====================================================================
# CONSTANTES
# =====================================================================
from dotenv import load_dotenv
load_dotenv()

TELEGRAM_TOKEN     = os.getenv("TELEGRAM_TOKEN", "")
TELEGRAM_CHAT_ID   = os.getenv("TELEGRAM_CHAT_ID", "")
INTERVALO_SEGUNDOS = 3
TOP_PROCESOS       = 10


# =====================================================================
# FUNCIÓN: Enviar alerta a Telegram
# =====================================================================
def enviar_telegram(mensaje):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        return
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": TELEGRAM_CHAT_ID, "text": mensaje})
    except Exception as e:
        print(f"  ✗ Error Telegram: {e}")


# =====================================================================
# FUNCIÓN: Limpiar pantalla
# =====================================================================
def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')


# =====================================================================
# FUNCIÓN: Línea separadora decorativa
# =====================================================================
def separador(caracter='—', ancho=60):
    print(caracter * ancho)


# =====================================================================
# FUNCIÓN: Información del sistema operativo
# =====================================================================
def mostrar_info_sistema():
    separador('=')
    print("  INFORMACIÓN DEL SISTEMA")
    separador('=')
    print(f"  Sistema operativo : {platform.system()} {platform.release()}")
    print(f"  Hostname          : {platform.node()}")
    print(f"  Arquitectura      : {platform.machine()}")
    print(f"  Versión de Python : {platform.python_version()}")
    separador()


# =====================================================================
# FUNCIÓN: Uso de CPU
# =====================================================================
def mostrar_cpu():
    porcentaje     = psutil.cpu_percent(interval=1)
    nucleos        = psutil.cpu_count(logical=True)
    bloques_total  = 30
    bloques_llenos = int((porcentaje / 100) * bloques_total)
    barra          = '█' * bloques_llenos + '░' * (bloques_total - bloques_llenos)
    print(f"\n  CPU")
    print(f"   Núcleos : {nucleos}")
    print(f"   Uso     : [{barra}] {porcentaje:.1f}%")
    if porcentaje >= 85:
        print("   ⚠️  ALERTA: CPU muy alto")
        enviar_telegram(f"⚠️ ALERTA CPU: {porcentaje:.1f}% en {platform.node()}")
    elif porcentaje >= 60:
        print("   ↑ CPU moderado")


# =====================================================================
# FUNCIÓN: Uso de RAM
# =====================================================================
def mostrar_ram():
    ram            = psutil.virtual_memory()
    total_gb       = ram.total / (1024 ** 3)
    usada_gb       = ram.used  / (1024 ** 3)
    libre_gb       = ram.available / (1024 ** 3)
    porcentaje     = ram.percent
    bloques_total  = 30
    bloques_llenos = int((porcentaje / 100) * bloques_total)
    barra          = '█' * bloques_llenos + '░' * (bloques_total - bloques_llenos)
    print(f"\n  RAM")
    print(f"   Total  : {total_gb:.1f} GB")
    print(f"   Usada  : {usada_gb:.1f} GB")
    print(f"   Libre  : {libre_gb:.1f} GB")
    print(f"   Uso    : [{barra}] {porcentaje:.1f}%")
    if porcentaje >= 85:
        print("   ⚠️  ALERTA: RAM muy alta")
        enviar_telegram(f"⚠️ ALERTA RAM: {porcentaje:.1f}% en {platform.node()}")


# =====================================================================
# FUNCIÓN: Top N procesos por uso de CPU
# =====================================================================
def mostrar_procesos():
    procesos = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            procesos.append({
                'pid':    proc.info['pid'],
                'nombre': proc.info['name'],
                'cpu':    proc.info['cpu_percent'] or 0,
                'ram':    proc.info['memory_percent'] or 0,
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    top = sorted(procesos, key=lambda p: p['cpu'], reverse=True)[:TOP_PROCESOS]
    separador()
    print(f"\n  TOP {TOP_PROCESOS} PROCESOS POR CPU\n")
    print(f"  {'PID':<8} {'NOMBRE':<30} {'CPU %':<10} {'RAM %'}")
    separador('—', 60)
    for p in top:
        nombre = p['nombre'][:28] if len(p['nombre']) > 28 else p['nombre']
        print(f"  {p['pid']:<8} {nombre:<30} {p['cpu']:<10.1f} {p['ram']:.1f}")


# =====================================================================
# FUNCIÓN PRINCIPAL
# =====================================================================
def main():
    print("\n  Iniciando monitor... presiona Ctrl+C para salir.\n")
    enviar_telegram(f"✅ Monitor iniciado en {platform.node()}")
    time.sleep(1)
    while True:
        limpiar_pantalla()
        ahora = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print(f"\n  ⏱️  MONITOR DE SISTEMA  ⏱️  {ahora}")
        mostrar_info_sistema()
        mostrar_cpu()
        mostrar_ram()
        mostrar_procesos()
        separador('=')
        print(f"  Actualizando en {INTERVALO_SEGUNDOS} segundos...  Ctrl+C para salir")
        separador('=')
        time.sleep(INTERVALO_SEGUNDOS)


# =====================================================================
# PUNTO DE ENTRADA
# =====================================================================
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        enviar_telegram(f"🛑 Monitor detenido en {platform.node()}")
        print("\n\n  Monitor detenido. ¡Hasta luego!\n")