import urllib.parse
import os
import socket
import threading
import requests

# 获取当前脚本所在的文件夹路径
script_directory = os.path.dirname(os.path.abspath(__file__))

# HTTP代理服务器配置
proxy_host = "127.0.0.1"
proxy_port = 1234
is_running = True  # 标志变量，控制代理服务器的运行状态

def handle_client(client_socket):
    # 接收浏览器的请求
    request_data = client_socket.recv(4096)

    # 解析请求内容
    request_lines = request_data.split(b'\n')
    first_line = request_lines[0].decode('utf-8')
    method, url, _ = first_line.split(' ')

    if "buuoj.cn" not in url:
        client_socket.close()
        return
    else:
        print(f"接收到来自浏览器的请求：{url}")

    url_parts = urllib.parse.urlsplit(url)
    target_host = url_parts.hostname
    if target_host is None:
        target_host = url_parts.netloc.split(':')[0]  # 使用 netloc 替代 hostname
    target_port = url_parts.port or 80  # 如果 URL 中没有指定端口号，则默认为 80

    # 获取目标服务器的IP地址
    target_ip = socket.gethostbyname(target_host)

    # 将请求发送给目标服务器
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.connect((target_ip, target_port))
    server_socket.send(request_data)

    # 接收目标服务器的响应
    response_data = server_socket.recv(4096)

    # 接收POST参数值
    if method == 'POST':
        post_data = request_data.split(b'\r\n\r\n')[-1]
        post_params = urllib.parse.parse_qs(post_data.decode('utf-8'))
        if post_params:
            for key, value in post_params.items():
                value_encoded = urllib.parse.quote(value[0], safe='')  # 对参数值进行 URL 编码

                # 创建文件夹路径
                request_folder = os.path.join(script_directory, "requests", target_host, f"{key}_{value_encoded}")
                os.makedirs(request_folder, exist_ok=True)
                request_filename = os.path.join(request_folder, "request.txt")
                with open(request_filename, 'wb') as request_file:
                    request_file.write(request_data)

                # 构建新的POST请求
                new_post_data = {key: value[0]}  # 构建新的POST参数
                response = requests.post(url, data=new_post_data)  # 发送新的POST请求
                html_content = response.text  # 获取返回的HTML源码

                # 创建文件夹路径
                response_folder = os.path.join(script_directory, "responses", target_host, f"{key}_{value_encoded}")
                os.makedirs(response_folder, exist_ok=True)
                response_filename = os.path.join(response_folder, "response.html")
                with open(response_filename, 'w', encoding='utf-8') as response_file:
                    response_file.write(html_content)

    # 将响应发送给浏览器
    client_socket.send(response_data)

    # 关闭连接
    client_socket.close()
    server_socket.close()

def start_proxy_server():
    # 创建套接字
    proxy_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy_server.bind((proxy_host, proxy_port))
    proxy_server.listen(5)

    print(f"代理服务器正在监听 {proxy_host}:{proxy_port}")

    global is_running  # 声明 is_running 为全局变量

    while is_running:
        try:
            client_socket, addr = proxy_server.accept()
            client_handler = threading.Thread(target=handle_client, args=(client_socket,))
            client_handler.start()
        except KeyboardInterrupt:
            is_running = False  # 当检测到键盘输入时，停止代理服务器的运行
            break

    # 关闭代理服务器
    proxy_server.close()