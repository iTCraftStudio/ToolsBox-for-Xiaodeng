import pygame
import easygui
import urllib.request
import json
import fanyi
import time
import log as logs
from log import log
import json
import threading
import login
import sys
import requests
import random
import hsd
import os
from win10toast import ToastNotifier

__ver__ = 2.4
timer = time.time()

log(f"正在启动 XiaoDengCode's Tools Box [Version:{__ver__}]")
log("读取内置插件")
log(f"组件[Fanyi]版本号: {fanyi.__ver__}")
log(f"组件[log]版本号：{logs.__ver__}")
log(f"组件[login]版本号：{login.__ver__}")

log(f"正在读取配置文件 . . .")
f = open("./config/user.json","r",encoding = "utf-8")
config_uid = json.loads(f.read())["uid"]
f.close()
log(f"用户UID：{config_uid}")

if config_uid == "":
    log("=== 此用户没有登录！ ===","[WARN]")
    log("加载登录选项 . . .")
    if login.login() == 1:
        sys.exit()
    else:
        sys.exit()
        
log("初始化窗口")
pygame.init()
screen = pygame.display.set_mode((600,400))
pygame.display.set_caption(f"小邓の工具箱{__ver__}专业版 (By：小邓学编程)")
pygame.display.set_icon(pygame.image.load("./src/icon.ico"))
log("完成")

log("初始化变量")
bg = (135,206,250)
x = 0
y = 500
fps = 0
_fps = 0
tools_x = 500
jrrp_action = 1
today_thread = None
toast = ToastNotifier()
today_text = ""
today_back = 1
today_action = 1
_hsd = None
fanyi_action = 1
hsd_action = 1
about_action = 0
fanyi_thread = None
scr = 0
fanyi_text = None
pos = (0,0)
timer1 = None
hour = time.localtime(time.time())[2]
USER = login.dectry(config_uid).split("|")
log("完成")

if 0 <= hour <= 12:
    hello = f"早上好，{USER[0]} ！"
elif 12 <= hour <= 13:
    hello = f"中午好，{USER[0]} ！"
elif 13 <= hour <= 17:
    hello = f"下午好，{USER[0]} ！"
elif 18 <= hour <= 24:
    hello = f"晚上好，{USER[0]} ！"
else:
    hello = f"你好，{USER[0]} ！"

log("初始化素材")
user = pygame.font.Font("./src/welcame.ttf",40).render(hello,bg,(255,255,255))
about = pygame.font.Font("./src/about.ttf",20).render(f"小邓的工具箱(版本：{__ver__}，By:小邓学编程)",bg,(255,255,255))
about_act = pygame.font.Font("./src/about.ttf",20).render(f"小邓的工具箱(版本：{__ver__}，By:小邓学编程)",bg,(255,0,0))
about_test = pygame.font.Font("./src/font.ttf",17)
fps_show = pygame.font.Font("./src/about.ttf",20)
jrrp_button_a = pygame.image.load("./src/jrrp_button.png")
today_font = pygame.font.Font("./src/font.ttf",20)
jrrp_button_b = pygame.image.load("./src/jrrp_button_action.png")
jrrp_int = pygame.font.Font("./src/welcame.ttf",200)
wait = pygame.font.Font("./src/font.ttf",35)
msg1 = pygame.font.Font("./src/font.ttf",25).render("亿些稀奇古怪的东西（",bg,(255,255,255))
today_button_a = pygame.image.load("./src/today_button.png")
today_button_b = pygame.image.load("./src/today_button_action.png")
fanyi_button_a = pygame.image.load("./src/fanyi_button.png")
fanyi_button_b = pygame.image.load("./src/fanyi_button_action.png")
hsd_button_a = pygame.image.load("./src/cave_button.png")
hsd_button_b = pygame.image.load("./src/cave_button_action.png")
fanyi_title = pygame.font.Font("./src/font.ttf",30)
fanyi_test = pygame.font.Font("./src/font.ttf",20)
hsd_text = pygame.font.Font("./src/welcame.ttf",25)
hsd_thank = pygame.font.Font("./src/welcame.ttf",22).render("感谢 StarWorld、服作者 提供回声洞服务！",bg,(255,255,0))
"""
down_button_a = pygame.image.load("./src/downloader_button.png")
down_button_b = pygame.image.load("./src/downloader_action.png")
"""
log("完成")
log("初始化函数")

def jrrp():
    now = time.localtime(time.time())
    d = now[0] * 10000 + now[1] * 100 + now[2]
    c = ""
    for i in config_uid.split("_"):
        c += i
    c = int(c)
    return (((d+1324)*(((d+154)*(c+1))%(c+3421)+((d+879)*(c+34))%((c+413)%(9*(((d+87)*(c+213))%((c+45)+76))))))+(((d+1)*(c+43))%(c+1)+((d+234)*(c+654))%((c+32)%(453*(((d+5362)*(c+532))%((c+86)+234)))))+91312)%1001

def fanyi_thread_target():
    global fanyi_text
    fanyi_text = easygui.codebox("请输入翻译原文（中文）",
                                 "ToolsBox生草")

