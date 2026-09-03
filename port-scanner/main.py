import socket
target = input("请输入目标IP：")
port = int(input("请输入端口："))

s=socket.socket()
print("开始连接")

try:
    s.connect((target,port))
    print("端口开放")
except:
    print("端口关闭")
finally:
    s.close()


