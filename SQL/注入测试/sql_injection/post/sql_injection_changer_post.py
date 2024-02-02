import requests

class SQLInjectionChangerPOST:
    def __init__(self) -> None:
        pass
    
    def Change_request(self,request_file_path,change_value):
       # 请求包路径

        with open(request_file_path, 'r') as file:
            request_data = file.read()

        # 根据空行分离请求头和请求正文
        headers, body = request_data.split('\n\n', 1)

        # 将请求正文解析为字典
        params = {}
        for param in body.split('&'):
            key, value = param.split('=')
            params[key] = value

        # 修改第一个参数的值
        first_param_key = list(params.keys())[0]  # 获取第一个参数的键
        params[first_param_key] = change_value  # 修改第一个参数的值

        # 将修改后的参数转换回请求正文格式
        modified_body = '&'.join([f"{key}={value}" for key, value in params.items()])

        modified_request = headers + '\n\n' + modified_body

        # 从请求头中获取Host
        host = headers.split('\n')[1].split(': ')[1]

        # 构建请求头
        headers_dict = {}
        for line in headers.split('\n')[1:]:
            key, value = line.split(': ')
            headers_dict[key] = value

        # 发送修改后的请求
        response = requests.post('http://' + host, data=modified_body, headers=headers_dict)

        # 将返回的包以网页源码形式存储
        with open('response.html', 'w', encoding='utf-8') as file:
            file.write(response.text)

        print("响应已存储到response.html")
