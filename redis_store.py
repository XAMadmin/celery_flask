import logging
from logging import handlers
import redis
from flask import Flask, jsonify
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
amount_limit = 100
rf_handler = handlers.TimedRotatingFileHandler('redis.log', when='midnight', interval=1, backupCount=7) # 'redis.log',
rf_handler.setFormatter(
    logging.Formatter(
        "%(asctime)s %(filename)s line:%(lineno)d [%(levelname)s] %(message)s")
)
logging.getLogger().setLevel(logging.INFO)
logging.getLogger().addHandler(rf_handler)


executor = ThreadPoolExecutor(4)
app = Flask(__name__)

pool = redis.ConnectionPool(host='127.0.0.1', port=6379, decode_responses=True)
r = redis.Redis(connection_pool=pool)

def limit_handle():
    
    time.sleep(0.5)
    keyname = 'limit'
    incr_amount = 1
    
    # if not r.exists(keyname):
    #     r.setnx(keyname, 0)
    # if r.incrby(keyname, incr_amount) <= amount_limit:

    #     print("剩余库存：{}".format( amount_limit - int(r.get(keyname))))
    #     return True
    # else:
    #     print("库存不足, 需要增加：{}".format(int(r.get(keyname)) - amount_limit))
    #     return False




@app.route("/limit")
def show():
    futures = [executor.submit(limit_handle)]

    for future in as_completed(futures):
        print(future.result())

        res = future.result()

        if res:
            data = 'success'
            logging.info("success")
        else:
            logging.info("failed")
            data = 'failed'

    return jsonify(errno='200', errmsg='limit', info=data)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)