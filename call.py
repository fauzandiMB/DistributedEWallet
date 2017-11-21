import sys
import requests
import json
import sqlite3
# from flask import Flask
# from flask import request
# from flask import jsonify
# from flask import Response

def check_ip():
	ip_ret = '127.0.0.1'

	list_ip = 'http://152.118.31.2/list.php'

	responseData = json.loads((requests.get(list_ip)).text)

	for ip in responseData:
		if (ip['npm']=='1406623266'):
			ip_ret = ip['ip']
			break

	return ip_ret

def ping(target_ip):
	url = 'http://' + target_ip + '/ewallet/ping'
	try:
		responseData = json.loads((requests.post(url, timeout=5)).text)
		pong = responseData['pong']

		if(pong==1):
			print('ping ke ' + target_ip +  ' berhasil')
		else:
			print('ping ' + target_ip +  ' gagal')
	except:
		print('ping ' + target_ip +  ' gagal')

def register(target_ip, user_id, nama):
	url = 'http://' + target_ip + '/ewallet/register'
	try:
		responseData = json.loads((requests.post(url, timeout=5, json={"user_id": user_id, "nama": nama})).text)
		status_register = responseData['status_register']
	
		if(status_register==1):
			print('Registrasi sukses')
		elif(status_register==-4):
			print('Registrasi gagal! Terdapat kesalahan di DB di host')
		elif(status_register==-99):
			print('Registrasi gagal! Terdapat kesalahan yang tidak terdefinisi di host')
		elif(status_register==-2):
			print('Registrasi gagal! Quorum belum terpenuhi')

		return status_register
	except:
		print('Registrasi gagal! tidak mendapatkan response')

		return -99

def getSaldo(target_ip, user_id):
	url = 'http://' + target_ip + '/ewallet/getSaldo'
	try:
		responseData = json.loads((requests.post(url, timeout=5, json={"user_id": user_id})).text)
		nilai_saldo = responseData['nilai_saldo']
		
		if(nilai_saldo==-1):
			print('getSaldo gagal! Akun belum terdaftar di host')

			conn = sqlite3.connect('ewallet.db')

			#Implement auto registasi here
			try:
				print('mencoba mencari user_id dalam DB')
				cursor = conn.execute('SELECT * FROM account WHERE user_id = ' + user_id)
				account = cursor.fetchone()
				conn.close()

				if(account is not None):
					print('Akun tidak ditemukan dalam DB')
				else:
					print('Akun ditemukan. Mencoba melakukan registrasi otomatis')
					
					nama = account[1]

					if(registasi(target_ip, user_id, nama)==1):
						print('Registrasi otomatis berhasil. mencoba kembali getSaldo')
						getSaldo(target_ip, user_id, nama)
			except:
				conn.close()
		elif(nilai_saldo==-4):
			print('getSaldo gagal! Terdapat kesalahan di DB di host')
		elif(nilai_saldo==-99):
			print('getSaldo gagal! Terdapat kesalahan yang tidak terdefinisi di host')
		elif(nilai_saldo==-2):
			print('getSaldo gagal! Quorum belum terpenuhi')
		else:
			print('getSaldo sukses! Nilai saldo: ' + str(nilai_saldo))

		return nilai_saldo
	except:
		print('getSaldo gagal! tidak mendapatkan response')

		return -99

def getTotalSaldo(target_ip, user_id):
	url = 'http://' + target_ip + '/ewallet/getTotalSaldo'
	try:
		responseData = json.loads((requests.post(url, timeout=100, json={"user_id": user_id})).text)
		nilai_saldo = responseData['nilai_saldo']
		
		if(nilai_saldo==-1):
			print('getTotalSaldo gagal! Akun belum terdaftar di host')

			conn = sqlite3.connect('ewallet.db')

			#Implement auto registasi here
			try:
				print('mencoba mencari user_id dalam DB')
				cursor = conn.execute('SELECT * FROM account WHERE user_id = ' + user_id)
				account = cursor.fetchone()
				conn.close()

				if(account is not None):
					print('Akun tidak ditemukan dalam DB')
				else:
					print('Akun ditemukan. Mencoba melakukan registrasi otomatis')
					
					nama = account[1]

					if(registasi(target_ip, user_id, nama)==1):
						print('Registrasi otomatis berhasil. mencoba kembali getTotalSaldo')
						getTotalSaldo(target_ip, user_id, nama)
			except:
				conn.close()	
		elif(nilai_saldo==-4):
			print('getTotalSaldo gagal! Terdapat kesalahan di DB di host')
		elif(nilai_saldo==-3):
			print('getTotalSaldo gagal! Tidak mendapatkan response dari host user tersebut')
		elif(nilai_saldo==-99):
			print('getTotalSaldo gagal! Terdapat kesalahan yang tidak terdefinisi di host')
		elif(nilai_saldo==-2):
			print('getTotalSaldo gagal! Quorum belum terpenuhi')
		else:
			print('getTotalSaldo sukses! Nilai saldo: ' + str(nilai_saldo))

		return nilai_saldo
	except:
		print('getTotalSaldo gagal! tidak mendapatkan response')

		return -99

