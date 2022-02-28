from apscheduler.schedulers.background import BackgroundScheduler
import time
def function():
    print("定时任务跑起来了")

# 定义后台执行调度器
scheduler = BackgroundScheduler()
# 添加任务，间隔5s执行一次func()函数。  看不懂没关系后面会介绍
scheduler.add_job(func=function, trigger="interval", seconds=5)
# 启动定时器
scheduler.start()
# 使主程序不关闭
while True:
    print(time.sleep(9999))