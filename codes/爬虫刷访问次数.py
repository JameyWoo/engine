import requests

url = 'https://blog.csdn.net/wjh2622075127/article/details/89842206'
url2 = 'https://blog.csdn.net/wjh2622075127/article/details/89816323'
for i in range(10):
    html = requests.get(url)