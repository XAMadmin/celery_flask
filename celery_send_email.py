from flask import Flask, request, render_template, session, redirect, flash, url_for
from celery import Celery
from flask_mail import Mail, Message

# import os
# os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1') # 加上这句话


app = Flask(__name__)

app.config["CELERY_BROKER_URL"] = "redis://localhost:6379/0"
app.config["CELERY_RESULT_BACKEND"] = "redis://localhost:6379/0" # secret_key

app.config["CELERY_TASK_SERIALIZER"] = 'pickle'

app.config["CELERY_RESULT_SERIALIZER"] = 'pickle'

app.config["CELERY_ACCEPT_CONTENT"] = ['pickle', 'json']



app.config["SECRET_KEY"] = "456qwqeqeqe"

# flask-mail发送邮件
# app.config['MAIL_DEBUG'] = True             # 开启debug，便于调试看信息
# app.config['MAIL_SUPPRESS_SEND'] = False    # 发送邮件，为True则不发送
# app.config['MAIL_SERVER'] = 'smtp.qq.com'   # 邮箱服务器
# app.config['MAIL_PORT'] = 465               # 端口
# app.config['MAIL_USE_SSL'] = True           # 重要，qq邮箱需要使用SSL
# app.config['MAIL_USE_TLS'] = False          # 不需要使用TLS
# app.config['MAIL_USERNAME'] = ''  # 填邮箱
# app.config['MAIL_PASSWORD'] = ''      # 填授权码     
# app.config['MAIL_DEFAULT_SENDER'] = '[]'  # 填邮箱，默认发送者
app.config.update(
    MAIL_DEBUG = True,
	MAIL_SERVER='smtp.qq.com',
	MAIL_PORT='465',
	MAIL_USE_SSL=True,
	MAIL_USERNAME='', # 填邮箱
	MAIL_PASSWORD=''  # 填授权码
	)

mail = Mail(app)


celery = Celery(app.name, broker=app.config["CELERY_BROKER_URL"])
celery.conf.update(app.config)


@celery.task
def send_async_email(msg):
    with app.app_context():
        mail.send(msg)


@app.route("/index1", methods=["GET", "POST"])
def index():

    if request.method == "GET":
        return render_template("index.html", email=session.get("email", ""))
    
    email = request.form.get("email")
    print(email)
    session["email"] = email

    if request.form.get("email") == "":
        flash("Sender cannot be empty !")
        return redirect(url_for('index'))


    # 发送信息
    msg = Message(
                    request.form.get("title", ""),
                    sender="", # 服务器邮箱
                    recipients=[request.form.get("email", "")]
                 )
     
    # msg.html = '<h1>hello world！</h1>'
    # msg.body = 'This is a test email sent from a background Celery task.'
    msg.html = request.form.get("centent", "")

    if request.form.get('submit') == "Send":
        result = send_async_email.delay(msg)
        print(result.ready())
        flash('Sending email to {0}'.format(email))
    else:
        send_async_email.apply_async(args=[msg], countdown=60)
        flash('An email will be sent to {0} in one minute'.format(email))

    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)


# 开启celery
# celery -A celery_send_email.celery  worker -l info -P eventlet