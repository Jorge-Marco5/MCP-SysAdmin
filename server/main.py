from mcp.server.fastmcp import FastMCP

from tools.obtener_hora import obtener_hora
from tools.metricas_sistema import metricas_sistema
from tools.lista_procesos import lista_procesos
from tools.lista_puertos import listar_puertos
from tools.verificar_puerto import verificar_puerto
from tools.matar_proceso import matar_proceso

# 1. Inicializamos el servidor
# "MiPrimerServidor" es el nombre que verán los clientes
mcp = FastMCP("MiPrimerServidor")

# 2. Creamos una Herramienta (Tool) simple
# El decorador @mcp.tool() convierte la función en algo que la IA puede usar
@mcp.tool()
def tiempo_sistema() -> str:
    """Obtiene la fecha y hora actual del sistema"""
    return obtener_hora()
    
@mcp.tool()
def obtener_metricas_sistema() -> str:
    """Obtiene metricas del sistema"""
    return metricas_sistema()

@mcp.tool()
def listar_procesos_top(limite: int = 10, tipo: str = "cpu") -> str:
    """
        Lista los procesos que más CPU están consumiendo en este momento.
        Args:
            limite: Cantidad de procesos a mostrar (default 10).
            tipo: Tipo de proceso a listar (cpu, ram)
        """
    return lista_procesos(limite, tipo)

@mcp.tool()
def listar_procesos_en_puertos(protocol: str = "all") -> str:
    """
    Lista los puertos que están siendo utilizados en el sistema.
    Args:
        protocol: Protocolo a listar (tcp, udp, all)
    """
    return listar_puertos(protocol)

@mcp.tool()
def verificar_proceso_en_puerto(port: int) -> str:
    """
    Verifica si un puerto está en uso y muestra el proceso que lo está utilizando.
    Args:
        port: Puerto a verificar
    """
    return verificar_puerto(port)

@mcp.tool()
def matar_proceso_en_puerto(port: int) -> str:
    """
    Cierra el proceso del puerto especifico
    Args:
        port: Puerto a cerrar
    """
    return matar_proceso(port)

# 4. Ejecución
# FastMCP se encarga automáticamente de manejar la conexión (stdio)
if __name__ == "__main__":
    mcp.run()