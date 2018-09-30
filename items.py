class Phone:
    _id = ''
    id = ''
    name = ''  # 商品名称
    brand = ''  # 商品品牌
    model = ''  # 商品型号
    url = ''  # 商品链接
    source = ''  # 商品来源
    ram = ''  # 运行内存
    rom = ''  # 机身内存
    cpu = ''  # CPU型号
    video_url = ''  # 商品视频链接
    memory_card = ''  # 是否支持存储卡
    max_mem_sup = ''  # 内存卡最大扩展
    resolution = ''  # 分辨率
    figer = ''  # 是否支持指纹
    pack_list = ''  # 商品清单
    battery = ''  # 电池容量
    screen_size = ''  # 屏幕尺寸
    f_camera = ''  # 前置摄像头
    r_camera = ''  # 后置摄像头
    shop = {}  # 店铺信息，包含店铺名称(shop_name)和店铺的URL(shop_url)
    thumb_pic = []  # 缩略图
    #
    hot_spot = []  # 选购热点
    detail_url = []  # 详细图url
    description = ''
    extra_message = ''


class Price:
    # 下面是变化的属性
    _id = ''
    id = ''
    price = {}  # 手机价格，包含价格（price_value）和当前日期(date)


class SalePromotion:
    _id = ''
    id = ''
    sale_promotion = {}  # 包括了领券和满减(两个数组合并，然后统一用sale_promotion_value)，还有日期(date)


class Opinion:
    _id = ''
    id = ''
    opinion = {}  # 好评度(opnion_value)，包括好评数(high_number)、中评数(medium_number)、差评数(low_number)，还有百分比(high_rate)、当前日期(date)


class Impress:
    _id = ''
    id = ''
    impress = {}  # 印象标签，包括印象的名称(impress_name)，印象的数量(impress_number)，还有时间(date)


def object_to_dict(data):
    dict1 = dict(data.__dict__)
    del dict1['__module__']
    del dict1['__dict__']
    del dict1['__weakref__']
    del dict1['__doc__']
    return dict1