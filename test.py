#!/usr/bin/python3
# -*- coding: utf-8 -*-
import json
from lxml import etree
import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
import time

# 定义请求头
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"
}

cookies = {
    'Cookies':'bid=qjf1zprHQ5A; __utmc=30149280; ll="118371"; viewed="2252862"; douban-fav-remind=1; __utmz=30149280.1648520945.3.3.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __gads=ID=ef8521945c328054-221cccdb67d100c9:T=1648520947:RT=1648520947:S=ALNI_MYHsgxNZ-ge5AWgppYWYvx1JN_EjQ; push_noty_num=0; push_doumail_num=0; __utmv=30149280.25306; dbcl2="253066269:LGDN2yzpYaA"; ck=J19w; ap_v=0,6.0; _pk_ses.100001.8cb4=*; __utma=30149280.1250153523.1648352387.1649900533.1649933344.8; __utmt=1; _pk_id.100001.8cb4=d924c444428e1795.1648353221.5.1649933347.1649859825.; __utmb=30149280.4.10.1649933344'
}


def save_csv(total_data,path):
    mydata = pd.DataFrame(total_data, columns=['name', 'star', 'vote_count', 'time', 'text'])
    mydata.to_csv(path, mode='a+', index=False, encoding="utf_8_sig")


def duanping(id, save_dir):
    url = "https://movie.douban.com/subject/"+str(id)+"/comments"

    for page_start in range(0, 500, 20):
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
            params=params,
            cookies=cookies
        )

        total_data = []

        bs = BeautifulSoup(response.text,'lxml')
        div_list = bs.find_all('div',attrs={'class':'comment'})
        print(len(div_list))
        for div in div_list:
            vote_count = div.find('span',attrs={'class':'votes vote-count'}).text
            name = div.find('span',attrs={'class':'comment-info'}).find('a').text
            try:
                star_level = div.find('span',attrs={'class':'comment-info'}).find_all('span')[1].get('title')
            except:
                star_level = ''

            pb_time = div.find('span',attrs={'class':'comment-info'}).find_all('span')[-1].get('title')
            comment = div.find('span', attrs={'class':'short'}).text
            data=[name,star_level,vote_count,pb_time,comment]
            total_data.append(data)
        save_csv(total_data, path=save_dir+'/short_comments.csv')
        time.sleep(0.1)


def yingping(id):
    """
    根据电影id获取评论
    :param id:
    :return:
    """
    ### 短评论
    save_path = f'./{id}/comment'
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    duanping(id, save_path)
    url = "https://movie.douban.com/subject/"+str(id)+"/reviews"
    for page_start in range(0, 500, 20):

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

        #如果当前页已经没有影评退出循环
        if len(comment_div_list)==0:
            break

        for comment_div in comment_div_list:

            comment_id = comment_div.get('id')
            # print(id)

            print(comment_id)
            save_path = f'./{id}/comment'
            if not os.path.exists(save_path):
                os.makedirs(save_path)
            # 用changpinglun加载一下长评论
            changpinglun(comment_id,save_path)



def changpinglun(id,save_dir):
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
    # print(content)
    vote_count = bs.find('div', attrs={'class': 'main-panel-useful'}).find('button').text.split(' ')[-4]
    # print(vote_count)
    name = bs.find('header', attrs={'class': 'main-hd'}).find_all('span')[0].text

    try:
        star_level = bs.find('span', attrs={'class': 'main-title-rating'}).get('title')
    except:
        star_level = ''

    pb_time = bs.find('header', attrs={'class': 'main-hd'}).find_all('span')[-1].text

    comment_list = bs.find('div', attrs={'class':'main-bd'}).find_all('p')
    comments = ''


    for comment_p in comment_list:
        comments = comments + comment_p.text +'\n'

    # print(comments)
    comments=comments.strip('"')
    data = [name, star_level, vote_count, pb_time, comments]
    save_csv([data],path=save_dir+'/long_comments.csv')
    time.sleep(2)
    return comments


# changpinglun(26825482)

yingping(26825482)