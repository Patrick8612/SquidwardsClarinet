# Python TCP 端口扫描器

一个基于 Python 编写的简单 TCP 端口扫描器，用于学习网络编程、多线程、命令行参数解析以及基础服务识别。

> 本项目主要用于学习 Python 网络编程和网络安全基础。

---

## 项目功能

- TCP Connect 端口扫描
- 支持 IP 地址扫描
- 支持域名解析
- 支持自定义端口范围
- 支持多线程并发扫描
- 支持自定义并发线程数
- 基于端口号进行基础服务识别
- 基础 Banner 获取
- 扫描结果保存到文本文件
- 命令行参数解析
- 基本的参数合法性检查
- 异常处理

---

## 项目结构

```text
port-scanner/
├── main.py              # 程序入口，负责参数处理和结果保存
├── scanner.py           # 端口扫描核心功能
├── README.md            # 项目说明
├── .gitignore           # Git 忽略文件配置
└── scan_result.txt      # 扫描结果（本地生成，不提交到 Git）

环境要求
Python 3.12+
Windows / Linux / macOS 均可运行

本项目使用 Python 标准库，不需要安装额外的第三方依赖。

主要使用：

socket
threading
concurrent.futures
argparse
time
sys
使用方法
1. 扫描默认端口范围

默认扫描 1~1000 端口：

python main.py 127.0.0.1
2. 指定端口范围

例如扫描 1~100：

python main.py 127.0.0.1 -s 1 -e 100

其中：

-s / --start：起始端口
-e / --end：结束端口
3. 指定并发线程数

例如使用 50 个线程：

python main.py 127.0.0.1 -s 1 -e 1000 -w 50

其中：

-w / --workers：并发线程数
默认值为 100

线程数量支持：

1 ~ 1000
4. 扫描域名

程序支持输入域名，程序会先进行 DNS 解析，再对解析得到的 IPv4 地址进行扫描。

例如：

python main.py example.com -s 1 -e 100

程序会显示：

[*] 开始扫描目标：example.com
[*] 解析 IP：xxx.xxx.xxx.xxx
扫描结果示例

程序运行后，会在终端显示类似：

[*] 开始扫描目标：127.0.0.1
[*] 解析 IP：127.0.0.1
[*] 端口范围：1 ~ 1000
[*] 并发线程数：100

[+] 端口 80 (HTTP) 开放
    Banner: ...

[*] 共发现 1 个开放端口
[*] 扫描耗时：0.52 秒
[*] 扫描结果已保存到 scan_result.txt
[*] 扫描完成

同时会生成：

scan_result.txt

用于保存本次扫描结果。

基本服务识别

程序根据常见端口号进行基础服务判断：

端口	服务
21	FTP
22	SSH
23	Telnet
80	HTTP
135	RPC
443	HTTPS
3306	MySQL
3389	RDP
6379	Redis
8080	HTTP-Proxy

需要注意：

基于端口号的服务判断只是基础推测，并不能完全代表目标端口实际运行的服务。

实现原理

程序主要分为两个部分。

main.py
负责：

解析命令行参数
检查端口范围
检查线程数量
进行 DNS 解析
调用扫描模块
显示扫描结果
统计扫描耗时
保存扫描结果

scanner.py
负责：

创建 TCP Socket
设置连接超时时间
尝试连接目标端口
判断端口是否开放
获取基础 Banner
使用线程池进行并发扫描
返回扫描结果
多线程扫描

本项目使用：
ThreadPoolExecutor
创建线程池。

由于端口扫描主要涉及网络 I/O 操作，因此使用多线程可以同时对多个端口进行连接，提高扫描效率。
例如：

with ThreadPoolExecutor(max_workers=max_workers) as executor:
    ...

其中 max_workers 用于控制并发线程数量。

Banner 获取

对于部分服务，程序会尝试向目标端口发送简单的数据，并读取服务器返回的数据。

例如 HTTP 服务会尝试发送：

GET / HTTP/1.1
Host: target
Connection: close

然后读取服务器返回的数据作为基础 Banner 信息。

Banner 获取并不是所有服务都支持，因此部分开放端口可能不会返回 Banner。

参数检查

程序会检查：

起始端口是否在 1~65535
结束端口是否在 1~65535
起始端口是否小于等于结束端口
并发线程数是否在 1~1000
域名是否能够正常解析

如果参数错误，程序会给出提示并退出。

学习内容

通过这个项目，可以学习：

Python 基础语法
函数与模块
socket 网络编程
TCP 基础
多线程
线程池
命令行参数解析
DNS 基础
Banner 获取
异常处理
文件读写
Git / GitHub 项目管理
后续改进方向

目前项目已经实现基本的端口扫描功能，后续可以继续研究：

更完善的服务识别
更准确的 Banner 解析
TCP / UDP 扫描
IPv6 支持
更完善的扫描结果格式
JSON 格式结果保存
日志系统
扫描性能优化
安全声明

本项目仅用于：

网络安全学习
Python 网络编程学习
本地实验环境
自有设备测试
已获得授权的安全测试

请勿对未经授权的服务器、网站或网络设备进行扫描。

License

本项目仅用于学习和研究。
