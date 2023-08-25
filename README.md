# README

## 描述

将当天天气情况通过邮件发送给朋友的脚本。

数据的传输保存基本都是使用json格式，已经封装好了，感兴趣可以自行百度谷歌（了解python的朋友应该懂，就是字典）；

我自己使用没遇到啥bug，发现问题烦请指正，邮箱，私信或者issue；

随手写的小玩具，随缘维护o.O?



## 展示

### PC端

![image-20230826001345567](https://gitee.com/moni_world/pic_bed/raw/master/img/image-20230826001345567.png)



### 移动端

![image-20230826001520517](https://gitee.com/moni_world/pic_bed/raw/master/img/image-20230826001520517.png)



## 使用

1. 下载到本地；

2. 取得自己的邮箱token，注册和风天气，获取天气key；

3. 填写朋友信息在json文件中，就是姓名邮箱城市；

   > 注意：城市id需要自己去[和风api](https://dev.qweather.com/docs/api/geoapi/city-lookup/)获取，虽然可以写通用的但作为我个人来使用的话没啥必要，因为就发给寥寥数人（包括自己），大家基本也就在一个固定的地址；

4. 运行脚本：

   ```shell
   # 自己写一个脚本：send_weather.bat (win) / send_weather.sh (linux)
   python -u ./send_weather.py(windows可以替换成绝对地址)
   
   # windows双击打开即可
   
   # linux
   sh send_weather.sh
   ```

   或者pycharm直接运行也可，但shell运行更好，因为可以定时（请自行搜索linux和windows的定时启动脚本）；

详细教学地址：[python定时天气预报（邮件提醒）（部署到云服务器）](http://t.csdn.cn/3Xylp)



## 证书

**MIT**



## TODO

- [ ] 添加组件，如节日提醒，生日提醒和自然灾害预警，网易云每日一曲；
- [ ] 美化界面（邮件可以使用html语法，应该能做的很好看，我这个界面确实土味）；
- [ ] 部署到云服务器（得花钱买服务器啊，以后如果有其他需要买服务器的地方就顺便部署上去）；



## 友情链接

和风天气：https://console.qweather.com/#/console

一言：https://developer.hitokoto.cn/sentence/

搏天api：https://api.btstu.cn/



