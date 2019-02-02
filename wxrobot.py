from wxpy import *
from weather import all
from tops import main
from movies import get_main
import time

#天气查询
city = {'北京':'beijing/beijing',
        '上海':'shanghai/shanghai',
        '深圳':'guangdong/shenzhen',
        '广州':'guangdong/guangzhou',
        '东莞':'guangdong/dongguan',
        '河源':'guangdong/heyuan'}
msg1 = all('北京市')
msg2 = all('上海市')
msg3 = all('广州市')
msg4 = all('深圳市')
msg5 = all('东莞市')
msg6 = all('河源市')
msg7 = all('清远市')
file = 'Top250豆瓣.doc'
movie_info = main()
#movie_info = ''.join(movie_info)        #格式化list

invite_text = "Hello!Py机器人很高兴为你服务。回复'功能 + 数字'获取对应功能\n1.天气查询\n2.豆瓣top250电影排行查询\n3.网易云热门音乐查询\n4.近期上映电影查询\n例如：要获取查询天气的功能时回复\n\n功能1"  #任意回复获取的菜单
menu_1 = '功能1'
menu_2 = '功能2'
menu_3 = '功能3'
menu_4 = '功能4'
friend = '伟城'

bot = Bot(cache_path = True)
bot.enable_puid()    #启用聊天对象的puis属性
xiaoi = XiaoI('open_NalJ6YZfiVkc','NrtVjWBbI5py4YqPrujt')
adminer = bot.friends(update=True).search(friend)[0]

def invite_weather(user,text):
    check_weather = text
    msg1 = all(check_weather)
    user.send(msg1)

def invite_movie(user,text):
    if 't' in text:
        check_num = int(text.split('t')[1])
        if check_num in range(1,251):
            user.send((movie_info[int(check_num) - 1]))
        else:
            user.send('抱歉！超出了搜索范围! >.<')

    else:
        check_num = int(text.split('T')[1])
        if check_num in range(1, 251):
            user.send((movie_info[int(check_num) - 1]))
        else:
            user.send('抱歉！超出了搜索范围! >.<')

#注册自动回复好友消息
@bot.register(adminer,msg_types = TEXT)
def adminer(msg):
    if menu_1 in ''.join(msg.text.split()):
        msg.sender.send('请输入您要查找的城市(仅限北上广深、河源、东莞、清远):')
        #invite_weather(msg.sender,msg.text)

    elif menu_2 in ''.join(msg.text.split()):
        #msg.sender.send('请稍等，后台正在处理数据...')
        #time.sleep(2)
        msg.sender.send('请输入您要查找的电影排名(t1-t250):\n例如：要获取排名第1的电影时回复：t1')
    elif 't' in ''.join(msg.text.split()).lower():
        msg.sender.send('请稍等，机器人正在爬取数据...')
        invite_movie(msg.sender,msg.text)

    elif menu_3 in ''.join(msg.text.split()):
        return '网易云热门音乐查询功能测试中'

    elif menu_4 in ''.join(msg.text.split()):
        msg.sender.send('请稍等，机器人正在爬取数据...')
        hot_movie = get_main()
        msg.sender.send('正在热映的电影：\n' + hot_movie+'以上信息由Py机器人提供\n'+'数据来源：淘票票网\n' + 'Have a nice day!^_^')

    elif '北京' in ''.join(msg.text.split()):
        msg.sender.send('请稍等，机器人正在爬取数据...')
        time.sleep(1.5)
        msg.sender.send(msg1)
    elif '上海' in ''.join(msg.text.split()):
        msg.sender.send('请稍等，机器人正在爬取数据...')
        time.sleep(1.5)
        msg.sender.send(msg2)
    elif '广州' in ''.join(msg.text.split()):
        msg.sender.send('请稍等，机器人正在爬取数据...')
        time.sleep(1.5)
        msg.sender.send(msg3)
    elif '深圳' in ''.join(msg.text.split()):
        msg.sender.send('请稍等，机器人正在爬取数据...')
        time.sleep(1.5)
        msg.sender.send(msg4)
    elif '东莞' in ''.join(msg.text.split()):
        msg.sender.send('请稍等，机器人正在爬取数据...')
        time.sleep(1.5)
        msg.sender.send(msg5)
    elif '河源' in ''.join(msg.text.split()):
        msg.sender.send('请稍等，机器人正在爬取数据...')
        time.sleep(1.5)
        msg.sender.send(msg6)
    elif '清远' in ''.join(msg.text.split()):
        msg.sender.send('请稍等，机器人正在爬取数据...')
        time.sleep(1.5)
        msg.sender.send(msg7)

    else:
        msg.sender.send('抱歉！没有找到相关的信息。\n如果你对我们有什么想法或者建议，欢迎留言给Py机器人，谢谢合作。')
        msg.sender.send(invite_text)
bot.join()
