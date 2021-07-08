### celery-flask-redis邮件发

#### 1. flask-mail发送邮件

~~~python
# flask-mail发送邮件
# app.config['MAIL_DEBUG'] = True             # 开启debug，便于调试看信息
# app.config['MAIL_SUPPRESS_SEND'] = False    # 发送邮件，为True则不发送
# app.config['MAIL_SERVER'] = 'smtp.qq.com'   # 邮箱服务器
# app.config['MAIL_PORT'] = 465               # 端口
# app.config['MAIL_USE_SSL'] = True           # 重要，qq邮箱需要使用SSL
# app.config['MAIL_USE_TLS'] = False          # 不需要使用TLS
# app.config['MAIL_USERNAME'] = ''  # 填邮箱
# app.config['MAIL_PASSWORD'] = ''      # 填授权码     
# app.config['MAIL_DEFAULT_SENDER'] = '[2625187688@qq.com]'  # 填邮箱，默认发送者
~~~

#### 2.flask配置

~~~python
app = Flask(__name__)

app.config["CELERY_BROKER_URL"] = "redis://localhost:6379/0"
app.config["CELERY_RESULT_BACKEND"] = "redis://localhost:6379/0" # secret_key

app.config["CELERY_TASK_SERIALIZER"] = 'pickle'

app.config["CELERY_RESULT_SERIALIZER"] = 'pickle'

app.config["CELERY_ACCEPT_CONTENT"] = ['pickle', 'json']
~~~

#### 3.详细代码查看（celery_send_email.py）

#### 4. 运行celery

```python
# 开启celery
# celery -A celery_send_email.celery  worker -l info -P eventlet
```

#### 5.附件（利用python web框架做文件流下载 ， file_down.py）

