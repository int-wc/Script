import requests
from bs4 import BeautifulSoup
import re

class Analyser:
    def __init__(self) -> None:
        pass
    def analyze_html(self, url):
        '''现在是array类型'''
        response = requests.get(url)
        html_content = response.text

        soup = BeautifulSoup(html_content, 'html.parser')

        pre_tag = soup.find('pre')
        array_contents = pre_tag.get_text()

        results = re.findall(r'string\(\d+\) "([^"]+)"', array_contents)

        result_list = [result for result in results]

        return result_list
    
    def analyze_post_request(self,request):
        body = request.split('\r\n\r\n')[-1]
        print(body)
        params = body.split('&')
        parsed_params = {}
        for param in params:
            key, value = param.split('=')
            parsed_params[key] = value
        print(parsed_params)
        return parsed_params