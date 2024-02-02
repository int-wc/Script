import collection.selfproxy
from sql_injection.get.sql_injection_checker_get import SQLInjectionChecker
import multiprocessing
from sql_injection.post.sql_injection_tester_post import SQLInjectionTesterPOST

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
   _____ ______ _      ______ _____ _______ ______ _______          _        _____  ____  _      _       _           _   
  / ____|  ____| |    |  ____/ ____|__   __|  ____|__   __|        | |      / ____|/ __ \\| |    (_)     (_)         | |  
 | (___ | |__  | |    | |__ | |       | |  | |__     | | ___   ___ | |_____| (___ | |  | | |     _ _ __  _  ___  ___| |_ 
  \\___ \\|  __| | |    |  __|| |       | |  |  __|    | |/ _ \\ / _ \\| |______\\___ \\| |  | | |    | | '_ \\| |/ _ \\/ __| __|
  ____) | |____| |____| |   | |____   | |  | |       | | (_) | (_) | |      ____) | |__| | |____| | | | | |  __/ (__| |_ 
 |_____/|______|______|_|    \\_____|  |_|  |_|       |_|\\___/ \\___/|_|     |_____/ \\___\\_\\______|_|_| |_| |\\___|\\___|\\__|
                                                                                                       _/ |              
                                                                                                      |__/               \033[0m'''
    print(draw)
    choice = menu()

    if choice == 1:
        # 在一个单独的进程中启动代理服务器
        proxy_process = multiprocessing.Process(target=collection.selfproxy.start_proxy_server)
        proxy_process.start()
        # 监听键盘输入，当检测到键盘输入时，结束代理服务器进程
        input("\n\033[94m按下回车键结束代理服务器\033[0m\n")
        proxy_process.terminate()
        tester = SQLInjectionTesterPOST()
        tester.chooser.choose_file()
    elif choice == 2:
        url = input("请输入URL: ")
        checker = SQLInjectionChecker(url)
        checker.start_get()
    else:
        print("无效的选择")