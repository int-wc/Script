from sql_injection.post.sql_injection_chooser_post import SQLInjectionChooserPOST


class SQLInjectionTesterPOST:
    def __init__(self):
        self.chooser = SQLInjectionChooserPOST()
        self.injection_points = []
        self.noallow = []
    
#1、猜测注入点
#2、猜测注入类型--先跳过
#3、探查过滤函数
        #绕过滤
#4、报表，爆库