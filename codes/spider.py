# 获取所有博客的url，并爬取他们的页面
# 分别将内容和格式存储到raw和xml文件夹中

import requests
import pickle
import json
import os
import re

def getUrls():
    list_urls = 'https://blog.csdn.net/wjh2622075127/article/list/'
    pattern = re.compile(r'<a href="(https://blog.csdn.net/wjh2622075127/article/details/.*)" target="_blank">')
    urls = []
    for i in range(1, 13):
        list_url = list_urls + str(i) + '?'
        list_page = requests.get(list_url).text
        get_urls = pattern.findall(list_page)
        for i in range(len(get_urls)):
            if i % 2 == 0:
                urls.append(get_urls[i])
    # print(urls)
    with open("../src/indexes/urls.pkl", 'wb') as file: # 存储链接列表
        pickle.dump(urls, file)
    return urls

def writeToFiles(urls):
    extfiles = os.listdir('../src/raw/')
    local_urls = []
    for url in urls:
        html = requests.get(url).text
        title = re.findall(r'<title>(.*) - 姬小野的博客 - CSDN博客</title>', html)[0]
        reps = ['\'', '\"', ' ', ':', r'/', '*']
        for each in reps:
            title = title.replace(each, '_')
        id = re.findall(r'details/(.*)', url)[0]
        # print(title, id)
        article = re.findall(r'(<article.*</article>)', html, re.S)[0]
        pattern = re.compile(r'<[^>]+>', re.S)
        result = pattern.sub('', article)
        rep_list = ['\n', '\t', url, '版权声明：看我干嘛? 你又没打算转载我的博客~']
        for each in rep_list:
            result = result.replace(each, ' ')
        # 保存博客内容到.blog文本
        path = r"../src/raw/" + id + '_' + title + '.blog'
        sub_path = id + '_' + title + '.blog'
        if sub_path in extfiles:
            pass
        else:
            local_urls.append(sub_path)
            with open(path, 'w+', encoding='utf-8') as file:
                file.write(result)
        # 保存含html标签的博客到xml文件中
        extfiles = os.listdir('../src/xmls/')
        path = r"../src/xmls/" + id + '_' + title + '.xml'
        sub_path = id + '_' + title + '.xml'
        if sub_path in extfiles:
            pass
        else:
            with open(path, 'w+', encoding='utf-8') as file:
                file.write(article)
    with open("../src/indexes/local_urls.pkl", 'wb') as file: # 存储链接列表
        pickle.dump(local_urls, file)

def get_links(): # 获取链接，写入到文件中
    files = os.listdir('../src/xmls/')
    links = {}
    for each in files:
        with open('../src/xmls/' + each, 'r', encoding='utf-8') as file:
            text = file.read()
            link = re.findall(r'(https://blog.csdn.net/wjh2622075127/article/details/[\d]+)', text)
            links[each.replace('.xml', '.blog')] = link
    # print(links)

def main():
    urls = getUrls()
    # writeToFiles(urls)
    get_links()

if __name__ == '__main__':
    main()