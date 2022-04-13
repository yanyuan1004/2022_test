#!/usr/bin/python3
# -*- coding: utf-8 -*-
import json
from lxml import etree
import re
import pandas as pd
import requests

# 定义请求头
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"
}
def duanping(id = 0 ,file = 0,num = 0):
    url = "https://movie.douban.com/subject/"+str(26825482)+"/comments"

    for page_start in range(0, 20, 20):
        if page_start == 0:
            params = {
                "sort": "new_score",
                "status": "P",
                "limit": 20
            }
        else:
            params = {
                "sort": "new_score",
                "status": "P",
                "limit": 20,
                "start":page_start
            }
        response = requests.get(
            url=url,
            headers=headers,
            params=params
        )
        
        tree = etree.HTML(response.text)
        div_list = tree.xpath('//*[@id="comments"]/div')
        print(len(div_list))
        for list in div_list[:20]:
            vote_count = list.xpath('.//span[@class="votes vote-count"]/text()')[0]
            print(vote_count)
        
def yingping():
    url = "https://movie.douban.com/subject/"+str(26825482)+"/reviews"
    for page_start in range(0, 20, 20):
        params = {
            "start":page_start
        }
        response = requests.get(
            url=url,
            headers=headers,
            params=params
        )
        tree = etree.HTML(response.text)
        div_list = tree.xpath('/html/body/div[3]/div[1]/div/div[1]/div[1]/div')
        print(len(div_list))
        for list in div_list[:20]:
            usr_id = list.xpath('.//div[@class="main review-item"]')[0]
            id = usr_id.get('id')
            # print(type(vote_count))
            print(id)
            #用changpinglun加载一下长评论
            
def changpinglun(id = 0):
    url = "https://movie.douban.com/j/review/"+str(14323672)+"/full"#14322777

    response = requests.get(
        url=url,
        headers=headers
    )

    content = response.content
    results = json.loads(content)#可能出现json空的bug
    print((results["html"]))


yingping()