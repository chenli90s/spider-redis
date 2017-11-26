# -*- coding: utf-8 -*-
import scrapy
from Tianqi.items import TianqiItem
import time
# ----1 导入类
from scrapy_redis.spiders import RedisSpider

# ----2 修改继承
# class TianqiSpider(scrapy.Spider):
class TianqiSpider(RedisSpider):
    name = 'tianqi'

    # ----3 注销允许的域和起始的url
    # allowed_domains = ['tianqi.com']
    # # 修改起始的URL
    # start_urls = ['http://lishi.tianqi.com/']

    # ----4 动态获取允许的域(可选)
    def __init__(self, *args, **kwargs):
        domain = kwargs.pop('domain','')
        self.allowed_domains = list(filter(None,domain.split(',')))
        super(TianqiSpider, self).__init__(*args, **kwargs)
    # ----5 redis_key
    redis_key = "tq"


    def parse(self, response):
        # 获取所有地区节点列表
        node_list = response.xpath('//ul[@class="bcity"]/li/a[@target="_blank"]')
        # print(len(node_list))
        # 遍历地区节点列表
        for node in node_list[10:15]:
            url = node.xpath('./@href').extract_first()
            area = node.xpath('./text()').extract_first()

            # 创建请求，添加meta
            yield scrapy.Request(url,callback=self.parse_area,meta={"meta_1":area})

    def parse_area(self, response):
        # print (response.url,'------')
        # 接收meta传参
        area = response.meta['meta_1']
        # 获取月份url列表
        url_list = response.xpath('//*[@id="tool_site"]/div[2]/ul/li/a/@href').extract()

        # 编列url列表
        for  url in url_list:
            # 发送请求
            yield scrapy.Request(url,callback=self.parse_data,meta={"meta_2":area})

    def parse_data(self, response):
        # print (response.url,'******')
        # 获取meta传参
        area = response.meta['meta_2']

        # 获取每一天数据的节点列表
        node_list = response.xpath('//div[@class="tqtongji2"]/ul')[1:]
        # 遍历
        for node in node_list:
            # 创建item实例
            item = TianqiItem()
            # 从节点中抽取数据
            item['area'] = area
            item['url'] = response.url
            item['timestamp'] = time.time()

            item['date'] = node.xpath('./li[1]/a/text()|./li[1]/text()').extract_first()
            item['max_t'] = node.xpath('./li[2]/text()').extract_first()
            item['min_t'] = node.xpath('./li[3]/text()').extract_first()
            item['weather'] = node.xpath('./li[4]/text()').extract_first()
            item['wind_direction'] = node.xpath('./li[5]/text()').extract_first()
            item['wind_power'] = node.xpath('./li[6]/text()').extract_first()

            # print (item)

            # 返回数据给引擎
            yield item





