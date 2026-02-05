import psutil
import socket

def listar_puertos(protocol: str = "all"):
    try:
        resultado = "Lista de los puertos en uso (LISTEN/UDP):\n"
        found = False
        
        # Mapping 'all' to 'inet' for psutil, otherwise use as is
        kind = 'inet' if protocol == 'all' else protocol
    
        for conn in psutil.net_connections(kind=kind):
            # TCP uses LISTEN, UDP usually has status NONE but we want to show it
            is_tcp_listen = (conn.type == socket.SOCK_STREAM and conn.status == psutil.CONN_LISTEN)
            is_udp = (conn.type == socket.SOCK_DGRAM)
            
            if is_tcp_listen or is_udp:
                try:
                    name = psutil.Process(conn.pid).name() if conn.pid else "Unknown"
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    name = "Unknown"
                
                proto = "TCP" if conn.type == socket.SOCK_STREAM else "UDP"
                laddr = f"{conn.laddr.ip}:{conn.laddr.port}"
                
                resultado += f"Process: {name} | PID: {conn.pid or 'N/A'} | Proto: {proto} | Local: {laddr}\n"
                found = True

        if found:
            return resultado
        else:
            return "No ports found."
    except psutil.AccessDenied:
        return "Error: Access denied. Please run with elevated privileges (sudo/admin)."