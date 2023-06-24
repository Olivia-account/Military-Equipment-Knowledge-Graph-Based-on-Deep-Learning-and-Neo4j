# %% [markdown]
# # 导入库与设置请求头

# %%
import requests
from lxml import etree as et
import urllib
import urllib.request
import urllib.error
from bs4 import BeautifulSoup
import json
import time
import random
import os

# %%
# 请求头
headers = {
    # 用户代理
        'User-Agent': 'Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1'

    # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
}

USER_AGENT_LIST = [
    'MSIE (MSIE 6.0; X11; Linux; i686) Opera 7.23',
    'Opera/9.20 (Macintosh; Intel Mac OS X; U; en)',
    'Opera/9.0 (Macintosh; PPC Mac OS X; U; en)',
    'iTunes/9.0.3 (Macintosh; U; Intel Mac OS X 10_6_2; en-ca)',
    'Mozilla/4.76 [en_jp] (X11; U; SunOS 5.8 sun4u)',
    'iTunes/4.2 (Macintosh; U; PPC Mac OS X 10.2)',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:5.0) Gecko/20100101 Firefox/5.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:9.0) Gecko/20100101 Firefox/9.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:16.0) Gecko/20120813 Firefox/16.0',
    'Mozilla/4.77 [en] (X11; I; IRIX;64 6.5 IP30)',
    'Mozilla/4.8 [en] (X11; U; SunOS; 5.7 sun4u)'
]

# %% [markdown]
# # 确认页面请求状态

# %%
# 获取请求主页面、二级页面状态码
home_page = 'http://www.wuqibaike.com/index.php?category-view-8'
second_page = 'http://www.wuqibaike.com/index.php?doc-view-21590'
print('主网页请求情况：', requests.get(url=home_page, headers=headers).status_code)
print('二级页面网页请求情况：', requests.get(url=second_page, headers=headers).status_code)

# %% [markdown]
# # 函数准备

# %%
# 下载页面
def download(url, user_agent='wswp', num_retries=2):
    print('downloading: %', url)
    # 防止对方禁用Python的代理，导致forbidden错误
    headers = {'User-agent': user_agent}
    request = urllib.request.Request(url, headers=headers)
    try:
        html = urllib.request.urlopen(request).read()
    except urllib.error.URLError as e:
        print('download error:', e.reason)
        html = None
        if num_retries > 0:
            # URLError是一个上层的类，因此HttpERROR是可以被捕获到的。code是HttpError里面的一个字段
            if hasattr(e, 'code') and 500 <= e.code < 600:
                return download(url, num_retries - 1)
    return html

# %%
# 获得页面内容
def get_content(page_url):
    html_result = download(page_url)

    if html_result is None:
        print('is None')
        exit(1)
    else:
        pass
    
    # 分析得到的结果，从中找到需要访问的内容
    soup = BeautifulSoup(html_result, 'html.parser')
    return soup

# %%
# 生成所有主界面的urls，输入页数参数num(最多791页，每页10条)
def get_home_urls(main_url, start, end):
    home_urls = []
    for i in range(start, end+1, 1):
        home_page = main_url + str(i)
        home_urls.append(home_page)
    return home_urls

# %%
# 获取所有二级界面的urls
def get_second_urls(main_url, start, end):
    second_urls = []
    pages = get_home_urls(main_url, start, end)
    for page in pages:
        page_html = get_content(page)
        dls = page_html.find_all('dl', attrs={'class': 'col-dl'})
        for dl in dls:
            url = dl.find('a', attrs={'class': 'clink f20'})['href']
            url = 'http://www.wuqibaike.com/' + url
            second_urls.append(url)
    return second_urls

# %%
# 获取二级页面中的内容
def get_second_content(second_url,count):
    # 获取二级页面内容
    second_html = get_content(second_url)
    name = second_html.find('h1').find('a').text
    body = second_html.find('div', attrs={'class': 'content_topp'})
    content = second_html.find('div', attrs={'class': 'des'}).text
    
    p_all = body.find_all('p')
    for p in p_all:
        content = content + p.text + '\n'  
    return content


