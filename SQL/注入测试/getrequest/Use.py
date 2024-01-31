import subprocess
import os

def Use_Post():
    port = "1234"  # 替换为你想要使用的端口号
    script_path = "P.py"  # 使用相对路径指定脚本路径

    # 获取当前脚本所在的目录
    script_directory = os.path.dirname(os.path.abspath(__file__))

    # 改变当前工作目录到脚本所在的目录
    os.chdir(script_directory)

    # 启动mitmproxy进程
    try:
        subprocess.run(["mitmproxy", "-s", script_path, "-p", port], check=True)
    except subprocess.CalledProcessError as e:
        print(f"命令运行失败: {e}")

def menu():
    print("选择URL传递数据的方式:")
    print("1. POST")
    print("2. GET")
    choice = input("请输入你的选择 (1/2): ")
    return choice


# def Use_Get():
#     port = "1234"  # 替换为你想要使用的端口号
#     script_path = "G.py"  # 使用相对路径指定脚本路径

#     # 获取当前脚本所在的目录
#     script_directory = os.path.dirname(os.path.abspath(__file__))

#     # 改变当前工作目录到脚本所在的目录
#     os.chdir(script_directory)

#     # 启动mitmproxy进程
#     try:
#         subprocess.run(["mitmproxy", "-s", script_path, "-p", port], check=True)
#     except subprocess.CalledProcessError as e:
#         print(f"命令运行失败: {e}")