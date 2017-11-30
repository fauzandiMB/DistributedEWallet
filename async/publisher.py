import pika
import logging
import time
import datetime

logging.basicConfig(level=logging.INFO)

# url = 'amqp://owiwtdks:179ts8ri0UgZYfi63pHo8Ux3JTbPbywD@spider.rmq.cloudamqp.com/owiwtdks'
url = 'amqp://sisdis:sisdis@172.17.0.3'

params = pika.URLParameters(url)
connection = pika.BlockingConnection(params)
channel = connection.channel()

channel.queue_declare(queue='EX_PING')

while True:
	ts = time.time()
	timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
	body = '{"action": "ping", "npm": "1406623266", "ts": "'+timestamp+'"}';
	channel.basic_publish(exchange='EX_PING', routing_key='', body='{"action": "ping", "npm": "1406623266", "ts": "'+timestamp+'"}')
	print(" [x] Published with body: " + body)
	time.sleep(5)


connection.close()