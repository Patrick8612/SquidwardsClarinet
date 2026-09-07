import time
import argparse
import sys
import socket

from scanner import scan_port

def main():
    parser=argparse.ArgumentParser(
        description="Python TCP 端口扫描器"
        )
    parser.add_argument(
        "target",
        help="目标IP地址"
        )

    parser.add_argument(
        "-s",
        "--start",
        type=int,
        default=1,
        help="起始端口，默认：1"
    )

    parser.add_argument(
        "-e",
        "--end",
        type=int,
        default=1000,
        help="结束端口，默认：1000"
    )

    parser.add_argument(
        "-w", "--workers",
        type=int,
        default=100, 
        help="并发线程数，默认100"
        )

    args = parser.parse_args()
    
    target = args.target
    start_port = args.start
    end_port = args.end
    max_workers = args.workers

# DNS解析
    try:
        target_ip = socket.gethostbyname(target)
    except socket.gaierror:
        print(f"[-] 无法解析目标：{target}")
        sys.exit(1)

    MIN_PORT = 1
    MAX_PORT = 65535
    # 检查起始端口
    if not (MIN_PORT <= start_port <= MAX_PORT):
        print(f"[-] 起始端口非法，范围必须 {MIN_PORT}~{MAX_PORT}")
        sys.exit(1)
    # 检查结束端口
    if not (MIN_PORT <= end_port <= MAX_PORT):
        print(f"[-] 结束端口非法，范围必须 {MIN_PORT}~{MAX_PORT}")
        sys.exit(1)
    # 检查端口范围
    if start_port > end_port:
        print("[-] 起始端口不能大于结束端口")
        sys.exit(1)

    # 检查线程数量
    if not (1 <= max_workers <= 1000):
        print("[-] 线程数量非法，范围必须是 1~1000")
        sys.exit(1)

    print(f"[*] 开始扫描目标：{target}")
    print(f"[*] 解析 IP：{target_ip}")
    print(f"[*] 端口范围：{start_port} ~ {end_port}")
    print(f"[*] 并发线程数：{max_workers}")
    start_time = time.time()

    open_ports = scan_port(
        target_ip,
        start_port, 
        end_port, 
        max_workers
        )
    
    elapsed = time.time() - start_time
# 扫描结果
    if not open_ports:
        print("[-] 在指定端口范围内没有发现开放端口")
    else:
        print("[*] 扫描结果：")

        for result in open_ports:
            port = result["port"]
            service = result["service"]
            banner = result["banner"]

            if banner:
                print(f"[+] 端口 {port} ({service}) 开放")
                print(f"    Banner: {banner[:200]}")
            else:
                print(f"[+] 端口 {port} ({service}) 开放")
 
    print(f"[*] 共发现 {len(open_ports)} 个开放端口")
    print(f"[*] 扫描耗时：{elapsed:.2f} 秒")
 # 保存扫描结果
    try:
        with open("scan_result.txt", "w", encoding="utf-8") as f:
            f.write("Python TCP 端口扫描器扫描结果\n")
            f.write("=" * 40 + "\n\n")

            f.write(f"目标：{target}\n")
            f.write(f"解析 IP：{target_ip}\n")
            f.write(f"端口范围：{start_port} ~ {end_port}\n")
            f.write(f"并发线程数：{max_workers}\n")
            f.write(f"扫描耗时：{elapsed:.2f} 秒\n\n")

            f.write("开放端口：\n")
            f.write("-" * 40 + "\n")

            if not open_ports:
                f.write("没有发现开放端口\n")
            else:
                for result in open_ports:
                    port = result["port"]
                    service = result["service"]
                    banner = result["banner"]

                    f.write(f"端口：{port}\n")
                    f.write(f"服务：{service}\n")

                    if banner:
                        f.write(f"Banner：{banner[:200]}\n")
                    else:
                        f.write("Banner：无\n")

                    f.write("\n")

            f.write(f"共发现 {len(open_ports)} 个开放端口\n")

        print("[*] 扫描结果已保存到 scan_result.txt")

    except OSError as e:
        print(f"[-] 保存扫描结果失败：{e}")

    print("[*] 扫描完成")

if __name__ == "__main__":
    main()