import datetime
import json
import time
from items import Phone,object_to_dict,Price,SalePromotion,Opinion,Impress
import requests
from selenium import webdriver
from driver_func import pulllowfunc
from scrapy import Selector
from file import readFile,writeFile,appendFile,save_info_print
import pymongo
import schedule
import re
import random
import time
from driver_func import pulllowfunc
from selenium import webdriver
from file import writeFile
import requests
from requests.exceptions import ProxyError
from requests.exceptions import ReadTimeout

headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
        }

desc_headers = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language':'zh-CN,zh;q=0.9',
    'Cache-Control':'max-age=0',
    'Connection':'keep-alive',
    'Cookie':'__guid=71681542.2918503703033858000.1536131649286.0476; monitor_count=3',
    'Host':'dsc.taobaocdn.com',
    'Upgrade-Insecure-Requests':'1',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
}

headers_price = {
    #'Referer': 'https://detail.tmall.com/item.htm?spm=a220o.1000855.0.da321h.143d2412ia1G4P&id=566866136662&sku_properties=5919063:6536025;12304035:970947070;122216431:27772',
    #'Referer': 'https://detail.tmall.com/item.htm?spm=a220o.1000855.0.da321h.143d2412ia1G4P&id=566866136662&sku_properties=5919063:6536025;12304035:970947070;122216431:27772',
    #'Referer': 'https://detail.tmall.com/item.htm?id=567293908632&skuId=3793903203124',
    #'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
    'Referer':'https://detail.tmall.com/item.htm?',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
}

# 未登录的只能访问第一页的 header
request_header_1 = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Cookie': 'cna=oIYOFO7rVkMCAXQEYYqDGRdg; _med=dw:1440&dh:900&pw:1440&ph:900&ist:0; cq=ccp%3D1; lid=%E6%89%93%E6%AD%BB%E4%B8%8D%E7%9C%8B%E6%9F%AF%E5%8D%97; hng=CN%7Czh-CN%7CCNY%7C156; t=3b4b84d8eeb470f55892a40512be0e65; tracknick=%5Cu6253%5Cu6B7B%5Cu4E0D%5Cu770B%5Cu67EF%5Cu5357; _tb_token_=fe9eee5b81ebe; cookie2=17597788d56e422a692f1c52cbcb86c0; res=scroll%3A1349*6555-client%3A1349*631-offset%3A1349*6555-screen%3A1366*768; pnm_cku822=098%23E1hvy9vUvbpvUvCkvvvvvjiPR2SOAji8P2sZ1j1VPmPpAjlhPF5vtjDPRs5hsjlhRphvCvvvvvvEvpCW2blJvvaw1W1lYCA7Ecqhzj7Q%2Bul1B5c6D70O5C63GExr1EeKfvDr1RBl5dUf8rBldE7rejwu%2BExr1EKKNZMZlEkxdX3tEbmxfwo4ddyCvm9vvvvvphvvvvvv9krvpvFavvmm86Cv2vvvvUUdphvUOQvv9krvpv3Fuphvmvvv92pxwtZXkphvC99vvOC0L9hCvvOvCvvvphvPvpvhvv2MMTwCvvpvvUmm; isg=BOzsOfTanIGQsI8EcSUzLuL2vcreDYGY3Qe-DEYt6hcpUYxbbraW3pTjdVnMWcin',
    'Host': 'list.tmall.com',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'

}

