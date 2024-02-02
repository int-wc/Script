import os
from sql_injection_chooser_post import SQLInjectionChooserPOST

class SQLInjectionTesterPOST:
    def __init__(self):
        self.chooser = SQLInjectionChooserPOST()
    
# 示例用法
tester = SQLInjectionTesterPOST()
tester.chooser.choose_file()