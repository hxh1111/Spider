import requests
from bs4 import BeautifulSoup

def get_url(url):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
               'referer': 'https: // dianying.taobao.com /'
               }

    try:
        res = requests.get(url,headers = headers,timeout = 10).text
        return res
    except  requests.exceptions.ConnectTimeout as err:
        print('抱歉，连接超时:' +str(err))
    except  requests.exceptions.ConnectionError as err:
        print('请检查您的网络连接是否正常:' + str(err))
    except:
        print('未知的异常！')

    return None

def get_msg(res):
    #找到电影名
    soup = BeautifulSoup(res,'lxml')
    movie_name = soup.select('.bt-l')
    name = []
    for i in range(0,29):
        name.append(movie_name[i].text.center(20))

    #找电影评分
    movie_rank = soup.select('.bt-r')
    rank = []
    for i in range(len(name)):
        rank.append(('评分:'+movie_rank[i].text).center(21))

    #找电影信息
    movie_info = soup.select('.movie-card-list')
    info = []
    for i in range(len(name)):
        info.append(movie_info[i].text)

    #将信息汇总
    msg = []
    for i in range(len(name)):
        msg.append(name[i] + '\n' + rank[i] + info[i]+'\n\n')

    return msg

def get_main():
    url = 'https://dianying.taobao.com/showList.htm?spm=a1z21.3046609.w2.3.32c0112auAHTvG&n_s=new'
    res = get_url(url)
    msg = get_msg(res)
    msg = ''.join(msg)
    return msg

if __name__ == '__main__':
    msg = get_main()
    print(msg)