request_header = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate, br',
    'Accept-Language':'zh-CN,zh;q=0.9',
    #'Cache-Control':'max-age=0',
    #'Connection':'keep-alive',
    'Cookie':'t=b4a19f4923892b69eae611789db1d895; _tb_token_=feee337b757be; cookie2=141232f20a255c8217eff166312cd26e; dnk=cup%5Cu5514cup; uc3=vt3=F8dByE%2Bn%2B4KJqLOhn4A%3D&id2=UU6m1m%2B2k0Yb8A%3D%3D&nk2=AG8XxWgbk9E%3D&lg2=VFC%2FuZ9ayeYq2g%3D%3D; tracknick=cup%5Cu5514cup; lid=cup%E5%94%94cup; _l_g_=Ug%3D%3D; unb=2679497599; lgc=cup%5Cu5514cup; cookie1=WqbyjojZo8KAxzXVJhNgA9aYHN9BVd62msz0Q25us8s%3D; login=true; cookie17=UU6m1m%2B2k0Yb8A%3D%3D; _nk_=cup%5Cu5514cup; sg=p97; csg=e82de8b6; __guid=164613410.1673403999594594300.1547620723708.1094; _med=dw:1366&dh:768&pw:1366&ph:768&ist:0; cna=Rr/FFOd33jUCAXFpg3i8zi50; otherx=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0; swfstore=98555; x=__ll%3D-1%26_ato%3D0; _uab_collina=154762214238767571291871; _m_h5_tk=74655a35ff93c30cbc0648fa2782f681_1547632411601; _m_h5_tk_enc=c625de81af4727cd6e347bdac9f0b573; tk_trace=1; tkmb=e=5Bjtl0g4RnG_B4EjW_Nhoo3z9t61HvgowhXHHv3Sy1hF5exTDwyVG4H_jGrDuzZGHXLced8k6VNhj7USTMh5HDwWP0Qt42XLU7obgta22Q5mIMu_PEOir-ANcqNqGrbU4lXhCO7aXsm-S8BATx87sZcnF8XtzQrDxsknJ7_DxzJxzSSBewKZxC3B2ZpjOPhzzjxz0uou2FFF26gkZCZghlVaePl1AVP2bx2JvdzcRhZwxgCOA1dQBsMb_U3mGXM2&iv=0&et=1547625329&tk_cps_param=26632258&tkFlag=1; hng=CN%7Czh-CN%7CCNY%7C156; uc1=cookie15=UIHiLt3xD8xYTw%3D%3D; enc=Z3nxZRrmM9nSo3UAvooJLAruN0wFc2LSfwH5UYln7GPOkTyjYdBDssm%2BdjcV0NoifLOSfDvCok9Xwhizs4m9QA%3D%3D; res=scroll%3A1309*6500-client%3A1309*605-offset%3A1309*6500-screen%3A1366*768; x5sec=7b22746d616c6c7365617263683b32223a22326133373466343562313638333736616661366464616133383238666639623443504c712b2b4546454979616862436b746366756f674561445449324e7a6b304f5463314f546b374d6a513d227d; monitor_count=177; pnm_cku822=098%23E1hvivvUvbpvj9CkvvvvvjiPR2SOsjr8Psdptj1VPmPwsjDRPssZzj1WR2spsvGCvvpvvPMMvphvC9vhvvCvpvyCvhQvE2wvC0evD7zhV4tYVVzhAj7xhonbkbmDYEkXJZTQ0f0DW3CQog0HsXZpejanAXcBlLyzOvxrAWBl5dUf8KBlKU66%2B2E1SXVxCLIZkphvC99vvOC0B4yCvv9vvUv6HJps1dyCvm9vvvvvphvvvvvv93avpv3lvvmm86Cv2vvvvUUdphvUOQvv9krvpv3FRphvCvvvvvm5vpvhvvmv99%3D%3D; whl=-1%260%260%260; isg=BENDv90yG5T3QtfqdC117NSO0gctEMYtrM0Cq3Ugt6LBNGNW_Yr8SiCmqoTflC_y',
    # 'Host':'list.tmall.com',
    # 'Referer':'http://list.tmall.com/search_product.htm?cat=50024400',
    'Upgrade-Insecure-Requests':'1',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
}

cookie = 't=b4a19f4923892b69eae611789db1d895; _tb_token_=feee337b757be; cookie2=141232f20a255c8217eff166312cd26e; dnk=cup%5Cu5514cup; uc1=cookie16=UtASsssmPlP%2Ff1IHDsDaPRu%2BPw%3D%3D&cookie21=W5iHLLyFe3xm&cookie15=WqG3DMC9VAQiUQ%3D%3D&existShop=false&pas=0&cookie14=UoTYMbm37ATCzw%3D%3D&lng=zh_CN; uc3=vt3=F8dByE%2Bn%2B4KJqLOhn4A%3D&id2=UU6m1m%2B2k0Yb8A%3D%3D&nk2=AG8XxWgbk9E%3D&lg2=VFC%2FuZ9ayeYq2g%3D%3D; tracknick=cup%5Cu5514cup; lid=cup%E5%94%94cup; _l_g_=Ug%3D%3D; unb=2679497599; lgc=cup%5Cu5514cup; cookie1=WqbyjojZo8KAxzXVJhNgA9aYHN9BVd62msz0Q25us8s%3D; login=true; cookie17=UU6m1m%2B2k0Yb8A%3D%3D; _nk_=cup%5Cu5514cup; sg=p97; csg=e82de8b6; __guid=164613410.1673403999594594300.1547620723708.1094; _med=dw:1366&dh:768&pw:1366&ph:768&ist:0; cna=Rr/FFOd33jUCAXFpg3i8zi50; otherx=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0; swfstore=98555; x=__ll%3D-1%26_ato%3D0; _uab_collina=154762214238767571291871; res=scroll%3A1309*6555-client%3A1309*605-offset%3A1309*6555-screen%3A1366*768; x5sec=7b22746d616c6c7365617263683b32223a223964353739386330346133323531396334306263363264623538613433663636434c6d772b2b4546454c575075706e52784c446667674561444449324e7a6b304f5463314f546b374e773d3d227d; monitor_count=13; pnm_cku822=098%23E1hvCvvUvbpvUvCkvvvvvjiPR2SOAjDWRLSwtjrCPmPZQjrWn2LytjE8PssOzj3WRphvCvvvvvvCvpvVvvpvvhCvKphv8vvvvvCvpvvvvvmmH6CvmjZvvUUdphvWvvvv9krvpv3Fvvmm86CvmVRivpvUvvmvnCxdIjeEvpvVmvvC9jXHmphvLv3SdpvjcWFZaNpBh7QEfwFUaXgOfvc61WFvVCi%2BVd0DyOvO5onmsX7v1EIaWDNBlwethbUf8w1lYWp7rjlW1W2hzCOqb64B9W2%2B%2BfvPvpvhvv2MMTwCvvpvvUmm; whl=-1%260%260%260; isg=BD09wReOPWIzHJkEfk8T-u4MTJn3cmD7xo_Mhf-CYxT1Nl1oxiix_T3s5CrVtonk'



