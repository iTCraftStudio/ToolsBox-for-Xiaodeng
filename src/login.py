from easygui import *
from log import log
__ver__ = 1.1
def enctry(s):
    k = 'djq%5cu#-jeq15abg$z9_i#_w=$o88m!*alpbedlbat8cr74sd'
    encry_str = ""
    for i,j in zip(s,k):
    # i为字符，j为秘钥字符
        temp = str(ord(i)+ord(j))+'_' # 加密字符 = 字符的Unicode码 + 秘钥的Unicode码
        encry_str = encry_str + temp
    return encry_str
# 解密
def dectry(p):
    k = 'djq%5cu#-jeq15abg$z9_i#_w=$o88m!*alpbedlbat8cr74sd'
    dec_str = ""
    for i,j in zip(p.split("_")[:-1],k):
      # i 为加密字符，j为秘钥字符
        temp = chr(int(i) - ord(j)) # 解密字符 = (加密Unicode码字符 - 秘钥字符的Unicode码)的单字节字符
        dec_str = dec_str+temp
    return dec_str
def login():
    log(f"登录函数启动",f="[login]")
    mode = choicebox("用户您好，为了让您有更好的使用体验，请 注册/登录 ！",
          "登录/注册 ToolsBox-ID",
          ("我有账号，立即登录！","我没有账号，注册一个！"))
    log(f"用户选择了：{mode}",f="[login]")
    if mode == "我有账号，立即登录！":
        user = multpasswordbox("Login by user ID!",
                        "登录 ToolsBox-ID",
                        ("User ID","Password"))
        if user != None:
            u = dectry(user[0]).split("|")
            if u[1] != user[1]:
                msgbox("密码错误!","登陆失败",ok_button = "Exit")
                return 1
            with open("./config/user.json","w") as f:
                f.write('{"uid":"'+user[0]+'"}')
            return 0
    elif mode == "我没有账号，注册一个！":
        user = multpasswordbox("注册 IoolsBox-ID!",
                               "注册",
                               ("用户名","密码"))
        if user != None:
            if user[1] == passwordbox("重复您的密码",
                                      "重复密码"):
                uid = enctry(f"{user[0]}|{user[1]}")
                msgbox(f"""用户名：{user[0]}
密码：{user[1]}
User ID：{uid}""","注册成功！",ok_button = "返回")
                return login()
            else:
                msgbox("密码错误","Err",ok_button = "EXIT")
                return 1
        else:
            return 1
    else:
        return 1