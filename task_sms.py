from os import name
from celery import Celery


# 大多数后台处理不需要返回结果，如果需要则必须配置 backend='redis://localhost'
app = Celery('background_task_celery', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0') 

@app.task(name="rub_jobs.tasktest")
def test():
    print('task...')
    return 'abc'


@app.task(name="rub_jobs.tasktest1")
def test1(a, b):
    print("task1")
    return  a + b


if __name__ == '__main__':

    test.delay() # 调用 test 任务
    # test.apply_async(countdown=10) # 10s后再次调用
    print('no result')    #    
    result = test1.delay(1, 2)
    print(result.get()) # 获取返回结果
    print('后台任务发送完毕，程序结束！')