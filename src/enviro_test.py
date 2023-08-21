# Test various sensors of Google Enviro Hat

import time
import board
from adafruit_bme280 import basic as adafruit_bme280
from opt3001 import opt3001
from HDC2010 import HDC2080


OPT_addr = 0x45
BME_addr = 0x76
HDC_addr = 0x40

i2c = board.I2C()  # uses board.SCL and board.SDA


try : 
	opt = opt3001.OPT3001(OPT_addr)
	opt.write_config_reg(opt3001.I2C_LS_CONFIG_CONT_FULL_800MS)


except :
	print('OPT3001 not found')
	opt = None

try :
	bme = adafruit_bme280.Adafruit_BME280_I2C(i2c, address = BME_addr)
	bme.sea_level_pressure = 1013.25
except:
	print('BME280 not found')
	bme = None

try :
	hdc = HDC2080(address=HDC_addr)
except:
	print('HDC 2010 not found')
	hdc= None

if not (hdc or bme or opt):
	exit('No sensors Found')

print('\nStarting Measurements\n')
while(True):
	light_str = ''
	bme_str1 = ''
	bme_str2 = ''
	hdc_str = ''
	if opt:
		light_str += 'Light : {:0.0f} Lux\n'.format(opt.read_lux_float())
	if hdc:
		hdc_str += 'HDC Temp : {0:3.1f} C. HDC Humidity : {1:3.1f} %\n'.\
			format(hdc.readTemperature(),hdc.readHumidity())
	if bme:  
		temp = bme.temperature
		rh = bme.relative_humidity
		P = bme.pressure
		alt = bme.altitude
		bme_str1 += 'BME Temp : {0:3.1f} C. BME Humidity : {1:3.1f} %\n'.format(temp,rh)
		bme_str2 += 'Pressure : {0:0.1f} hPa. Altitude {1:0.2f} m\n'.format(P,alt)



	display_str = light_str+bme_str1+bme_str2+hdc_str
	print(display_str)
	time.sleep(10)


