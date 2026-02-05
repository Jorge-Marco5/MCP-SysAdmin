import psutil
import platform

def metricas_sistema():
    try:
        cpu_percent = psutil.cpu_percent(interval=0.5)
        memoria = psutil.virtual_memory()
    
        info = (
            f"--- Estado del Sistema ---\n"
            f"🖥️ CPU Uso: {cpu_percent}%\n"
            f"💾 RAM Uso: {memoria.percent}% (Libre: {memoria.available / (1024**3):.2f} GB)\n"
            f"⚙️ SO: {platform.system()} {platform.release()}"
        )
        return info
    except Exception as e:
        return f"Error al obtener metricas del sistema: {str(e)}"