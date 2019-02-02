import requests
from bs4 import BeautifulSoup
import re

def open_url(url):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
    try:
        res = requests.get(url,headers=headers,timeout = 10).text
        return res
    except  requests.exceptions.ConnectTimeout as err:
        print('抱歉，连接超时:' +str(err))
    except  requests.exceptions.ConnectionError as err:
        print('请检查您的网络连接是否正常:' + str(err))
    except:
        print('未知的异常！')

def find_movie(res):
    soup = BeautifulSoup(res,'lxml')

    #序号
    number = []
    targets0 = soup.find_all('div',class_ = 'pic')
    for each in targets0:
        number.append(each.em.text + '.')

    #电影名
    movies = []
    targets1 = soup.find_all('div', class_='hd')
    for each in targets1:
        if len(each.select('a span')) == 2 :
            movies.append(each.select('a span')[0].text + each.select('a span')[1].text)
        else:
            movies.append(each.select('a span')[0].get_text() + each.select('a span')[1].get_text() + each.select('a span')[2].get_text())

    #评分
    ranks = []
    targets2 = soup.find_all('span',class_ = 'rating_num')
    for each in targets2:
        ranks.append('   评分:%s   '% each.text)

    #背景资料
    msg = []
    targets3 = soup.find_all('div',class_ = 'bd')
    for each in targets3:
        try:
            msg.append(each.p.text.split('\n')[1].strip()+each.p.text.split('\n')[2].strip())
        except:
            continue

    result = []
    length = len(movies)
    for each in range(length):
        result.append(number[each] + movies[each] + ranks[each] + msg[each] + '\n' + '\n' )


    return result

#找出有多少个页面
def find_page(res):
    soup = BeautifulSoup(res,'lxml')
    page = soup.find('span',class_ = 'next').previous_sibling.previous_sibling.text
    return int(page)

def main():
    hostname = 'https://movie.douban.com/top250'

    res = open_url(hostname)
    page = find_page(res)
    info = []

    for each in range(page):
        url = hostname + '?start=' + str(25*each)
        res = open_url(url)
        fm = find_movie(res)
        info.extend(fm)

    return info


    #with open('Top250豆瓣.txt','w',encoding='utf-8') as f:
        #for each in info:
           #f.write(each)


    #if name == '' or name == '/':
        #return '您没有输入任何相关信息'

    #elif name.isdigit():
        #if int(name.strip()) > 251 or int(name.strip()) <= 0:
            #return '抱歉！超出了搜索范围。'
        #else:
            #return (info[int(name.strip()) - 1])

#    else:
        #temp = []
        #for each in info:
            #if name in each:
                #temp.append(each)

        #if temp:
            #temp = ''.join(temp)
            #return temp
        #else:
            #return ('抱歉！没有找到任何相关记录。')

if __name__ == '__main__':
    #name = input('请输入您要查找的电影(导演、演员)名字或电影排名(评分)：')
    info = main()















