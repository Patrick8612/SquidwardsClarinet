import socket

def scan_port(target, start_port, end_port):
    has_open = False
    for port in range(start_port, end_port + 1):
        s = socket.socket()
        s.settimeout(0.5)
        try:
            s.connect((target, port))
            print(f"[+] 端口 {port} 开放")
            has_open = True
        except:
            pass
        finally:
            s.close()
    # 返回标记，不做任何结果打印
    return has_open

def main():
    try:
        target = input("请输入目标IP：")
        start_port = int(input("请输入起始端口："))
        end_port = int(input("请输入结束端口："))
    except ValueError:
        print("[-] 端口必须输入数字！")
        exit()

    if start_port > end_port:
        print("[-] 起始端口不能大于结束端口")
        exit()

    print(f"[*] 开始扫描，端口范围：{start_port} ~ {end_port}")
    has_open = scan_port(target, start_port, end_port)

    if not has_open:
        print("[-] 在指定端口范围内没有发现开放端口")
    print("[*] 扫描完成")

if __name__ == "__main__":
    main()