import re
name = '4G全网通 赤焰红 官方标配 6+128GB'
if re.search('[0-9]?G?\+?[0-9]+GB?', name):
    print(re.search('[0-9]?G?\+?[1-9][0-9]+GM?B?', name))

import uuid

print(str(uuid.uuid4()).split('-')[0])

import requests
import json

# response = requests.get('http://api.xdaili.cn/xdaili-api//greatRecharge/getGreatIp?spiderId=3ced196c453c4b0a902cfae93681101e&orderno=YZ2018933179FCQpVA&returnType=2&count=1')
# print(response.text)
# obj = json.loads(response.text)
# print(obj['RESULT'][0])
# proxies = {
#     'https':'http://' + obj['RESULT'][0]['ip'] + ':' + obj['RESULT'][0]['port']
# }

# respsoner = requests.get('https://log.mmstat.com/v.gif?logtype=1&title=%E6%89%8B%E6%9C%BA-%E5%A4%A9%E7%8C%ABTmall.com-%E7%90%86%E6%83%B3%E7%94%9F%E6%B4%BB%E4%B8%8A%E5%A4%A9%E7%8C%AB&pre=https%3A%2F%2Flist.tmall.com%2Fsearch_product.htm%2F_____tmd_____%2Fverify%2F%3Fnc_token%3Ddd49055851264c407bdda29f14f9242f%26nc_session_id%3D013xXk5B4PlkG-aMzGxNA_T5sX1ar5cJJJ7XB5orgBlyECpd4ATrCz9sEDH3UIYHvCBxcs32Y5e1eT-bTbWY6pTrIVH1PCiKoKmEThMDQdlOt9blrKLMEsDxyHGtdbS8cH%26nc_sig%3D05LO-1siennj7yh60y9eaY1bxRhFcytk9UO2uSbLWo-kr8mx8KwpXCjheBkZw0HHjucr-Fl3LWw_yWj9zym8BtiZlC_Ti67Pt4elQKvJomcJK1XsaAeh8hlDheOsqgWo_ZKFFxX7MAO7Ka3PJrKbRVosf9fLNdnMj_FeZ5Ryj5YTih4dn_VliqBxPkMV15QPJzVaABCN3R-uCfH5cPWFvoocKAMfhHVjJMyfXUoDtFJA7nHNI9hQsRZW9N7hkAnJ5AGErJoJ1qO4Ey38gJaNGxZQ5KK63BFWHxblTJKV3SqjwcdjiiIblUPpz-orALxIE1%26x5secdata%3D5e0c8e1365474455070961b803bd560607b52cabf5960afff39b64ce58073f78d979de2416369c06d4b7baf6310e2ef30fb58e11561318b0308ef8fd9c3fa89a0bb560b6b5c6f65e984ddd63ba1d1d7c396bb9766f330c5b5132ff34742323e581de66ecf56ceefe58b43bc7d00cbc44524b2377b38c5a19331b3954a03b72e668d3e7b17b21bd719fb03c9f712bf98798c92afd477d7e4691b16b931d3dbb71cf0668a613bfce08422c454842020c0e5fd102e32437f7b8741ec5aa54e4ecf05a96b607c3cba52cf264e0eb8554db770bc1524a0ba9894b714e5abb1799eb9201e4ee5c156d344e73c99d13eb28e7f0834483b45f7c195c851e5ea867461b6ef58a49c29fa722359df311fdf60c67e643057e2edd1838e1ccc05f4f01cfb617210e3262c1af4c702d6f07b89fa3f306fe3d96f437e26cb843d9bd96ae725188f8b26098ae3913dec42886212a6d7a39261b7f764385dfac9875f00815d4a5d1159fbba9ebb98a19904b60f4c987d9f6009df39efa3dcae4ac7e36523ca278e33481563d4eb6cd56118b1e9b5caa3bee5d3a7fd0bf18127a6b42524cca7ebf665fccf9c64b92e4719b3bc63e28ca284d4f771544628745bf98ea45856749d728b4f04ef64dc6d8d8884c9ae02ebfd81251c4561eb756e49756827571063f0258d2e1fb1462e1c30da77afca3523c68c6c470087c766208ad51d79eaea49b4052b186417df3ef9c6a9fe5c8126c137fb42c3624cd198b9a8de00b5dcb16926512%26x5step%3D100&scr=1366x768&cna=Rr/FFOd33jUCAXFpg3i8zi50&nick=cup%5Cu5514cup&spm-cnt=a220m.1000858.0.0.6e4c2a68USN3eO&category=2&uidaplus=2679497599&at_type=search&at_bucketid=sbucket%5f2&at_mall_pro_re=10001&aplus&at_rn=57bdbdf4e6ba584c0ed344c9886c1ebf&yunid=&feee337b757be&asid=AX/jtZ/B+T5cLqHIMwAAAAC5aEXGdleXsA==&p=1&o=win10&b=chrome63&s=1366x768&w=webkit&ism=pc&cache=fa94368&lver=8.8.0&jsver=aplus_std&pver=0.6.3&urlokey=J_Filter&aws=1&_hng=CN%25257Czh-CN%25257CCNY%25257C156&tag=1&stag=-1&lstag=-1&_slog=0')
# print(respsoner.status_code)


from selenium import webdriver
from selenium.webdriver import ActionChains
import time
import requests

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

response = requests.get('https://list.tmall.com/search_product.htm?q=%CA%D6%BB%FA&type=p&vmarket=&spm=875.7931836%2FB.a2227oh.d100&from=mallfp..pc_1_searchbutton',headers=request_header)
print(response.text)