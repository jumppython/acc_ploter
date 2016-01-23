#!/usr/bin/env python
#encoding=utf-8

import serial
import datetime
import oauth2 as oauth
import sys
import threading
import time
from urllib import urlencode

argv = sys.argv
argc = len(argv)

#	Twitter の開発者になって下記の4つのkeyを埋めてください
consumer_key="ここにConsumer Keyを記述する"
consumer_secret="ここにConsumer Secretを記述する"
access_token_key="ここにAccess Token Keyを記述する"
access_token_secret="ここにAccess Token Serectを記述する"

client  = oauth.Client(
	oauth.Consumer(key=consumer_key, secret=consumer_secret),
	oauth.Token(access_token_key, access_token_secret)
	)

#	UARTの出力を読み込んで様々な処理を行う(実質メイン関数)
def mThread(ser):
	while True:
		#	UARTを読み込んでリスト化(配列に代入)
		line = ser.readline()
		field = line.strip()
		sline = field.split(';')
		length = len(sline)

		#	加速度データであればこの中の処理
		if length == 16 and  sline[11] == "X":
			mode = int(sline[7])

			#	メッセージの作成
			#	Normal
			if mode == 0:
				x = float(sline[12])/100.0
				y = float(sline[13])/100.0
				z = float(sline[14])/100.0
				message = "X=%f Y=%f Z=%f" % ( x, y, z )
			#	Tap
			elif mode == 1:
#				message = "い、痛い///"
				message = "シングルタップ"
			#	Double Tap
			elif mode == 2:
#				message = "いてっ、いたいって..."
				message = "ダブルタップ"
			#	Free Fall
			elif mode == 4:
#				message = "お～ち～る～"
				message = "自由落下"
			#	Active
			elif mode == 8:
#				message = "だれも私をとめられない!!"
				message = "動いた"
			#	inactive
			elif mode == 10:
#				message = "動かざること山の如し"
				message = "動いていない"
			else :
				continue

			#	作成したメッセージに時間を付与
			ntime = datetime.datetime.today()
			strtime = ntime.strftime("%Y/%m/%d %H:%M:%S")
			message = strtime + " " + message
			unicode( message, "utf-8" )
			print message

			#	メッセージを投稿
			client.request(
				'https://api.twitter.com/1.1/statuses/update.json',
				'POST',
				urlencode({
				'status': message
				}),
			)

if __name__ == "__main__":
	#	引数がある場合、引数で指定したデバイスを用いる
	if argc != 2:
		ser = serial.Serial( "/dev/ttyUSB0", 115200, timeout=1 );
	else :
		ser = serial.Serial( argv[1], 115200, timeout=1 )

	#	グラフを描画する関数を別スレッドで実行
	t = threading.Thread( target=mThread, args=( ser, ) )
	t.setDaemon(True)
	t.start()

	#	q を入力すると終了
	while True:
		key = raw_input()
		if key == "q":
			break

	ser.close()
