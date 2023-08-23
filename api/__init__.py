import requests
import json
import time


api_host = 'www.autohome.com.cn'  # autohome
android_api_host = 'a.athm.cn'  # autohome


class AutoHomeApi:
    def __init__(self, host=api_host):
        self.host = host
        self.android_host = android_api_host
        self.session = requests.session()
        self.web_mainpage()

    def web_mainpage(self):
        """根据burpsuite和此处返回的html内容不一致推测，有指纹检测"""
        api_url = f'http://{self.host}/beijing/'
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.31(0x18001f37) NetType/WIFI Language/zh_CN'
        }  #
        r = self.session.get(api_url, headers=headers)
        # print(r.text)

    def android_get_brandlist(self):
        """安卓的接口 获取brandlist"""
        api_url = f'http://{self.android_host}/cars.app.autohome.com.cn/carbase/selectcarportal/brandlist'  # pm=2&pluginvcersion=11.51.0
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.31(0x18001f37) NetType/WIFI Language/zh_CN'
        }  #
        r = self.session.get(api_url, headers=headers)
        r_cnt = json.loads(r.text)
        return r_cnt

    def get_branchid_by_name(self, name):
        r = self.android_get_brandlist()
        brandlist = r.get('result').get('brandlist')
        for i in brandlist:
            for _ in i.get('list'):
                if _.get('name') == name:
                    return _.get('id')

    def get_brand_by_id(self, brandid):
        api_url = f'http://{self.host}/ashx/index/GetHomeFindCar.ashx?type=1&brandid={brandid}&v=1'
        headers = {
            'content-type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.31(0x18001f37) NetType/WIFI Language/zh_CN'
        }  #
        r = requests.get(api_url, headers=headers)
        r_cnt = json.loads(r.text)
        return r_cnt

    def get_brand_by_name(self, name):
        branchid = self.get_branchid_by_name(name)
        r = self.get_brand_by_id(branchid)
        return r

    def get_carseries_by_seriesid(self, seriesid):
        api_url = f'http://{self.host}/ashx/index/GetHomeFindCar.ashx?type=2&seriesid={seriesid}&format=json&v=1'
        headers = {
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.31(0x18001f37) NetType/WIFI Language/zh_CN'
        }  #
        r = requests.get(api_url, headers=headers)
        r_cnt = json.loads(r.text)
        return r_cnt

    def get_car_config_by_specid(self, spec_id):  # cityid后面再改
        """根据车型id获取具体配置"""
        api_url = f'http://{self.android_host}/cars.app.autohome.com.cn/carcfg/config/newspeccompare?specids={spec_id}&cityid=440300&pm=2&pluginversion=11.51.0&site=2'  # &model=1&seriesid=146
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.31(0x18001f37) NetType/WIFI Language/zh_CN'
        }  #
        r = requests.get(api_url, headers=headers)
        return r.text

    # def


if __name__ == '__main__':
    autohome = AutoHomeApi()
    r = autohome.get_car_config_by_specid('58754')
    print(r)
