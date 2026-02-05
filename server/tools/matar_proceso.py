import psutil
import socket
import os
import signal

def matar_proceso(port: int) -> str:
    try:
        data = []
        for conn in psutil.net_connections(kind='inet'):
            if conn.laddr.port == port:
                is_tcp_listen = (conn.type == socket.SOCK_STREAM and conn.status == psutil.CONN_LISTEN)
                is_udp = (conn.type == socket.SOCK_DGRAM)
                
                if is_tcp_listen or is_udp:
                    data.append([port, conn.pid or 'N/A', f"{conn.laddr.ip}:{conn.laddr.port}"])
        
        if data:
             # Basic logic: kill the first found PID that is valid
             target_pid = data[0][1]
             if target_pid != 'N/A':
                os.kill(target_pid, signal.SIGKILL)
                return (f"Process {target_pid} on port {port} killed.")
             else:
                return ("PID not found for that port (might be owned by root/system).")
        else:
            return ("Port not found or not in use.")
    except psutil.TimeoutExpired:
        return "Error: Process timeout expired."
    except psutil.AccessDenied:
        return "Error: Access denied. don't have permissions to kill this process. Try running with sudo/admin."
    except Exception as e:
        return f"Error: {e}"