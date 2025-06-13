import socket
import threading

clients = {}  # key：用户名，valve：套接字对象
clients_lock = threading.Lock()


def tcp_recv(a, address):
    global clients
    try:
        name = a.recv(1024).decode('utf-8')
        print(f'现在解密了客户的信息，他名字是{name}')
        with clients_lock:
            clients[name] = a
        while True:
            try:
                data = a.recv(1024).decode('utf-8')
                if not data:
                    print(f"客户端{name}断连")
                    break
                message = name + ':' + data + '\n'
                for i in clients.values():
                    i.send(message.encode('utf-8'))
            except Exception as e:
                print(f"客户端{e}")
                break
    except Exception as e:
        print(f"给我发用户名的时候就报错了{e}")

    with clients_lock:
        if name and name in clients:
            del clients[name]

    a.close()


def tcplink():  # 主线程函数
    global clients
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('127.0.0.1', 2025))
    server.listen(10)
    print('服务器监听开始')
    while True:
        try:
            client_socket, address = server.accept()
            print(f'接到一个客户端{address}')
            t = threading.Thread(target=tcp_recv, args=(client_socket, address))
        except ConnectionResetError:
            print(f'客户端{address}异常断开链接')
            continue
        except KeyboardInterrupt:
            print("服务器关闭")
            break
    server.close()
    print("服务器彻底关闭，释放了服务器对象")


if __name__ == '__main__':
    t = threading.Thread(target=tcplink)
    t.start()
