from flask import Flask
from flask import request
from flask import jsonify
from flask import Response
import requests
import json
import socket

import sqlite3

conn = sqlite3.connect('ewallet.db')

app = Flask(__name__)

def checkQuorum():
	return 100
	
	check_quorum_url = 'http://152.118.31.2/list.php'

	responseData = json.loads((requests.get(check_quorum_url)).text)

	jumlahHidup = 0
	jumlahMati = 0

	for element in responseData:
		try:

			ping_url = 'http://' + element['ip'] + '/ewallet/ping'

			responseData = json.loads((requests.post(ping_url, timeout=1)).text)['pong']
			
			if(responseData==1):
				# statusList.append('hidup')
				jumlahHidup+=1
			else:
				# statusList.append('mati')
				jumlahMati+=1
		except:
			# statusList.append('mati')
			jumlahMati+=1
			continue

	return float(jumlahHidup)*100/(jumlahHidup+jumlahMati)
	
@app.route("/ewallet/ping", methods=["POST"])
def ping():
	try:
		responseData = {'pong': 1}
		return jsonify(responseData)
	except:
		responseData = {'pong': -99}
		return jsonify(responseData)
	
@app.route("/ewallet/register", methods=["POST"])
def register():
	quorumVal = checkQuorum()

	if(quorumVal>=50):
		try:
			requestParam = json.loads(request.data)

			conn = sqlite3.connect('ewallet.db')

			user_id = requestParam['user_id']

			nama = requestParam['nama']
				
			try:
				conn.execute('INSERT INTO account (user_id, nama, saldo) VALUES("' + user_id + '", "' + nama +'", 0)')
				conn.commit()
				conn.close()
				return jsonify({'status_register': 1});
			except:
				conn.close()
				return jsonify({'status_register': -4});
		except:
			return jsonify({'status_register': -99});
	else:
		return jsonify({'status_register': -2});

@app.route("/ewallet/getSaldo", methods=["POST"])
def getSaldo():
	quorumVal = checkQuorum()

	if(quorumVal>=50):
		try:
			requestParam = json.loads(request.data)

			conn = sqlite3.connect('ewallet.db')

			user_id = requestParam['user_id']
				
			try:
				cursor = conn.execute('SELECT * FROM account WHERE user_id = ' + user_id)

				account = cursor.fetchone()
				conn.close()

				if(account is None):
					return jsonify({'nilai_saldo': -1});
				else:
					return jsonify({'nilai_saldo': account[2]});
			except:
				conn.close()
				return jsonify({'nilai_saldo': -4});
		except:
			return jsonify({'nilai_saldo': -99});
	else:
		return jsonify({'nilai_saldo': -2});
	
@app.route("/ewallet/transfer", methods=["POST"])
def transfer():
	quorumVal = checkQuorum()

	if(quorumVal>=50):
		try:
			requestParam = json.loads(request.data)

			conn = sqlite3.connect('ewallet.db')

			user_id = requestParam['user_id']

			nilai = int(requestParam['nilai'])

			try:
				cursor = conn.execute('SELECT * FROM account WHERE user_id = ' + user_id)

				account = cursor.fetchone()
				conn.close()

				if(account is None):
					return jsonify({'status_transfer': -1});
				else:
					if(nilai<0 or nilai>1000000000):
						return jsonify({'status_transfer': -5});
					else:
						#Implement transfer here
						conn = sqlite3.connect('ewallet.db')
						jumlah = int(account[2]) + nilai
						cursor = conn.execute('UPDATE account SET saldo = ' + str(jumlah) + ' WHERE user_id = ' + user_id)
						conn.commit()
						conn.close()

						return jsonify({'status_transfer': 1});
			except:
				conn.close()
				return jsonify({'status_transfer': -4});
		except:
			return jsonify({'status_transfer': -99});
	else:
		return jsonify({'status_transfer': -2});

@app.route("/ewallet/getTotalSaldo", methods=["POST"])
def getTotalSaldo():
	quorumVal = checkQuorum()
	
	if(quorumVal>=100):
		try:
			requestParam = json.loads(request.data)

			conn = sqlite3.connect('ewallet.db')

			user_id = requestParam['user_id']
			
			try:
				cursor = conn.execute('SELECT * FROM account WHERE user_id = ' + user_id)

				account = cursor.fetchone()
				conn.close()

				if(account is None):
					return jsonify({'nilai_saldo': -1});
				else:
					#Implement Get Total Saldo here

					#Jika akun kita sendiri:
					if(user_id=='1406623266') :
						list_ip_url = 'http://152.118.31.2/list.php'

						list_ip = json.loads((requests.get(list_ip_url)).text)

						totalSaldo = 0

						for ip in list_ip:
							try:
								url = 'http://' + ip['ip'] + '/ewallet/getSaldo'

								responseData = json.loads((requests.post(url, timeout=5, json={'user_id' : user_id})).text)['nilai_saldo']

								if(responseData!=-1 and responseData!=-4 and responseData!=-99 and responseData!=-2):
									totalSaldo += responseData
							except:
								continue

						return jsonify({'nilai_saldo': totalSaldo});
					#Jika akun orang lain
					else:
						try:
							url = 'http://' + user_id + '/ewallet/getTotalSaldo'
							responseData = json.loads((requests.post(url, timeout=100)).text)['nilai_saldo']
							
							return jsonify({'nilai_saldo': responseData});
						except:
							return jsonify({'nilai_saldo': -3});
			except:
				conn.close()
				return jsonify({'nilai_saldo': -4});
		except:
			return jsonify({'nilai_saldo': -99});
	else:
		return jsonify({'nilai_saldo': -2});

@app.errorhandler(404)
def not_found(e):	
	return Response('{"detail": "The requested URL was not found on the server.  If you entered the URL manually please check your spelling and try again.", "status": "404", "title": "Not Found"}', status=404, mimetype='application/json')
	
if __name__ == "__main__":
	app.run(host="0.0.0.0", port=80, debug=True, threaded=True)
