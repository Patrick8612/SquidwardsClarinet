import socket
import threading
from concurrent.futures import ThreadPoolExecutor

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

print_lock = threading.Lock()  # 打印锁，解决多线程输出乱码

def scan_single_port(target, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.5)
    try:
        s.connect((target, port))
        # 拿到锁，只有拿到锁的线程才能print
        with print_lock:
            service = port_service.get(port, "Unknown")
            print(f"[+] 端口 {port} ({service}) 开放")
        return port
    except (ConnectionRefusedError, TimeoutError, OSError):
        return None
    finally:
        s.close()

def scan_port(target, start_port, end_port):
    open_ports = []
    max_workers = 100

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        port_range = range(start_port, end_port + 1)
        results = executor.map(
            lambda p: scan_single_port(target, p),
              port_range
        )

        for res in results:
            if res is not None:
                open_ports.append(res)

    open_ports.sort()
    return open_ports