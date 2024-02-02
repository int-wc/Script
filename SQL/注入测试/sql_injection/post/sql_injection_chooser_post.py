import os

class SQLInjectionChooserPOST:
    def __init__(self):
        self.root_directory = os.path.dirname(os.path.abspath(__file__))  # 获取脚本自身所在文件夹路径
        self.found_directory = None  # 用于存储找到的目标文件夹
        self.selected_file_content = None  # 用于存储最后选择的文件内容
        self.selected_file_path = None  #用于存储最后选择的文件地址

    def search_target_directory(self, directory, target_folder):
        self.found_directory = None  # 重置已找到的目标文件夹
        self.dfs_search(directory, set(), target_folder)

    def dfs_search(self, current_dir, visited, target_folder):
        if self.found_directory:  # 如果已经找到目标文件夹，则停止递归搜索
            return
        visited.add(current_dir)
        for root, dirs, files in os.walk(current_dir):
            if target_folder in dirs:
                self.found_directory = os.path.join(root, target_folder)
                print(f"\033[92m\n找到目标文件夹:{os.path.relpath(self.found_directory, self.root_directory)}\033[0m")
                return
            for d in dirs:
                if os.path.join(root, d) not in visited:
                    next_dir = os.path.join(root, d)
                    self.dfs_search(next_dir, visited, target_folder)
        if os.path.dirname(current_dir) not in visited:
            next_dir = os.path.dirname(current_dir)
            self.dfs_search(next_dir, visited, target_folder)

    def print_files_interactively(self, directory):
        while True:
            print("\033[2J\033[;H")  # 清屏
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
            if self.selected_file_content != None:
                print(f"\033[91m已选择文件：{os.path.relpath(self.selected_file_path, self.root_directory)}\033[0m")
            print(f"\033[94m现在所处文件夹:{os.path.relpath(directory, self.root_directory)}\033[0m\n")
            file_list = os.listdir(directory)
            for i, file in enumerate(file_list):
                print(f"\033[96m{i+1}. {file}\033[0m")
            print("\033[93m\nq. 返回上一级菜单\033[0m")
            print("\033[91mquit. 退出选择菜单\033[0m\n")
            choice = input("\033[95m输入要选择的文件或者探索的文件或文件夹的编号: \033[0m")
            if choice.lower() == 'quit':
                break
            elif choice.lower() == 'q':
                return
            else:
                try:
                    choice_index = int(choice) - 1
                    if 0 <= choice_index < len(file_list):
                        choice_path = os.path.join(directory, file_list[choice_index])
                        if os.path.isfile(choice_path):
                            with open(choice_path, 'r', encoding='utf-8', errors='ignore') as f:
                                file_content = f.read()
                                self.selected_file_content = file_content  # 将选择的文件内容存储在属性中
                                self.selected_file_path = choice_path
                        else:
                            self.print_files_interactively(choice_path)
                    else:
                        print("无效的选择，请输入有效的编号。")
                except ValueError:
                    print("无效的选择，请输入有效的编号。")

    # 示例用法
    def choose_file(self):
        target_folder = 'collection'
        self.search_target_directory(self.root_directory, target_folder)
        if self.found_directory:
            selected_file = self.print_files_interactively(self.found_directory)
            if selected_file:
                print("选择的文件的绝对地址:", selected_file)

# # 示例用法
# tester = SQLInjectionChooserPOST('example_file')
# tester.test_search_and_print_files_interactively()
