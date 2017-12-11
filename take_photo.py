import dropbox
import os
import urllib
import requests
import mraa
import time
import datetime
import json

deviceId = "DH0ipQDb"  
deviceKey = "h82HqT0FnRMwr1PU"
dataChnId = "display2"

pin = mraa.Gpio(44)
pin.dir(mraa.DIR_OUT)
pin.write(1)

url= "https://api.mediatek.com/mcs/v2/devices/DH0ipQDb/datachannels/display2/datapoints"
headers = {"Content-Type":"application/json","deviceKey":"h82HqT0FnRMwr1PU"}

a = requests.get(url, headers=headers).json()
print a

while True:
	r = requests.get(url, headers=headers).json()
	if(a==r):
		print "data is not update!!"
	else:
		x = json.loads(r['dataChannels'][0]['dataPoints'][0]['values']['value'])
		i = x['EventCode']
		c = 0
		print i
		a=r
		if(i==3 or i==1):
			# Take a picture
			command = 'fswebcam -i 0 -d v4l2:/dev/video0 --no-banner -p YUYV --jpeg 95 --save ./image.jpg'
			os.system(command)

			# Set Access Token
			access_token = 'F53u5Y_XRLAAAAAAAAAAD-0F5ltuRzNveV4qvXS1-pGbe9CbjuogSe47AmvFwOhb'
			dbx = dropbox.Dropbox(access_token )
			print 'linked account: ', dbx.users_get_current_account()

			# Upload Image to Dropbox
			with open('./image.jpg', 'rb') as f:
				response = dbx.files_upload(f.read(), '/Invalid_Image/image.jpg', mode=dropbox.files.WriteMode("overwrite"))
			print "uploaded:", response
			f.close()

			while(c<10):
				pin.write(1)
				time.sleep(0.1)
				pin.write(0)
				time.sleep(0.1)
				c = c+1