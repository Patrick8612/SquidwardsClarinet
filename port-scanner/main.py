import socket

target = input("请输入目标IP：")
has_open = False

for port in range(1, 101):

    s = socket.socket()
    s.settimeout(0.5)
    
    try:
        s.connect((target, port))
        print(f"[+] 端口 {port} 开放")
    except:
        pass

    s.close()
if not has_open:
    print("[-] 1‑100范围内没有发现开放端口")
