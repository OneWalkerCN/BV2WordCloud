import time
import jieba.analyse
import requests as r
import re
import os
from bs4 import BeautifulSoup as bs
import jieba
from wordcloud import WordCloud
import matplotlib.pyplot as plt


#获取查询弹幕要用的cid
def get_cid(url):
    try:
        text = request_html(url)
        cid = re.findall(r'(?<=/)\d{10}',text)[0]
        return cid
    except Exception as e:
        print("error in getting cid:",e)
        return ""
    
#通用方法，获取html文本
def request_html(url) -> str:
    header = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0"
    }
    try:
        res = r.get(url,headers = header)
        res.raise_for_status()
        res.encoding = res.apparent_encoding
        soup = bs(res.text,features="xml")
        return soup.prettify()
    except Exception as e:
        print("访问失败",e)
        return ""
    
#获取弹幕文本
def get_comment_texts(url):
    commen_url = "https://comment.bilibili.com/"
    text_list = []
    try:
        cid = get_cid(url)
        comment_text = request_html(commen_url+cid+".xml")
        comment_soup = bs(comment_text,features="xml")
        d_list = comment_soup.find_all("d")
        for d in d_list:
            text_list.append(d.text.strip())
        return text_list
    except Exception as e:
        print("error in getting comment texts",e)
        return ""
    
#获取弹幕解词和权重
def get_jieci_list(comment_list):
    jieci_list = []
    try:
        for comment in comment_list:
            jieba.load_userdict("./customDict.txt")
            jieci_list.append(comment.strip())
        jieci_str = str(jieci_list)
        jieci_str = jieci_str.replace("'","")
        jieci_str = jieci_str.replace(","," ")
        # 提取关键词和权重
        freq = jieba.analyse.extract_tags(jieci_str,200,withWeight = True)  
        # 提取文件中的关键词，topK表示提取的数量，withWeight=True表示会返回关键词的权重。
        #print(freq)
        freq = {i[0]: i[1] for i in freq}  # 字典
        return freq
    except Exception as e:
        print("解词失败",e)

#展示和下载词云
def get_wordcloud(jieci_freq,bv):
    word_cloud = WordCloud(font_path="./handWriting.ttf",width=800,height=800,background_color="#ffffff").generate_from_frequencies(jieci_freq)
    plt.imshow(word_cloud,interpolation='bilinear')
    plt.axis("off")
    plt.show()
    pic_index = str(time.time())
    file_name = "./Pics/CommentCloud_"+bv+"_"+pic_index+".jpg"
    if not os.path.exists("./Pics"):
        print("新建Pics目录")
        os.mkdir("./Pics")
    print("保存词云图片到",os.path.abspath(file_name))
    word_cloud.to_file(file_name)
    
#封装函数，根据BV号获取词云
def bv_2_wordcloud(bv):
    bili_url = "https://www.bilibili.com/video/"
    comment_list = get_comment_texts(bili_url+bv)
    if comment_list:
        jieci_freq= get_jieci_list(comment_list)
        get_wordcloud(jieci_freq,bv)
    else:
        print("获取失败！")
    

if __name__ == "__main__":
    bv_2_wordcloud("BV17F4m1w7wf")
