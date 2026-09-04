import socket

port_service = {
    22: "SSH",
    80: "HTTP",
    443: "HTTPS",
    21: "FTP",
    23: "Telnet",
    135: "RPC",
    3306: "MySQL",
    3389: "RDP",
    6379: "Redis",
    8080: "HTTP‑Proxy"
}

def scan_port(target, start_port, end_port):
    open_ports = []
    for port in range(start_port, end_port + 1):
        # 显式指定IPv4、TCP
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)
        try:
            s.connect((target, port))
            open_ports.append(port)

            service = port_service.get(port, "Unknown")
            print(f"[+] 端口 {port} ({service}) 开放")  
  
        except(ConnectionRefusedError,TimeoutError,OSError):
            pass
        finally:
            s.close()

    return open_ports