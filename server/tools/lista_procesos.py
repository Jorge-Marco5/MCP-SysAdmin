import psutil
import time

def lista_procesos(limite: int = 10, tipo: str = "cpu") -> str:
    try:
        # Primera pasada: Inicializar contadores de CPU
        # Necesitamos iterar una vez para que psutil empiece a contar
        procs = list(psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info']))
        for p in procs:
            try:
                p.cpu_percent()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        # Esperamos un momento para calcular el delta
        time.sleep(0.5)
        
        procesos = []
        # Segunda pasada: Obtener valores reales
        for proc in procs:
            try:
                # Al llamar cpu_percent() por segunda vez, nos da el uso en ese intervalo
                # sin bloquear (interval=None por defecto)
                cpu = proc.cpu_percent()
                
                # Actualizamos la info del objeto (aunque cpu_percent() retorna el valor, 
                # es bueno mantener la consistencia si accedemos a .info después)
                proc.info['cpu_percent'] = cpu
                
                procesos.append(
                    {
                        'pid': proc.info['pid'],
                        'name': proc.info['name'],
                        'cpu_percent': cpu,
                        'memory_info': proc.info['memory_info']
                    }
                )
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        # Ordenamos por consumo de CPU descendente
        if tipo == "cpu":
            top_procs = sorted(procesos, key=lambda p: p['cpu_percent'], reverse=True)[:limite]
            resultado = "--- Top Procesos por CPU ---\n"
        elif tipo == "ram":
            top_procs = sorted(procesos, key=lambda p: p['memory_info'].rss, reverse=True)[:limite]
            resultado = "--- Top Procesos por RAM ---\n"
        
        for p in top_procs:
            if tipo == "cpu":
                resultado += f"PID: {p['pid']} | {p['name']} | CPU: {p['cpu_percent']}%\n"
            elif tipo == "ram":
                resultado += f"PID: {p['pid']} | {p['name']} | RAM: {p['memory_info'].rss / (1024**2):.2f} MB\n"
            
        return resultado
    except Exception as e:
        return f"Error al obtener top de procesos: {str(e)}"
    