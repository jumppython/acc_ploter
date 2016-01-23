#!/usr/bin/env python
#encoding=utf-8

import serial
import threading
import sys
import time
import Gnuplot

argv = sys.argv
argc = len(argv)

gp = Gnuplot.Gnuplot()

def mThread(ser):
	#	UARTの出力を読み込んで様々な処理を行う(実質メイン関数)
	gp( "set grid" )
	x = [0]*1024
	y = [0]*1024
	z = [0]*1024
	ntime = [0]*1024
	stime = time.time()

	while True:
		#	UARTを読み込んでリスト化(配列に代入)
		line = ser.readline()
		field = line.strip()
		sline = field.split(';')
		length = len(sline)

		#	加速度データが来たらグラフに出力
		if length == 16 and  sline[11] == "X":
			print field
			x[0] = float(sline[12])/100.0
			y[0] = float(sline[13])/100.0
			z[0] = float(sline[14])/100.0

			#	現時刻の計算
			ntime[0] = time.time()-stime

			#	グラフのパラメータ設定
			xd = Gnuplot.Data( ntime, x, with_="lines", title="X Axis")
			yd = Gnuplot.Data( ntime, y, with_="lines", title="Y Axis")
			zd = Gnuplot.Data( ntime, z, with_="lines", title="Z Axis")

			#	プロット
			gp.plot(xd,yd,zd, xrange="[%f:%f]" % ( ntime[128], ntime[0] ))

			#	配列の更新
			i=1022
			while i >= 0:
				x[i+1] = x[i]
				y[i+1] = y[i]
				z[i+1] = z[i]
				ntime[i+1] = ntime[i]
				i -= 1

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
	gp.close()
