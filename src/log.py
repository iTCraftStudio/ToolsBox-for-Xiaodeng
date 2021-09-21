import time

__ver__ = 1.0
def log(log,lv="[INFO]",f = "[main]"):
    now = time.localtime(time.time())
    now_time = f"[{str(now[3])}:{str(now[4])}:{str(now[5])}]"
    print(f'{now_time}{f}{lv} {log}')