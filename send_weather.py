#  用提供好的api爬取天气数据，然后发送给邮箱
import requests
import json
from email.mime.text import MIMEText
import smtplib
import re

# 和风天气key
weather_key = 'YOUR KEY'
# qq邮箱token，也可以用别的邮箱
email_token = 'YOUR TOKEN'

# 得到数据，用json中的city_name来检索
# TODO: 可以用和风天气api来获取城市id，但是我自己使用量不大，也就发给固定几个人。所以就不写一些通用代码了。
city_lst = {'成都市温江区': '101270104', '北京市': '101010100', '绵阳市涪城区': '101270409'}


# 检测下雨
def is_rain(text):
    patten = ".?雨.?"
    match = re.match(patten, text)
    return match


def is_good_weather(text):
    patten = ".?晴.?"
    match = re.match(patten, text)
    return match


# 获取今日天气信息
def get_today_info(city_id):
    raw_url = f'https://devapi.qweather.com/v7/weather/24h?location={city_id}&key={weather_key}'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}
    r = requests.get(raw_url, headers=headers)
    now = json.loads(r.text)
    url = now['fxLink']
    return url


# 每日骚话
def get_yiyan():
    url = "https://v1.hitokoto.cn/"
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}
    r = requests.get(url, headers=headers)
    jsons = json.loads(r.text)
    return jsons


def get_pic():
    url = "https://api.btstu.cn/sjbz/api.php?lx=dongman&format=json"
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}
    r = requests.get(url, headers=headers)
    jsons = json.loads(r.text)
    return jsons


# TODO: 添加节假日信息和朋友生日信息
def get_info(city_id, name, yiyan, pic_url):
    url = f'https://devapi.qweather.com/v7/weather/3d?location={city_id}&key={weather_key}'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}
    r = requests.get(url, headers=headers)
    now = json.loads(r.text)
    today_info = now['daily'][0]
    stat = ''
    tempMax = today_info['tempMax']
    tempMin = today_info['tempMin']
    textDay = today_info['textDay']
    textNight = today_info['textNight']
    today_url = get_today_info(city_id)

    stat = f"<h3>今日气温: {tempMin}℃~{tempMax}℃</h3>" \
           f"<h3>日间天气情况: {textDay}<br>" \
           f"夜间天气情况: {textNight}</h3>" \
           f"<h3>祝{name}天天开心，早日赚钱来养哥们^_^</h3>" \

    # 降雨提醒
    if is_rain(textDay + textNight):
        stat += f"tips: 今天好像会下雨，适合在家打游戏睡觉，如果要出门的话记得带伞哦<br>"
    elif is_good_weather(textDay + textNight):
        stat += f"哇哦，今天天气不错欸，要不出去溜达溜达？<br>"

    # 图片和一言
    stat += f"<br><h3 style=\"text-align: center;\"><i>\"{yiyan['hitokoto']}\"</i></h3>"
    stat += f"<h4 style=\"text-align: right;\"><i>——《{yiyan['from']}》 {yiyan['from_who']}</i></h4>"
    # FIXME: 对前端不太懂，pc端宽高不适应，因电脑屏幕大小而出现溢出等现象
    width: int = int(int(pic_url['width']) * 0.6)
    height: int = int(int(pic_url['height']) * 0.6)

    stat += f"<p style=\"text-align: center;\"><img src=\"{pic_url['imgurl']}\" " \
            f"alt=\"图像描述\" width=\"{width}\" height=\"{height}\"></p>"

    # 今日天气详情
    stat += f"<br><a href={today_url}>今日天气详情</a><br>"
    stat += f"<br>退订或修改地址请私聊或call me，想哥就联系哥o.O?<br>"

    # print(stat)

    return stat


#  邮件传输
def smtp_tran(data, name, email, city_name):
    # print(data)
    msg = MIMEText(data, 'html', 'utf-8')
    HOST = 'smtp.qq.com'
    SUBJECT = f'{name}, 这是{city_name}今天的天气情况'
    FROM = 'YOUR@qq.com'   # 填你自己的邮箱
    TO = f'{email}'
    msg['Subject'] = SUBJECT
    msg['From'] = FROM
    msg['To'] = TO
    server = smtplib.SMTP(HOST, 25)
    server.set_debuglevel(1)
    server.login(FROM, f'{email_token}')
    server.sendmail(FROM, [TO], msg.as_string())
    server.quit()


# 对自己发邮件测试
def test_single(file_path):
    yiyan = get_yiyan()
    pic = get_pic()
    with open(file_path, 'r', encoding='utf-8') as rf:
        all_info = json.load(rf)
        info = all_info[0]
        city_name = info['city_name']
        name = info['name']
        email = info['email']
        city_id = city_lst[city_name]
        data = get_info(city_id, name, yiyan, pic)
        smtp_tran(data, name, email, city_name)


# 读取json文件，发送天气给json文件中记录的朋友
def send_to_all(file_path):
    yiyan = get_yiyan()
    pic = get_pic()
    with open(file_path, 'r', encoding='utf-8') as rf:
        all_info = json.load(rf)
        for info in all_info:
            city_name = info['city_name']
            name = info['name']
            email = info['email']
            city_id = city_lst[city_name]
            data = get_info(city_id, name, yiyan, pic)
            smtp_tran(data, name, email, city_name)


if __name__ == '__main__':
    # 发送给所有人
    # send_to_all("friend_info.json")

    # 测试
    test_single("friend_info.json")

    # print(get_pic())
