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
    choice = int(getrequest.Use.menu())
    if choice == 1:
        getrequest.Use.Use_Post()
        checker = SQLInjectionChecker("")
        file_path = input("请输入文件具体位置（绝对路径）：")
        checker.analyser.analyze_post_request(file_path)
        
    elif choice == "2":
        url = input("请输入URL: ")
        checker = SQLInjectionChecker(url)
        checker.start()
    else:
        print("无效的选择")