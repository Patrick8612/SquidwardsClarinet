import socket

target = input("请输入目标IP：")
has_open = False

start_port=int(input("请输入起始端口："))
end_port=int(input("请输入结束端口："))

for port in range(start_port, end_port + 1):

    s = socket.socket()
    s.settimeout(0.5)
    
    try:
        s.connect((target, port))
        print(f"[+] 端口 {port} 开放")
        has_open = True
    except:
        pass

    s.close()
if not has_open:
    print("[-] 在指定端口范围内没有发现开放端口")