# %% [markdown]
# # 主函数
# ### 按照页数下载，重新写进data.txt、更新data.json文件

# %%
def main(main_url, first_page, last_page, if_auto_generate):
    main_url = "http://www.wuqibaike.com/index.php?category-view-1-"
    # 输入参数：页数范围
    second_urls = get_second_urls(main_url, first_page, last_page)  
    content = ""
    datas = {}
    # 生成文件名
    name = "data/data"+time.strftime('%m%d%H%M%S', time.localtime(time.time()))

    # 获得所有地面目标词条的文本数据，并存为 TXT 文件
    for i in range(len(second_urls)):
        try:
            time.sleep(random.random()*10)
            second_url = second_urls[i]
            content = content + get_second_content(second_url, i)
        except:
            continue
    with open(name+'.txt', "w", encoding="utf-8") as f:
        f.write(content)
    with open(name+'.txt', "r", encoding="utf-8") as f:
        text_all = f.readlines()
        text_all1 = []
        count_text = 0
        for i in range(len(text_all)):
            if text_all[i] != '\n':
                text_all1.append(text_all[count_text].strip('\n').strip('\t'))
                count_text += 1
    with open(name+'.txt', "w", encoding="utf-8") as f:
        for i in text_all1:
            f.write(i+"\n")
    
    # 生成满足目标数据集文件格式的 JSON 文件，同时自动生成“oid”作为该文本段的原始 id 
    data = {}
    data['id'] = {}

    with open(name+'.txt', "r", encoding="utf-8") as f:
        texts = f.readlines()
    count = 1000000000
    # 创建json文件
    with open(name+'.json', "w", encoding="utf-8") as f:
        f.write('\n')
        
    if if_auto_generate:
        # with open(r'F:\graduate_design\code\relation_k\datam\input.txt', 'w') as f:
        with open(root + r'\relation_k\datam\input.txt', 'w') as f:
            f.write('')
        for i in texts:
            if i != '\n':
                with open(root + r'\code\relation_k\datam\input.txt', 'a') as f:
                    f.write(i)
        strs = ('python ../../relation_k/predict_per_para.py')
        result1 = os.system(strs)

        with open(root + r'\code\relation_k\output\result.json', 'r') as f:
            datas = json.load(f)
            
        with open(root + r'\code\relation_k\datam\input.txt', "r", encoding="utf-8") as f:
            texts = f.readlines()
        for i in range(len(datas)):
    
            data['id']['oid'] = str(count)
            data['id']['text'] = texts[i]
            
            if len(datas[str(i)]['nodes']) != 0:
                for j in datas[str(i)]['nodes']:
                    if '名称' in datas[str(i)]['nodes'][j]:
                        datas[str(i)]['nodes'][j]['name'] = datas[str(i)]['nodes'][j]['名称']
            data['id']['nodes'] = datas[str(i)]['nodes']
            data['id']['rels'] = datas[str(i)]['rels']
            with open(name+'.json', 'a') as f:
                f.write(json.dumps(data, ensure_ascii=False))
                f.write('\n')
            count += 1
        
    else:
        for i in texts:
            if i != '\n':
                data['id']['oid'] = str(count)
                data['id']['text'] = i
                data['id']['nodes'] = {}
                data['id']['rels'] = {}
                with open(name+'.json', 'a') as f:
                    f.write(json.dumps(data, ensure_ascii=False))
                    f.write('\n')
                count += 1
    
    print('数据爬取完毕')
    


# %%
if __name__ == "__main__":
    main_url = "http://www.wuqibaike.com/index.php?category-view-8-"
    root = os.path.abspath(os.path.dirname(__file__))
    first_page = 1
    last_page = 1
    if_auto_generate = False
    main(main_url, first_page, last_page, if_auto_generate)


