import requests
from bs4 import BeautifulSoup
import re
import time

city = {'北京市': 'beijing/beijing',
        '上海市': 'shanghai/shanghai',
        '深圳市': 'guangdong/shenzhen',
        '广州市': 'guangdong/guangzhou',
        '东莞市': 'guangdong/dongguan',
        '河源市': 'guangdong/heyuan',
        '清远市':'guangdong/qingyuan'}

def opens_url(url):
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        'Connection':'keep - alive',
        'Content - Type': 'text / html;charset = UTF - 8',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
    }
    try:
        res = requests.get(url,headers = headers,timeout = 10)
        return res
    except  requests.exceptions.ConnectTimeout as err:
        print('抱歉，连接超时:' +str(err))
    except  requests.exceptions.ConnectionError as err:
        print('请检查您的网络连接是否正常:' + str(err))
    except:
        print('未知的异常！')

def get_info(res,name):
    soup = BeautifulSoup(res.text,'lxml')
    weather_all = {}

# 当前天气\温度\更新时间\湿度\风向风力\温馨提示\空气质量
    weather_all['current_weather'] = re.search(r'([\u4e00-\u9fa5]{1,2})',str(soup.select('.wea_weather b'))).group(1)
    weather_all['curren_temperature'] = re.search(r'>(.\d?\d?)<',str(soup.select('.wea_weather em'))).group(1)
    weather_all['update_time'] = re.search(r'>([\u4e00-\u9fa5]+\d\d?:\d\d?[\u4e00-\u9fa5]+?)<',str(soup.select('.wea_weather strong'))).group(1)
    weather_all['humidity'] = re.search(r'([\u4e00-\u9fa5]+\s\d\d?%)',str(soup.select('.wea_about span'))).group(1)
    weather_all['wind'] = re.search(r'([\u4e00-\u9fa5]+?\d+?[\u4e00-\u9fa5]+?)',str(soup.select('.wea_about em'))).group(1)
    weather_all['tips'] = soup.select('.wea_tips em')[0].text
    weather_all['aircon'] = re.search(r'(\d\d?\s[\u4e00-\u9fa5]+?)',str(soup.select('.wea_alert em'))).group(1)

    weathercast_list = soup.select('.forecast li')
 # 今天天气\温度\风向\风力\空气质量
    weather_all['today_weather'] = re.search(r'"(.+?)"', str(weathercast_list[4])).group(1)
    weather_all['today_temperature'] = re.search(r'>(.+)<',str(weathercast_list[5])).group(1)
    weather_all['today_wind_direction'] = re.search(r'<em>(.+?)</em>', str(weathercast_list[6])).group(1)
    weather_all['today_wind_force'] = re.search(r'<b>(.+?)</b>',str(weathercast_list[6])).group(1)
    weather_all['today_aircon'] = re.search(r'">\s+(\d+\s[\u4e00-\u9fa5]+?)\s+</st',str(weathercast_list[7])).group(1)

# 明天天气\温度\风向\风力\空气质量
    weather_all['tm_weather'] = re.search(r'"(.+?)"',str(weathercast_list[9])).group(1)
    weather_all['tm_temperature'] = re.search(r'>(.+)<',str(weathercast_list[10])).group(1)
    weather_all['tm_wind_direction'] = re.search(r'<em>(.+?)</em>', str(weathercast_list[11])).group(1)
    weather_all['tm_wind_force'] =  re.search(r'<b>(.+?)</b>',str(weathercast_list[11])).group(1)
    weather_all['tm_aircon'] = re.search(r'">\s+(\d+\s[\u4e00-\u9fa5]+?)\s+</st', str(weathercast_list[12])).group(1)

# 后天天气\温度\风向\风力\空气质量
    weather_all['dtm_weather'] = re.search(r'"(.+?)"', str(weathercast_list[14])).group(1)
    weather_all['dtm_temperature'] = re.search(r'>(.+)<', str(weathercast_list[15])).group(1)
    weather_all['dtm_wind_direction'] = re.search(r'<em>(.+?)</em>', str(weathercast_list[16])).group(1)
    weather_all['dtm_wind_force'] = re.search(r'<b>(.+?)</b>', str(weathercast_list[16])).group(1)
    weather_all['dtm_aircon'] = re.search(r'">\s+(\d+\s[\u4e00-\u9fa5]+?)\s+</st', str(weathercast_list[17])).group(1)

#封装信息
    times = []
    for each in time.localtime() :
        times.append(each)

    msg = []
    msg.append('          ****%s天气情况****           ' % name)
    msg.append('现在是北京时间:%d年%d月%d日%d时%d分%d秒' % (times[0],times[1],times[2],times[3],times[4],times[5]))
    msg.append('数据于%s' % (weather_all['update_time']))
    msg.append(' ')
    msg.append('当前天气：%s' % (weather_all['current_weather']))
    msg.append('当前气温：%s度' % (weather_all['curren_temperature']))
    msg.append('当前湿度：%s' % (weather_all['humidity']))
    msg.append('当前风向\风力：%s' % (weather_all['wind']))
    msg.append('当前空气质量：%s' % (weather_all['aircon']))
    msg.append('温馨提示：%s' % (weather_all['tips']))
    msg.append(' ')
    msg.append('****三日天气预报****')
    msg.append(' ')
    msg.append('---今天---')
    msg.append('天气：%s' % (weather_all['today_weather']))
    msg.append('气温：%s度' % (weather_all['today_temperature']))
    msg.append('风向\风力：%s%s' % (weather_all['today_wind_direction'], weather_all['today_wind_force']))
    msg.append('空气质量：%s' % (weather_all['today_aircon']))
    msg.append(' ')
    msg.append('---明天---')
    msg.append('天气：%s' % (weather_all['tm_weather']))
    msg.append('气温：%s度' % (weather_all['tm_temperature']))
    msg.append('风向\风力：%s%s' % (weather_all['tm_wind_direction'], weather_all['tm_wind_force']))
    msg.append('空气质量：%s' % (weather_all['tm_aircon']))
    msg.append(' ')
    msg.append('---后天---')
    msg.append('天气：%s' % (weather_all['dtm_weather']))
    msg.append('气温：%s度' % (weather_all['dtm_temperature']))
    msg.append('风向\风力：%s%s' % (weather_all['dtm_wind_direction'], weather_all['dtm_wind_force']))
    msg.append('空气质量：%s' % (weather_all['dtm_aircon']))
    msg.append(' ')
    msg.append('以上信息由Py机器人提供')
    msg.append('数据来源：墨迹天气网')
    msg.append('Have a nice day!^_^')

    msg = '\n'.join(msg)
    return msg

def all(name):
    hostname = 'https://tianqi.moji.com/weather/china/'
    url = hostname + city[name]
    res = opens_url(url)
    msg = get_info(res,name)
    return msg

    #else:
        #return '抱歉！没有搜索到相关城市的天气信息。\nPy机器人会陆续更新城市的天气信息，敬请期待!'
if __name__ == '__main__':
    name = input('请输入您要查找的城市：')
    all(name)







