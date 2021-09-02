from flask import *
import serial
import time
import threading
import RPi.GPIO as GPIO

app = Flask(__name__)

bulb = False
motor = False
manual = True
manual_fan = True
web_mode = False

ser = serial.Serial('/dev/ttyS0', 9600)
ser.close()
ser.open()
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(13, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(11, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(15, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(16, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(19, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)

GPIO.output(21, GPIO.HIGH)
GPIO.output(22, GPIO.HIGH)
time.sleep(0.5)
GPIO.output(21, GPIO.LOW)
GPIO.output(22, GPIO.LOW)
time.sleep(0.5)
GPIO.output(21, GPIO.HIGH)
time.sleep(0.5)


def server():
	def init():
		GPIO.output(21, GPIO.HIGH)
		time.sleep(0.5)
		GPIO.output(21, GPIO.LOW)
		time.sleep(0.5)
		GPIO.output(21, GPIO.HIGH)
		time.sleep(0.5)
		ser.write(b"200")
		time.sleep(0.5)
	def check_status():
		global bulb
		global manual
		global motor
		global manual_fan
		#print(bulb)
		#print(manual)
		#print(motor)
		#print(manual_fan)
		if bulb == False and manual == True:
			ser.write(b"3")
			return "OFF"
		elif bulb == True and manual == True:
			ser.write(b"2")
			return "ON"
		else:
			return "Press the manual button again!!"
		#print(lights)
	def check_fan():
		global motor
		global manual_fan
		global manual
		#print(motor)
		#print(manual_fan)
		if motor == False and manual_fan == True:
			ser.write(b"4")
			return "OFF"
		elif motor == True and manual_fan == True:
			ser.write(b"5")
			return "ON"
		else:
			return "Press the manual button again!!"
	try:
		@app.route("/")
		def index():
			global web_mode
			global motor
			global bulb
			global manual
			global manual_fan
			motor = False
			manual = True
			bulb = False
			manual_fan = True
			if web_mode == False:
				return redirect("/web_disabled")
			else:
				init()
				return render_template("index.html", Lights = check_status(), Fan = check_fan(),auto_fan = "Manual",Auto_stat = "Manual", Auto_stat_all = "Manual")
		@app.route("/lights")
		def lights():
			global motor
			global bulb
			global manual
			global manual_fan
			global web_mode
			#print(web_mode)
			if web_mode == False:
				return redirect("/web_disabled")
			else:
				ser.write(b"7")
				if manual_fan == False:
					return redirect("/auto_fan_lights_manual")
				else:
					bulb = not bulb
					manual = True
					return render_template("index_lights.html", Lights = check_status(), Fan = check_fan(),auto_fan = "Manual",Auto_stat = "Manual", Auto_stat_all = "Manual")
		@app.route("/fan")
		def fan():
			global bulb
			global manual_fan
			global motor
			global manual
			global web_mode
			if web_mode == False:
				return redirect("/web_disabled")
			else:
				ser.write(b"8")
				if manual == False:
					return redirect("/auto_lights_fan_manual")
				else:
					motor = not motor
					manual_fan = True
					return render_template("index_fan.html", Lights = check_status(), Fan = check_fan(),auto_fan = "Manual",Auto_stat = "Manual", Auto_stat_all = "Manual")
		@app.route("/auto_lights")
		def auto_lights():
			global manual
			global bulb
			global motor
			global manual_fan
			global web_mode
			if web_mode == False:
				return redirect("/web_disabled")
			else:
				manual_fan = True
				ser.write(b"8")
				if manual == True:
					bulb = True
					print("Automated")
					manual = False
					ser.write(b"1")
					return render_template("auto_lights.html", Auto_stat = "Automatic", Fan = check_fan(), auto_fan = "Manual", Auto_stat_all = "Manual")
		@app.route("/auto_fan")
		def auto_fan():
			global manual_fan
			global manual
			global motor
			global bulb
			global web_mode
			if web_mode == False:
				return redirect("/web_disabled")
			else:
				manual = True
				ser.write(b"7")
				if manual_fan == True:
					motor = True
					manual_fan = False
					ser.write(b"6")
					motor = False
					return render_template("auto_fan.html", auto_fan = "Automatic", Lights = check_status(), Auto_stat = "Manual", Auto_stat_all = "Manual")
		@app.route("/auto_lights_fan_manual")
		def auto_lights_fan_manual():
			global web_mode
			if web_mode == False:
				return redirect("/web_disabled")
			else:
				ser.write(b"8")
				global motor
				motor = not motor
				return render_template("auto_lights_fan_manual.html", Auto_stat = "Automatic", Fan = check_fan(), auto_fan = "Manual", Auto_stat_all = "Manual")
		@app.route("/auto_fan_lights_manual")
		def auto_fan_lights_manual():
			global web_mode
			if web_mode == False:
				return redirect("/web_disabled")
			else:
				ser.write(b"7")
				global bulb
				bulb = not bulb
				return render_template("auto_fan_lights_manual.html", auto_fan = "Automatic", Lights = check_status(), Auto_stat = "Manual",Auto_stat_all = "Manual")
		@app.route("/all_auto")
		def all_auto():
			global web_mode
			if web_mode == False:
				return redirect("/web_disabled")
			else:
				ser.write(b"1000")
				all_auto = True
				return render_template("index_full_auto.html", Auto_stat_all = "Automatic")
		@app.route("/web_disabled")
		def web_disabled():
			global web_mode
			if web_mode == True:
				return redirect("/")
			else:
				return render_template("web_disabled.html")
	except exception as e:
		ser.close()

	app.run(host = '0.0.0.0', port = 8080)

def aux():
	global web_mode
	while True:
		if GPIO.input(12) == GPIO.HIGH:
			#print("Web OFF\r")
			web_mode = False
		else:
			#print("Web ON \r")
			GPIO.output(19, GPIO.LOW)
			GPIO.output(18, GPIO.LOW)
			web_mode = True
		if web_mode == False:
			GPIO.output(21, GPIO.LOW)
			if GPIO.input(13) == GPIO.HIGH:
				GPIO.output(19, GPIO.LOW)
			elif GPIO.input(11) == GPIO.HIGH:
				GPIO.output(19, GPIO.HIGH)
			elif GPIO.input(15) == GPIO.HIGH:
				GPIO.output(18, GPIO.HIGH)
			elif GPIO.input(16) == GPIO.HIGH:
				GPIO.output(18, GPIO.LOW)
		#else:
			#print("Nah!!!")


t1 = threading.Thread(target = server, args = ())
t2 = threading.Thread(target = aux, args = ())

t1.start()
t2.start()

try:
	t1.join()
except KeyboardInterrupt:
	GPIO.output(21, GPIO.LOW)
	print("\nPress ctrl + c again!")