def today_thread_target():
    global today_text
    req = requests.get(f"https://www.ipip5.com/today/api.php?type=txt")
    today_text = req.text

def welcame():
    toast.show_toast(title=hello,
                     msg=f"小邓の工具箱{__ver__}专业版 已准备完毕，感谢您的使用。",
                     icon_path=r"./src/tool.ico",
                     duration=10)
log("完成！")
log(f"初始化完成，用时{time.time() - timer}秒，计时器重置，进入循环。")
threading.Thread(target=welcame).start()    # 把消息框作为多线程启动，避免阻塞主线程
timer = time.time()
while __name__ == "__main__":
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            log("===* 程序退出 *===",lv = "[WARN]")
            sys.exit()
        elif event.type == pygame.MOUSEMOTION:
            pos = event.pos
        elif event.type == pygame.WINDOWMINIMIZED or event.type == pygame.WINDOWFOCUSLOST:
            pygame.display.set_caption(f"离开ing：小邓の工具箱{__ver__}专业版 (By：小邓学编程)")
        elif event.type == pygame.WINDOWEXPOSED:
            pygame.display.set_caption(f"小邓の工具箱{__ver__}专业版 (By：小邓学编程)")
        elif event.type == pygame.MOUSEWHEEL and scr == 0:
            if event.y > 0:
                tools_x += event.y * 10
            else:
                tools_x += event.y * 4
        elif event.type == pygame.MOUSEWHEEL and scr == 2:
            y += event.y * 10
        elif event.type == pygame.MOUSEBUTTONDOWN and scr == 0:
            if event.button == 1:
                if jrrp_action == 0:
                    scr = 1
                elif today_action == 0:
                    scr = 2
                elif fanyi_action == 0:
                    scr = 3
                elif hsd_action == 0:
                    scr = 4
                elif about_action:
                    scr = 5
        elif event.type == pygame.MOUSEBUTTONDOWN and (scr != 0):
            if event.button == 1:
                if today_back:
                    y = 0
                    scr = 0
                    today_back = 1
        else:
            log(event,lv = "[EVENT]")
            
    now = time.localtime(time.time())
    if 380 <= pos[1] <= 400 and 5 <= pos[0] <= 365:
        screen.blit(about_act,(5,380))
        about_action = 1
    else:
        screen.blit(about,(5,380))
        about_action = 0
    screen.blit(fps_show.render(f"FPS:{fps}",bg,(255,255,255)),(390,380))
    screen.blit(fps_show.render(f"{now[3]}:{now[4]}:{now[5]}",bg,(255,255,255)),(480,380))
    if y >= 0:
        y -= 0.5
    if time.time() - timer >= 1:
        fps = _fps
        _fps = 0
        timer = time.time()
    _fps += 1

    if scr == 0:
        screen.blit(user,(x+5,y+5))
        
        if (x+tools_x+0) <= pos[0] <= (x+tools_x+256):
            if (y+88) <= pos[1] <= (y+88+256):
                jrrp_action = 0
                screen.blit(jrrp_button_b,(x+tools_x+0,y+88))
            else:
                jrrp_action = 1
                screen.blit(jrrp_button_a,(x+tools_x+0,y+88))
        else:
            jrrp_action = 1
            screen.blit(jrrp_button_a,(x+tools_x+0,y+88))
        if (x+tools_x+300) <= pos[0] <= (tools_x+556) and (y+88) <= pos[1] <= (y+88+256):
            today_action = 0
            screen.blit(today_button_b,(x+tools_x+300,y+88))
        else:
            today_action = 1
            screen.blit(today_button_a,(x+tools_x+300,y+88))
        screen.blit(msg1,(x+tools_x+600,y+88))
        if (x+tools_x+600) <= pos[0] <= (x+tools_x+600+256) and (y+88+35) <= pos[1] <= (y+88+35+100):
            screen.blit(fanyi_button_b,(x+tools_x+600,y+88+35))
            fanyi_action = 0
        else:
            screen.blit(fanyi_button_a,(x+tools_x+600,y+88+35))
            fanyi_action = 1
        if (x+tools_x+600) <= pos[0] <= (x+tools_x+600+256) and (y+88+100+35+21) <= pos[1] <= (y+88+100+35+21+100):
            screen.blit(hsd_button_b,(x+tools_x+600,y+88+100+35+21))
            hsd_action = 0
        else:
            screen.blit(hsd_button_a,(x+tools_x+600,y+88+100+35+21))
            hsd_action = 1
        if tools_x <= 0-900:
            tools_x = 600
        tools_x -= 0.2
    elif scr == 1:
        screen.blit(wait.render("你今天的人品值是：",bg,(0,0,0)),(x+5,y+5))
        if timer1 == None:
            timer1 = time.time()
        if time.time() - timer1 >= 5:
            screen.blit(jrrp_int.render(str(jrrp()) + "‰",bg,(0,0,0)),(x+5,y+35))
        else:
            screen.blit(jrrp_int.render(str(random.randint(0,1000)) + "‰",bg,(0,0,0)),(x+5,y+35))
        y1 = 235
        if not(y+y1 <= pos[1] <= y+y1+20):
            screen.blit(today_font.render("返回首页",bg,(0,0,0)),(x+5,y+y1))
            today_back = 0
        else:
            screen.blit(today_font.render("返回首页",bg,(255,0,0)),(x+5,y+y1))
            today_back = 1
        y1 = 5
    elif scr == 2:
        if today_thread != None:
            if today_thread.is_alive():
                screen.blit(wait.render("正在载入：历史上的今天",bg,(0,0,0)),(x+5,y+5))
            else:
                y1 = 5
                for t in today_text.split("\n"):
                    screen.blit(today_font.render(t,bg,(0,0,0)),(x+5,y+y1))
                    y1 += 25
                
                if not(y+y1 <= pos[1] <= y+y1+20):
                    screen.blit(today_font.render("返回首页",bg,(0,0,0)),(x+5,y+y1))
                    today_back = 0
                else:
                    screen.blit(today_font.render("返回首页",bg,(255,0,0)),(x+5,y+y1))
                    today_back = 1
        else:
            today_thread = threading.Thread(target=today_thread_target)
            today_thread.start()
    elif scr == 4:
        screen.blit(wait.render("回声洞：",bg,(0,0,0)),(x+5,y+5))
        if _hsd == None:
            _hsd = [random.choice(hsd.hsd),random.choice(hsd.hsd),random.choice(hsd.hsd),random.choice(hsd.hsd)]
        else:
            screen.blit(hsd_text.render(_hsd[0],bg,(0,0,0)),(x+5,y+40+10))
            screen.blit(hsd_text.render(_hsd[1],bg,(0,0,0)),(x+5,y+40+30+10))
            screen.blit(hsd_text.render(_hsd[2],bg,(0,0,0)),(x+5,y+40+60+10))
            screen.blit(hsd_text.render(_hsd[3],bg,(0,0,0)),(x+5,y+40+90+10))
            screen.blit(hsd_thank,(x+5,y+40+90+30+10))
            y2 = y+40+90+10+5+30+30
            if not(y+y2 <= pos[1] <= y+y2+20):
                screen.blit(today_font.render("返回首页",bg,(0,0,0)),(x+5,y+y2))
                today_back = 0
            else:
                screen.blit(today_font.render("返回首页",bg,(255,0,0)),(x+5,y+y2))
                today_back = 1
            
    elif scr == 3:
        if fanyi_thread != None:
            if fanyi_thread.is_alive():
                screen.blit(wait.render("请在弹出的窗口中输入原文",bg,(0,0,0)),(x+5,y+5))
            else:
                screen.blit(fanyi_title.render("原文：",bg,(0,0,0)),(x+5,y+5))
                y2 = 30
                for i in fanyi_text.split("\n"):
                    screen.blit(fanyi_test.render(i,bg,(0,0,0)),(x+5,y+y2+5))
                    y2 += 25
                fanyi_text1 = fanyi_text
                for fan in fanyi.a:
                    fanyi_text1 = fanyi_text1.replace(fan[0],fan[1])
                screen.blit(fanyi_title.render("译文：",bg,(0,0,0)),(x+5,y+y2+5))
                y2 += 30
                for i in fanyi_text1.split("\n"):
                    screen.blit(fanyi_test.render(i,bg,(0,0,0)),(x+5,y+y2+5))
                    y2 += 25
                if not(y+y2 <= pos[1] <= y+y2+20):
                    screen.blit(today_font.render("返回首页",bg,(0,0,0)),(x+5,y+y2))
                    today_back = 0
                else:
                    screen.blit(today_font.render("返回首页",bg,(255,0,0)),(x+5,y+y2))
                    today_back = 1
        else:
            fanyi_thread = threading.Thread(target=fanyi_thread_target)
            fanyi_thread.start()
    elif scr == 5:
        y2 = 0
        about_text = [
            f"小邓の工具箱{__ver__}专业版",
            "Copyright (C) 2021  小邓学编程",
            "",
            "This program is free software: you can redistribute it and/or modify",
            "it under the terms of the GNU General Public License as published by",
            "the Free Software Foundation, either version 3 of the License, or",
            "(at your option) any later version.",
            "",
            "This program is distributed in the hope that it will be useful,",
            "but WITHOUT ANY WARRANTY; without even the implied warranty of",
            "MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the",
            "GNU General Public License for more details.",
            "",
            "You should have received a copy of the GNU General Public License",
            "along with this program.  If not, see <https://www.gnu.org/licenses"
        ]
        for i in about_text:
            screen.blit(about_test.render(i,bg,(0,0,0)),(x+5,y+y2+5))
            y2 += 20
        y2 += 10
        if not(y+y2 <= pos[1] <= y+y2+20):
            screen.blit(today_font.render("返回首页",bg,(0,0,0)),(x+5,y+y2))
            today_back = 0
        else:
            screen.blit(today_font.render("返回首页",bg,(255,0,0)),(x+5,y+y2))
            today_back = 1
    pygame.display.update()
    screen.fill(bg)
    