crawl_day_in_week = [0, 1, 2, 3, 4, 5, 6]

not_found_list = []

not_found_list_price = []

client = pymongo.MongoClient('localhost')
db = client['test']


detail_page_head = 'https://detail.tmall.com/item.htm?'
import time
from selenium.webdriver import ActionChains

response = requests.get('http://api.xdaili.cn/xdaili-api//greatRecharge/getGreatIp?spiderId=3ced196c453c4b0a902cfae93681101e&orderno=YZ2018933179FCQpVA&returnType=2&count=1')
print(response.text)
obj = json.loads(response.text)
print(obj['RESULT'][0])
# proxies = {
#     'https':'http://' + obj['RESULT'][0]['ip'] + ':' + obj['RESULT'][0]['port']
# }

service_args = [
    '--proxy=%s' % obj['RESULT'][0]['ip'] + ':' + obj['RESULT'][0]['port'],  # 代理 IP：prot    （eg：192.168.0.28:808）
    '--ssl-protocol=any',           #忽略ssl协议
    '--load - images = no',         # 关闭图片加载（可选）
    '--disk-cache=no',             # 开启缓存（可选）
    '--ignore-ssl-errors=true'     # 忽略https错误(可选)
]


def crawl_list_page_save_as_ids():
    # 打开一个浏览器对象
    driver = webdriver.Chrome(service_args=service_args)
    # 打开淘宝登陆页面
    driver.get('https://login.taobao.com/member/login.jhtml')
    # 模拟点击到账号密码登陆
    driver.find_element_by_id("J_Quick2Static").click()
    # 输入账号密码
    driver.find_element_by_id("TPL_username_1").send_keys("cup唔cup")
    password = driver.find_element_by_id("TPL_password_1").send_keys("nidemima")
    time.sleep(1)
    # 模拟滑块滑动
    slider = driver.find_element_by_xpath("//*[@id='nc_1_n1z']")
    # # 平行移动鼠标
    action = ActionChains(driver)
    action.drag_and_drop_by_offset(slider,500,0).perform()
    # 模拟点击登陆
    driver.find_element_by_id("J_SubmitStatic").click()
    time.sleep(4)
    url = 'https://list.tmall.com/search_product.htm?cat=50024400&q=%CA%D6%BB%FA&sort=s&style=g&from=sn_1_cat-qp#J_crumbs'
    driver.get(url)
    while '疯起人涌' in driver.page_source:
        time.sleep(3)
    if '500 Internal Server Error' in driver.page_source:
        time.sleep(3)
        driver.back()
        url = 'https://list.tmall.com/search_product.htm?cat=50024400&q=%CA%D6%BB%FA&sort=s&style=g&from=sn_1_cat-qp#J_crumbs'
        driver.get(url)
    if '亲，小二正忙，滑动一下马上回来' in driver.page_source:
        # 模拟滑块滑动
        slider = driver.find_element_by_xpath("//*[@id='nc_1_n1z']")
        # # 平行移动鼠标
        action = ActionChains(driver)
        action.drag_and_drop_by_offset(slider, 500, 0).perform()
        time.sleep(3)
    name_links = []
    id_links = []
    for x in range(1, 9):
        time.sleep(3)
        while '疯起人涌' in driver.page_source or '亲，小二正忙，滑动一下马上回来' in driver.page_source:
            while '疯起人涌' in driver.page_source:
                time.sleep(3)
            while '亲，小二正忙，滑动一下马上回来' in driver.page_source:
                # 模拟滑块滑动
                slider = driver.find_element_by_xpath("//*[@id='nc_1_n1z']")
                # # 平行移动鼠标
                action = ActionChains(driver)
                action.drag_and_drop_by_offset(slider, 500, 0).perform()
                time.sleep(3)
                driver.find_element_by_class_name('ui-page-next').click()
                time.sleep(3)
        selector = Selector(text=str(driver.page_source).replace('<span class="H">手机</span>','手机'))
        name = selector.xpath('//div[@class="productTitle productTitle-spu"]//a[1]/text()').extract()
        id = selector.xpath('//div[@class="productTitle productTitle-spu"]//a[1]/@href').extract()
        print(name)
        print(id)
        name_links = name_links + name
        id_links = id_links + id
        # 模拟点击下一页
        driver.find_element_by_class_name('ui-page-next').click()
    print(name_links)
    print(id_links)

crawl_list_page_save_as_ids()