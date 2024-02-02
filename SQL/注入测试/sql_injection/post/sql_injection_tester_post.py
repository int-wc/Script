import os

class SQLInjectionTesterPOST:
    def __init__(self, file):
        self.file = file
        self.root_directory = os.path.dirname(os.path.abspath(__file__))  # 获取脚本自身所在文件夹路径

    def search_collection_files_dfs(self, directory):
        self.dfs_search(directory, set())

    def dfs_search(self, current_dir, visited):
        print("Current directory:", current_dir)
        visited.add(current_dir)
        for root, dirs, files in os.walk(current_dir):
            if 'collection' in dirs:
                collection_path = os.path.join(root, 'collection')
                print("Entering collection folder:", collection_path)
                for file in os.listdir(collection_path):
                    file_path = os.path.join(collection_path, file)
                    try:
                        with open(file_path, 'rb') as f:
                            print("Reading file:", file_path)
                            content = f.read().decode('utf-8', errors='ignore')
                            print(content)
                    except UnicodeDecodeError:
                        print("Error reading file:", file_path)
                return
            for d in dirs:
                if os.path.join(root, d) not in visited:
                    next_dir = os.path.join(root, d)
                    self.dfs_search(next_dir, visited)
        if os.path.dirname(current_dir) not in visited:
            next_dir = os.path.dirname(current_dir)
            self.dfs_search(next_dir, visited)

    # 示例用法
    def test_search_collection_files_dfs(self):
        self.search_collection_files_dfs(self.root_directory)

# 示例用法
tester = SQLInjectionTesterPOST('example_file')
tester.test_search_collection_files_dfs()
