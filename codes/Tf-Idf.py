import jieba # 导入jieba库进行分词
import pickle
import json
import os
import re
from sklearn import feature_extraction # 导入sklearn库, 以获取文本的tf-idf值
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer

a_file = '../src/raw/89842206_Anaconda虚拟环境及PyCharm项目环境设置.blog'

def get_tf_idf(a_file):
    with open(a_file, 'r', encoding='utf-8') as file:
        txt = file.read()
        txt = re.sub(' +', ' ', txt)  # 将多个空格变成一个空格

    get_txt = []
    get_txt.append(' '.join(jieba.cut(txt, cut_all=False)))  # 将一个文本的分词内容以空格隔开作为一个元素, 多个文本时列表才显得有意义
    # print(get_txt)  # 输出

    mat = CountVectorizer()
    tf = TfidfTransformer()
    tfidf = tf.fit_transform(mat.fit_transform(get_txt))
    word = mat.get_feature_names()  # 单词的名称
    weight = tfidf.toarray()  # 权重矩阵, 在此示范中矩阵为(1, n)

    dic = {}  # 字典, [单词名称, 权重], 便于后面计算各个二进制位上的加权值(索引方便)
    for i in range(len(word)):
        dic[word[i]] = weight[0][i]
    # print(dic)
    show = sorted(dic.items(), key=lambda item: item[1], reverse=True)  # 按value排序, 查看文本主要内容
    # for each in show:
        # print(each)
    return dic

def get_link(url):
    with open("../src/indexes/links.pkl", 'rb') as file:
        links = pickle.load(file) # 读取字典{blog文件名：网络链接}
    # print(links)
    return links[url]

def get_local_urls():
    local_urls = os.listdir('../src/raw/')
    for each in local_urls:
        if ' ' in each:
            print(each)
    return local_urls

def adjust_weights(url, dic):
    txt = re.findall("../src/raw/.*_(.*)\.blog", url)[0]
    cut_words = jieba.lcut(txt, cut_all=True)
    for each in cut_words:
        dic[each] = dic.get(each, 0) + 0.5
    return dic

def main():
    urls = get_local_urls()
    print(urls)
    indexes = []
    for each in urls:
        url = '../src/raw/' + each
        one_index = {}
        one_index['from'] = each
        one_index['words'] = get_tf_idf(url)
        one_index['words'] = adjust_weights(url, one_index['words']) # 调整权重，使得标题权重更大
        one_index['link'] = get_link(each)
        indexes.append(one_index)
        # print(one_index)
    with open("../src/indexes/indexes.pkl", 'wb') as file:
        pickle.dump(indexes, file)
    # print(indexes)

if __name__ == '__main__':
    main()