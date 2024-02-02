class Chooser:
    def __init__(self):
        pass

    def choose_option(self, menu_items):
        for index, item in enumerate(menu_items):
            print(f"{index + 1}. {item}")
        choice = int(input("请输入您的选择的序号: ")) - 1
        if 0 <= choice < len(menu_items):
            return choice
        else:
            print("无效的选择。请重试。")
