import getrequest.Use
from sql_injection_thing.sql_injection_checker import SQLInjectionChecker

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
    print("\033[91m如果选择POST方式，请通过接下来的方式，将POST的请求包保存\033[0m")
    url = input("请先输入URL: ")
    choice = int(getrequest.Use.menu())
    if choice == 1:
        getrequest.Use.Use_Post()
    elif choice == "2":
        checker = SQLInjectionChecker(url)
        checker.start()
    else:
        print("无效的选择")