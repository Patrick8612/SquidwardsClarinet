import time
import argparse
import sys

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

    print(f"[*] 开始扫描目标：{target}")
    print(f"[*] 端口范围：{start_port} ~ {end_port}")
    start_time = time.time()

    open_ports = scan_port(target, start_port, end_port, max_workers)
    
    elapsed = time.time() - start_time

    if not open_ports:
        print("[-] 在指定端口范围内没有发现开放端口")
   
    print(f"[*] 共发现 {len(open_ports)} 个开放端口")
    print(f"[*] 扫描耗时：{elapsed:.2f} 秒")
    print("[*] 扫描完成")

if __name__ == "__main__":
    main()