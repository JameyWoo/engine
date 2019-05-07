import jieba
import pickle

def get_search_words():
    search = input('你想搜索什么？')
    search = jieba.lcut(search, cut_all=True)  # 全模式开启
    print(search)
    return search

def main():
    with open("../src/indexes/indexes.pkl", 'rb') as file:
        indexes = pickle.load(file)
    words = get_search_words()
    results = {}
    scores = []
    for each in indexes:
        res = 0
        for word in words: # 遍历每一个搜索词
            res += each['words'].get(word, 0)
        if res > 0:
            scores.append(res)
            if len(each['link']) > 0:
                results[each['link'][0]] = res
    # print(scores)
    # print(results)
    sorted_results = sorted(results.items(), key=lambda x: x[1], reverse=True)
    for each in sorted_results:
        print(each)

if __name__ == '__main__':
    main()