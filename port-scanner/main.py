import time
import sys

from scanner import scan_port

def main():
    if len(sys.argv) == 1:
        #交互模式
        target = input("请输入目标IP：")
        start_port = int(input("请输入起始端口："))
        end_port = int(input("请输入结束端口："))
    elif len(sys.argv) == 4:
        target = sys.argv[1]
        try:
            start_port = int(sys.argv[2])
            end_port = int(sys.argv[3])
        except ValueError:
            print("[-] 端口必须是数字！")
            sys.exit(1)
        
    else:
        print("参数数量错误！用法：python main.py ip 起始端口 结束端口")
        sys.exit(1)

    MIN_PORT = 1
    MAX_PORT = 65535
    if not (MIN_PORT <= start_port <= MAX_PORT):
        print(f"[-] 起始端口非法，范围必须 {MIN_PORT}~{MAX_PORT}")
        sys.exit(1)
        
    if not (MIN_PORT <= end_port <= MAX_PORT):
        print(f"[-] 结束端口非法，范围必须 {MIN_PORT}~{MAX_PORT}")
        sys.exit(1)

    if start_port > end_port:
        print("[-] 起始端口不能大于结束端口")
        sys.exit(1)

    print(f"[*] 开始扫描，端口范围：{start_port} ~ {end_port}")
    start_time = time.time()

    open_ports = scan_port(target, start_port, end_port)
    
    end_time = time.time()
    elapsed = end_time - start_time

    if not open_ports:
        print("[-] 在指定端口范围内没有发现开放端口")
    print("[*] 扫描完成")
   
    print(f"[*]共发现{len(open_ports)}个开放端口,耗时:{elapsed:.2f}秒")
if __name__ == "__main__":
    main()