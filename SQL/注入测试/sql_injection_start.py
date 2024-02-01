import conlletion_thing.Use
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
    print("\033[91m打开了一个代理服务器，请在浏览器先对指定url下手\033[0m")

    if choice == 1:
        checker = SQLInjectionChecker("")
        file_path = input("请输入文件具体位置（绝对路径）：")
        checker.analyser.analyze_post_request(file_path)

    elif choice == "2":
        url = input("请输入URL: ")
        checker = SQLInjectionChecker(url)
        checker.start()
    else:
        print("无效的选择")