def transfer(target_ip, user_id, nilai):
	url = 'http://' + target_ip + '/ewallet/transfer'
	try:
		responseData = json.loads((requests.post(url, timeout=5, json={"user_id": user_id, "nilai": nilai})).text)
		status_transfer = responseData['status_transfer']
		
		if(status_transfer==-1):
			print('transfer gagal! Akun belum terdaftar di host')

			conn = sqlite3.connect('ewallet.db')

			#Implement auto registasi here
			try:
				print('mencoba mencari user_id dalam DB')
				cursor = conn.execute('SELECT * FROM account WHERE user_id = ' + user_id)
				account = cursor.fetchone()
				conn.close()

				if(account is not None):
					print('Akun tidak ditemukan dalam DB')
				else:
					print('Akun ditemukan. Mencoba melakukan registrasi otomatis')
					
					nama = account[1]

					if(registasi(target_ip, user_id, nama)==1):
						print('Registrasi otomatis berhasil. mencoba kembali transfer')
						transfer(target_ip, user_id, nilai)
			except:
				conn.close()
		elif(status_transfer==-4):
			print('transfer gagal! Terdapat kesalahan di DB di host')
		elif(status_transfer==-99):
			print('transfer gagal! Terdapat kesalahan yang tidak terdefinisi di host')
		elif(status_transfer==-2):
			print('transfer gagal! Quorum belum terpenuhi')
		elif(status_transfer==-5):
			print('transfer gagal! Nilai transfer tidak valid')
		elif(status_transfer==1):
			print('transfer sukses!')
			#Implement kurangi saldo disini
			print('mengurangi saldo di DB')

			try:
				conn = sqlite3.connect('ewallet.db')
				cursor = conn.execute('SELECT * FROM account WHERE user_id = ' + '1406623266')
				account = cursor.fetchone()
				conn.close()

				conn = sqlite3.connect('ewallet.db')
				jumlah = int(account[2]) - int(nilai)
				cursor = conn.execute('UPDATE account SET saldo = ' + str(jumlah) + ' WHERE user_id = ' + '1406623266')
				conn.commit()
				conn.close()

				print('pengurangan saldo berhasil')
			except:
				print('pengurangan saldo gagal')
				conn.close()		
		return status_transfer
	except:
		print('transfer gagal! tidak mendapatkan response')

		return -99

args = sys.argv
my_ip = check_ip()

try:
	command = args[1]

	if(command=='ping'):
		try:
			target_ip = args[2]
			ping(target_ip)
		except:
			print('Format command salah! Contoh command ping:')
			print('python call.py ping 172.17.0.11')

	elif(command=='register'):
		try:
			target_ip = args[2]
			user_id = args[3]
			nama = ""

			for i in range(4, len(args)):
				nama += args[i]

			register(target_ip, user_id, nama)
		except:
			print('Format command salah! Contoh command register:')
			print('python call.py register 172.17.0.11 1406623266 Fauzandi Muhammad Baskara')

	elif(command=='getSaldo'):
		try:
			target_ip = args[2]
			user_id = args[3]

			getSaldo(target_ip, user_id)
		except:
			print('Format command salah! Contoh command getSaldo:')
			print('python call.py getSaldo 172.17.0.11 1406623266')
		
	elif(command=='getTotalSaldo'):
		try:
			target_ip = args[2]
			user_id = args[3]

			getTotalSaldo(target_ip, user_id)
		except:
			print('Format command salah! Contoh command getTotalSaldo:')
			print('python call.py getTotalSaldo 172.17.0.11 1406623266')

	elif(command=='transfer'):
		try:
			target_ip = args[2]
			user_id = args[3]
			nilai = args[4]

			transfer(target_ip, user_id, nilai)
		except:
			print('Format command salah! Contoh command transfer:')
			print('python call.py transfer 172.17.0.11 1406623266 800000')

	else:
		print('Format command salah! Berikut merupakan format command:')
		print('Untuk ping: python call.py ping [target_ip]')
		print('Untuk register: python call.py register [target_ip] [user_id] [nama]')
		print('Untuk getSaldo: python call.py getSaldo [target_ip] [user_id]')
		print('Untuk getTotalSaldo: python call.py getTotalSaldo [target_ip] [user_id]')
		print('Untuk transfer: python call.py trasfer [target_ip] [user_id] [nilai]')
except:
	print('Format command salah! Berikut merupakan format command:')
	print('Untuk ping: python call.py ping [target_ip]')
	print('Untuk register: python call.py register [target_ip] [user_id] [nama]')
	print('Untuk getSaldo: python call.py getSaldo [target_ip] [user_id]')
	print('Untuk getTotalSaldo: python call.py getTotalSaldo [target_ip] [user_id]')
	print('Untuk transfer: python call.py trasfer [target_ip] [user_id] [nilai]')