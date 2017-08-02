import redis
import time
r = redis.StrictRedis(host='localhost',port=6379, db=0)
r.set('name','ranjeet')
print(r.get('name'))
p = r.pubsub()
p.subscribe('zclient')
while True:
    message = p.get_message()
    if message:
        # do something with the message
        print(message)
        time.sleep(0.001)  
