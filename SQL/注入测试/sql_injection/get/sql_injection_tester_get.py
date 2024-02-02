import requests
from urllib.parse import urlencode, urlparse, parse_qs, parse_qsl, urlunparse
import urllib.parse


class SQLInjectionTester:
    def __init__(self, url):
        self.url = url
        self.injection_points = []

    def update_url_params(self,params):
        """更新url参数列表值"""
        parsed_url = urllib.parse.urlparse(self.url)
        url_params = urllib.parse.parse_qs(parsed_url.query)
        for key, value in params.items():
            url_params[key] = value
        updated_query = urllib.parse.urlencode(url_params, doseq=True)
        updated_url = urllib.parse.urlunparse((parsed_url.scheme, parsed_url.netloc, parsed_url.path, parsed_url.params, updated_query, parsed_url.fragment))
        return updated_url

    def find_injection_point(self, url):
        """寻找注入点"""
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        injection_points = []
        for key, value in query_params.items():
            for original_value in value:
                for symbol in ["'", '"', ')']:
                    test_value = original_value + symbol
                    test_params = query_params.copy()
                    test_params[key] = test_value
                    test_url = urlunparse(parsed_url._replace(query=urlencode(test_params, doseq=True)))
                    response_text = requests.get(test_url).text.lower()
                    if "error" in response_text or "sql syntax" in response_text:
                        injection_points.append((key, symbol))
                        break;
                    else:
                        injection_points.append((key, ""))
        
        injection_points = [list(elem) for elem in injection_points]
        return injection_points
        
    def test_injection_points(self, url):
        """测试注入点"""
        injection_points = self.find_injection_point(url)
        result = []
        for point, symbol in injection_points:
            result.append((point, symbol))
            self.injection_points.append((point,symbol))
        return result