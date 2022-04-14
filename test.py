#!/usr/bin/python3
# -*- coding: utf-8 -*-
import json
from lxml import etree
import re
import pandas as pd
import requests
from bs4 import BeautifulSoup
import time

# 定义请求头
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"
}

cookies = {
    'Cookies':'bid=qjf1zprHQ5A; __utmc=30149280; __utmc=223695111; ll="118371"; viewed="2252862"; douban-fav-remind=1; __utmz=30149280.1648520945.3.3.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __gads=ID=ef8521945c328054-221cccdb67d100c9:T=1648520947:RT=1648520947:S=ALNI_MYHsgxNZ-ge5AWgppYWYvx1JN_EjQ; push_noty_num=0; push_doumail_num=0; __utmv=30149280.25306; _vwo_uuid_v2=DB4BCA4273F64DF968E081C011B9A3B40|09689baca0f48fb5c4421933f6fd8a2e; __utmz=223695111.1649859827.5.5.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; ap_v=0,6.0; _pk_ref.100001.4cf6=["","",1649900533,"https://www.douban.com/"]; _pk_ses.100001.4cf6=*; __utma=30149280.1250153523.1648352387.1649859820.1649900533.7; __utmb=30149280.0.10.1649900533; __utma=223695111.1357127237.1648352387.1649859827.1649900533.6; __utmb=223695111.0.10.1649900533; dbcl2="253066269:LGDN2yzpYaA"; ck=J19w; _pk_id.100001.4cf6=794296baade17d9f.1648352387.6.1649904925.1649860142.'
}

def duanping(id = 0 ,file = 0,num = 0,hh = 1):
    url = "https://movie.douban.com/subject/"+str(id)+"/comments"

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
        total_data = []
        tree = etree.HTML(response.text)
        div_list = tree.xpath('//*[@id="comments"]/div')
        print(len(div_list))
        for list in div_list[:20]:
            vote_count = list.xpath('.//span[@class="votes vote-count"]/text()')[0]
            name = list.xpath('.//span[@class="comment-info"]/a/text()')[0]
            try:
                star_level = re.search('\d', list.xpath('.//span[@class="comment-info"]/span[2]/@class')[0]).group()
            except:
                star_level = ' '
            comment = str(list.xpath('.//span[@class="short"]/text()')[0])
            if(bool(hh)):
                comment = comment.replace('\n','').replace('\r','')
            pb_time=list.xpath('.//span[@class="comment-info"]/span[@class="comment-time "]/text()')[0].strip('\n').strip(' ').strip('\n')
            data=[name,star_level,vote_count,pb_time,comment]
            total_data.append(data)
        mydata=pd.DataFrame(total_data,columns=['name','star','vote_count','time','text'])
        if page_start==0:
            mydata.to_csv('./'+str(id)+'.csv',index=False,encoding="utf_8_sig")
        else:
            mydata.to_csv('./'+str(id)+'.csv',index=False,encoding="utf_8_sig",mode='a',header=False)
        time.sleep(0.08)

def yingping(id):
    """
    根据电影id获取评论
    :param id:
    :return:
    """
    url = "https://movie.douban.com/subject/"+str(id)+"/reviews"
    for page_start in range(0, 40, 20):

        print(f"page_start {page_start}")
        params = {
            "start":page_start
        }


        response = requests.get(
            url=url,
            headers=headers,
            params=params,
            cookies=cookies
        )
        bs = BeautifulSoup(response.text, 'lxml')
        comment_div_list = bs.find_all('div', attrs={'class':'main review-item'})

        # # 如果当前页已经没有影评退出循环
        # if len(comment_div_list)==0:
        #     break
        # print(len(comment_div_list))
        for comment_div in comment_div_list[:5]:

            id = comment_div.get('id')
            # print(id)
            # print(type(vote_count))
            print(id)
            # 用changpinglun加载一下长评论
            changpinglun(id)



def changpinglun(id = 0):
    """
    根据评论id 获取长评论
    :param id:
    :return: comments
    """
    url = "https://movie.douban.com/review/"+str(id)

    response = requests.get(
        url=url,
        headers=headers
    )

    content = response.text
    bs = BeautifulSoup(content,'lxml')
    # print(bs.find('div',id='link-report'))
    comment_list = bs.find('div', attrs={'class':'main-bd'}).find_all('p')
    comments = ''
    for comment_p in comment_list:
        comments = comments + comment_p.text +'\n'


    print(comments)
    time.sleep(2)
    return comments


duanping(26825482)
