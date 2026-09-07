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
    s.settimeout(1)
    try:
        s.connect((target, port))
        banner = ""
        try:
            # 判断是否http类端口
            if port in {80, 443, 8080, 8888}:
                payload = b"GET / HTTP/1.1\r\nHost:" + target.encode() + b"\r\nConnection:close\r\n\r\n"
                s.sendall(payload)
            else:
                s.sendall(b"\r\n")

            banner = s.recv(1024).decode("utf-8", errors="ignore").strip()
        except (TimeoutError, OSError):
            pass

        with print_lock:
            service = port_service.get(port, "Unknown")
            if banner:
                print(f"[+] 端口 {port} ({service}) 开放")
                print(f"    Banner: {banner}")
            else:
                print(f"[+] 端口 {port} ({service}) 开放")
        return {
            "port": port,
            "service": service,
            "banner": banner
        }
    except (ConnectionRefusedError, TimeoutError, OSError):
        return None
    finally:
        s.close()

def scan_port(target, start_port, end_port, max_workers):
    open_ports = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        port_range = range(start_port, end_port + 1)
        results = executor.map(
            lambda p: scan_single_port(target, p),
              port_range
        )

        for res in results:
            if res is not None:
                open_ports.append(res)

    open_ports.sort(key=lambda x: x["port"])
    return open_ports