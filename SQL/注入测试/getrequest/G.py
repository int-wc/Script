from mitmproxy import http

def requestG(flow: http.HTTPFlow) -> None:
    if flow.request.method == "GET":
        print("Intercepted a GET request:")
        print("URL:", flow.request.url)
        print("Request headers:", flow.request.headers)
        print("Request body:", flow.request.text)

# 在命令行中运行mitmproxy命令来启动代理
# mitmproxy -s get.py -p [端口]
