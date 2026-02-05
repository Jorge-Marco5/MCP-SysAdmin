import psutil
import socket

def verificar_puerto(port: int) -> str:
    try:
        resultado = f"Verificando puerto {port}...\n"
        found = False
        for conn in psutil.net_connections(kind='inet'):
            # Check port match FIRST
            if conn.laddr.port == port:
                 # Then check status/type
                is_tcp_listen = (conn.type == socket.SOCK_STREAM and conn.status == psutil.CONN_LISTEN)
                is_udp = (conn.type == socket.SOCK_DGRAM)
                
                if is_tcp_listen or is_udp:
                    try:
                        name = psutil.Process(conn.pid).name() if conn.pid else "Unknown"
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        name = "Unknown"
                    
                    proto = "TCP" if conn.type == socket.SOCK_STREAM else "UDP"
                    resultado += f"Status: IN USE ({proto}) | Process: {name} | PID: {conn.pid or 'N/A'} | Address: {conn.laddr.ip}:{conn.laddr.port}\n"
                    found = True
        
        if found:
            return resultado           
        else:
            return f"Port {port} is not in use (or not LISTEN/UDP)."
    except psutil.AccessDenied:
        return "Error: Access denied. Please run with elevated privileges (sudo/admin)."