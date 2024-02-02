import collection.selfproxy
from sql_injection.get.sql_injection_checker_get import SQLInjectionChecker
import multiprocessing

def menu():
    print("\033[91m1. POST [这将会打开一个代理，请你手动先让post包发出]\033[0m")
    print("\033[91m2. GET [这需要你输入url，手动输入过一次参数，会自动运行][如http://8573974b-50cf-4ff0-91a3-4d7a77103ebe.node5.buuoj.cn:81/?inject=10]\033[0m")

    while True:
        choice = input("请选择操作（1-POST，2-GET）：")
        if choice in ["1", "2"]:
            return int(choice)
        else:
            print("无效的选择，请重新选择")

if __name__ == "__main__":
    draw = '''\033[92m
   _____      _  __  _____ _______ ______ _______          _                  _                       
  / ____|    | |/ _|/ ____|__   __|  ____|__   __|        | |                | |                      
 | (___   ___| | |_| |       | |  | |__     | | ___   ___ | |______ ___  __ _| |_ __ ___   __ _ _ __  
  \\___ \\ / _ \\ |  _| |       | |  |  __|    | |/ _ \\ / _ \\| |______/ __|/ _` | | '_ ` _ \\ / _` | '_ \\ 
  ____) |  __/ | | | |____   | |  | |       | | (_) | (_) | |      \\__ \\ (_| | | | | | | | (_| | |_) |
 |_____/ \\___|_|_|  \\_____|  |_|  |_|       |_|\\___/ \\___/|_|      |___/\\__, |_|_| |_| |_|\\__,_| .__/ 
                                                                           | |                 | |    
                                                                           |_|                 |_|    \033[0m'''
    print(draw)
    choice = menu()

    if choice == 1:
        # 在一个单独的进程中启动代理服务器
        proxy_process = multiprocessing.Process(target=collection.selfproxy.start_proxy_server)
        proxy_process.start()
        # 监听键盘输入，当检测到键盘输入时，结束代理服务器进程
        input("\n\033[94m按下回车键结束代理服务器\033[0m\n")
        proxy_process.terminate()
    elif choice == 2:
        url = input("请输入URL: ")
        checker = SQLInjectionChecker(url)
        checker.start_get()
    else:
        print("无效的选择")