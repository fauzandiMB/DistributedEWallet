import pika
import logging
import sqlite3
import json

logging.basicConfig(level=logging.INFO)

# url = 'amqp://owiwtdks:179ts8ri0UgZYfi63pHo8Ux3JTbPbywD@spider.rmq.cloudamqp.com/owiwtdks'
url = 'amqp://sisdis:sisdis@172.17.0.3'

params = pika.URLParameters(url)

connection = pika.BlockingConnection(params)
channel = connection.channel()

channel.exchange_declare(exchange='EX_PING', exchange_type='fanout')

result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue

channel.queue_bind(exchange='EX_PING', queue=queue_name)

def callback(ch, method, properties, body):
	try:
		data = json.loads(body)

		if(data['action'] == 'ping'):
			conn = sqlite3.connect('tugas2.db')

			cursor = conn.execute('SELECT * FROM ping WHERE user_id = ' + data['npm'])

			account = cursor.fetchone()

			if(account is None):
				conn.execute('INSERT INTO ping (user_id, last_timestamp) VALUES (?, ?)', (data['npm'], data['ts']))
			else:
				conn.execute('UPDATE ping SET last_timestamp = ? WHERE user_id = ?', (data['ts'], data['npm']))

			conn.commit()
			conn.close()

		print(" [x] Format JSON valid %r" % body)
	except:
		print(" [x] Format JSON tidak valid %r" % body)

channel.basic_consume(callback, queue=queue_name, no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()