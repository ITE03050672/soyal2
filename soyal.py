import socket
import struct
import binascii
import datetime
import httplib, urllib
import requests
import json
import time

#SOYAL_MAX_DATA
SOYAL_MAX_DATA_STD = 244
SOYAL_MAX_DATA_TCP = 1400

#SOYAL_HEADER
SOYAL_HEADER_STANDARD = 0x7E
SOYAL_HEADER_EXTENDED = 0xFF005AA5

SOYAL_DEFAULT_DEST = 0x00
SOYAL_DEST_BROADCAST = 0xFF
SOYAL_ORIGINAL_XOR = 0xFF
SOYAL_DEFAULT_PORT = 1621

#SOYAL_PACKET
SOYAL_PACKET_STANDARD = 0
SOYAL_PACKET_EXTENDED_TCP = 2


SOYAL_ECHO_DATA = 0x03
SOYAL_CMD_ACK = 0X04
SOYAL_CMD_NACK = 0x05
SOYAL_AUTHERR = 0x06
SOYAL_NOTAG = 0x07
SOYAL_NOT_LOGIN = 0x08
SOYAL_CRC_ERR = 0x09
SOYAL_NOT_AUTH = 0x0A
SOYAL_AUTH_REJECT = 0x0B

SOYAL_GET_PARAMETERS = 0x12
SOYAL_SET_PARAMETERS = 0x20

SOYAL_PARAMETER_SUB_OPTION = 0x00
SOYAL_PARAMETER_SUB_AUTOOPEN_TIME = 0x01
SOYAL_PARAMETER_SUB_DAILY_ALARM = 0x02
SOYAL_PARAMETER_SUB_AUTO_DUTY_SHIFT = 0x03
SOYAL_PARAMETER_SUB_MASTER_CARD_UID = 0x04
SOYAL_PARAMETER_SUB_RS485_DOOR_NUM = 0x05
SOYAL_PARAMETER_SUB_CUSTOM_DEFINE = 0x06
SOYAL_PARAMETER_SUB_UID_BLOCK = 0x08
SOYAL_PARAMETER_SUB_TCP_ADDR_PORT = 0x0A
SOYAL_PARAMETER_SUB_8SETS_DUTY = 0x0B
SOYAL_PARAMETER_SUB_DESFIRE = 0x12
SOYAL_PARAMETER_SUB_RS485_STATUS = 0x81

SOYAL_RELAY_CTRL = 0x21
SOYAL_SET_RTC = 0x23
SOYAL_GET_RTC = 0x24

SOYAL_GET_OLDEST_EVENTLOG = 0x25
SOYAL_REMOVE_OLDEST_EVENTLOG = 0x37
SOYAL_EMPTY_EVENTLOG = 0x2D
SOYAL_BUZZER_SOUND = 0x26

SOYAL_SEND_LCD_TEXT = 0x28

SOYAL_DAILY_TIME_ZONE = 0x2A

SOYAL_RW_BEGIN_DAY = 0x2B

SOYAL_SET_ANNUAL_HOLIDAY = 0x2C

SOYAL_RW_USER_ALIAS = 0x2E
SOYAL_RW_USER_FLOOR = 0x2F

SOYAL_SERIAL_FORMAT = 0x30
SOYAL_SET_USER_PARM1 = 0x83
SOYAL_SET_USER_PARM2 = 0x84
SOYAL_ERASE_USER_DATA = 0x85

SOYAL_GET_USER_PARM = 0x87
SOYAL_INIT_ANTI_PASSBACK = 0x8A

EventCode_Dict = {
	0 : "SOYAL_CODE_ERR",
	1 : "SOYAL_INVALID_PIN",
	2 : "SOYAL_KEY_LOCKED_OVER_LIMIT",
	3 : "SOYAL_INVALID_CARD",
	4 : "SOYAL_TIMEZONE_ERR",
	5 : "SOYAL_DOOR_GROUP_ERR",
	6 : "SOYAL_EXPIRY_DATE",
	7 : "SOYAL_OVER_ACCESS_TIME",
	8 : "SOYAL_PIN_ERR",
	9 : "SOYAL_PRESS_DURESS_PB",
	10 : "SOYAL_ACCESS_BY_CARD_AND_PIN",
	11 : "SOYAL_NORMAL_ACCESS_BY_TAG",
	12 : "SOYAL_FORCE_CTRL_RELAY_ON",
	13 : "SOYAL_FORCE_CTRL_RELAY_OFF",
	14 : "SOYAL_CTRL_ARMED",
	15 : "SOYAL_CTRL_DISARMED",
	16 : "SOYAL_EGRESS",
	18 : "SOYAL_ALARM_EVENT",
	20 : "SOYAL_CTRL_PWROFF",
	21 : "SOYAL_DURESS",
	22 : "SOYAL_GUARDS_HELP",
	23 : "SOYAL_CLEANER_ACCESS",
	24 : "SOYAL_CTRL_PWRON",
	25 : "SOYAL_FORCE_CTRL_RELAY_ERR",
	26 : "SOYAL_RDR_RTN",
	27 : "SOYAL_PUSH_BTN",
	28 : "SOYAL_ACCESS_BY_PIN",
	29 : "SOYAL_DIGITAL_INPUT_ACTIVE",
	31 : "SOYAL_RS485_READER_OFF",
	32 : "SOYAL_RS485_READER_ON",
	33 : "SOYAL_USER_PIN_CHANGE",
	34 : "SOYAL_CHANGE_USER_PIN_ERR",
	35 : "SOYAL_ENTR_AUTO_DOOR_OPEN",
	36 : "SOYAL_EXIT_AUTO_DOOR_OPEN",
	37 : "SOYAL_AUTO_DISARMED",
	38 : "SOYAL_AUTO_ARMED",
	42 : "SOYAL_REMOTE_CTRL_UP",
	43 : "SOYAL_DISABLE_READER",
	44 : "SOYAL_ENABLE_READER",
	45 : "SOYAL_REMOTE_PANIC",
	46 : "SOYAL_USER_ENTRACE_PARKING",
	47 : "SOYAL_USER_EXIT_PARKING",
	48 : "SOYAL_COUNTER_TRIG",
	49 : "SOYAL_LATCH_RELAY",
	50 : "SOYAL_ENTER_EXIT_EDIT",
	55 : "SOYAL_FREE_ACCESS",
	59 : "SOYAL_INHIBIT_CARD_OPEN",
	60 : "SOYAL_NEVER_OPEN",
	62 : "SOYAL_CANNT_READ_DATE_MIFARE",
	63 : "SOYAL_CANNT_READ_CMD_MIFARE",
	64 : "SOYAL_CANNT_DEDUCT_MIFARE",
	65 : "SOYAL_SOR_GLOBAL_CARD_ACCESS",
	66 : "SOYAL_SOR_LAYER_ERR",
	67 : "SOYAL_REJECT_BEFORE_DATE",
	68 : "SOYAL_REJECT_EXPIRY",
	69 : "SOYAL_REJECT_LESS_CARD_VALUE",
	70 : "SOYAL_ACCESS_OK",
	71 : "SOYAL_ACCESS_OK_READ_FAILED",
	72 : "SOYAL_SOR_ACCESS_OK",
	73 : "SOYAL_ACCESS_REJECT_LESS_VALUE",
	74 : "SOYAL_ACCESS_OK_VALUE_FAILED",
	75 : "SOYAL_ACCESS_OK_WITHOUT_DEDUCTED",
	86 : "SOYAL_BLACK_TBL",
	100 : "SOYAL_ACCESS_OK_VIA_VEIN",
	101 : "SOYAL_ACCESS_REJECT",
	102 : "SOYAL_DOOR_LOCK",
	104 : "SOYAL_FIRE_ALARM"}

class Soyal_User:
	Records = None
	Addr = None
	TagHi = None
	TagLo = None
	Pin = None
	Mode = None
	Door1 = None
	Door2 = None
	Year = None
	Month = None
	Day = None
	Level = None
	Zone = None
	Option = None
	get_data = None

class MCS_Data:
	Soyal_Data = None

class Soyal_Event:
	EventCode = None
	SourceNodeId = None
	Year = None
	Month = None
	Day = None
	Hour = None
	Minute = None
	Second = None
	Address = None
	Door = None
	Level = None
	TagHi = None
	TagLo = None
	Timestamp = None

class Soyal_Clock:
	RID = None
	Year = None
	Month = None
	Weekday = None
	Day = None
	Hour = None
	Minute = None
	Second = None

class Soyal:
	def __init__(self, ip, port, node):
		self.address = (ip,port)
		self.node = node
		
		self.user = Soyal_User
		self.event_log = Soyal_Event
		self.clock = Soyal_Clock
		self.mcs = MCS_Data

#		self.packet = None
#		self.packet_data = None
		
	def connect(self):
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		result = self.s.connect_ex(self.address)
		if result:
			print "CONNECT ERROR!"
			print str(result)
			return -1
		else:
			return 0
	
	def disconnect(self):
		self.s.close()

	def __read_packet(self):
		self.rp = self.s.recv(SOYAL_MAX_DATA_TCP)
		return self.rp
	
	def get_mcs(self, id, key, chnid):
		deviceId = id
		deviceKey = key
		dataChnId = chnid
		
		url = "https://api.mediatek.com/mcs/v2/devices/" + deviceId + "/datachannels/" + dataChnId + "/datapoints"
		
		headers = {"Content-Type":"application/json","deviceKey":deviceKey}
	
		r = requests.get(url, headers=headers).json()
			
		if r['code'] == 200:
			self.mcs.Soyal_Data = json.loads(r['dataChannels'][0]['dataPoints'][0]['values']['value'])		
#			print self.mcs_user.Soyal_Data
			return self.mcs.Soyal_Data
		else:
			print "ERROR"
			return -1

#	GET_EVENT LOG
	def get_oldest_eventlog(self):
		length = 0x04
		xor = (SOYAL_ORIGINAL_XOR ^ self.node ^ SOYAL_GET_OLDEST_EVENTLOG) % 256
		sum1 = (self.node + SOYAL_GET_OLDEST_EVENTLOG + xor)% 256
		
		buffer1 = struct.pack('BBBBBB',SOYAL_HEADER_STANDARD,length,self.node,SOYAL_GET_OLDEST_EVENTLOG,xor,sum1)

		send_data = self.s.send(buffer1)
		recv_data = self.__read_packet()
		
		header = struct.unpack('B', str(recv_data)[0:1])[0]
		len1 = struct.unpack('B', str(recv_data)[1:2])[0]
		cmd = struct.unpack('B', str(self.rp)[3:4])[0]

		if header == SOYAL_HEADER_STANDARD:
			if len1 == 0x21:
	#			print "...SUCCESS"
	#			What is event ?
				self.event_log.EventCode = struct.unpack('B', str(recv_data)[3:4])[0]
				self.event_log.SourceNodeId = struct.unpack('B', str(recv_data)[4:5])[0]
	#			Event time
				self.event_log.Second = struct.unpack('B', str(recv_data)[5:6])[0]
				self.event_log.Minute = struct.unpack('B', str(recv_data)[6:7])[0]
				self.event_log.Hour = struct.unpack('B', str(recv_data)[7:8])[0]
				self.event_log.Day = struct.unpack('B', str(recv_data)[9:10])[0]
				self.event_log.Month = struct.unpack('B', str(recv_data)[10:11])[0]
				self.event_log.Year = struct.unpack('B', str(recv_data)[11:12])[0] + 2000
				
				t = datetime.datetime(self.event_log.Year, self.event_log.Month, self.event_log.Day, self.event_log.Hour, self.event_log.Minute, self.event_log.Second)
	#			Timestamp is minisecond for MCS
				self.event_log.Timestamp = time.mktime(t.timetuple()) * 1000

	#			Event User data
				self.event_log.Address = struct.unpack('B', str(recv_data)[13:14])[0] * 256 + struct.unpack('B', str(recv_data)[14:15])[0]
				self.event_log.Level = struct.unpack('B', str(recv_data)[18:19])[0]
				self.event_log.TagHi = struct.unpack('B', str(recv_data)[19:20])[0] * 256 + struct.unpack('B', str(recv_data)[20:21])[0]
				self.event_log.Door = struct.unpack('B', str(recv_data)[21:22])[0]
				self.event_log.TagLo = struct.unpack('B', str(recv_data)[23:24])[0] * 256 + struct.unpack('B', str(recv_data)[24:25])[0]
				return 0
			elif len1 == 0x0d:
#				Eventlog is empty, check if it's ACK or not
				if cmd == SOYAL_CMD_ACK:
					print "Eventlog is empty"
					return 1
			else:
				print "...ERROR"
				return -1

	def remove_oldest_eventlog(self):
		length = 0x04
		xor = (SOYAL_ORIGINAL_XOR ^ self.node ^ SOYAL_REMOVE_OLDEST_EVENTLOG) % 256
		sum1 = (self.node + SOYAL_REMOVE_OLDEST_EVENTLOG + xor)% 256
		
		buffer1 = struct.pack('BBBBBB',SOYAL_HEADER_STANDARD,length,self.node,SOYAL_REMOVE_OLDEST_EVENTLOG,xor,sum1)
		
		send_data = self.s.send(buffer1)
		recv_data = self.__read_packet()
		
		cmd = struct.unpack('B', str(recv_data)[3:4])[0]
		if cmd == SOYAL_CMD_ACK:
#			print "...SUCCESS"
			return 0
		elif cmd == SOYAL_CMD_NACK:
#			print "Eventlog is empty"
			return 1
		else :
			print "...Error"
			return -1

	def empty_eventlog(self):
		length = 0x04
		xor = (SOYAL_ORIGINAL_XOR ^ self.node ^ SOYAL_EMPTY_EVENTLOG) % 256
		sum1 = (self.node + SOYAL_EMPTY_EVENTLOG + xor)% 256
		
		buffer1 = struct.pack('BBBBBB',SOYAL_HEADER_STANDARD,length,self.node,SOYAL_EMPTY_EVENTLOG,xor,sum1)
		
		send_data = self.s.send(buffer1)
		recv_data = self.__read_packet()
		
		cmd = struct.unpack('B', str(recv_data[0])[3:4])[0]

		if cmd == SOYAL_CMD_ACK:
			print "...SUCCESS"
			return 0
		elif cmd == SOYAL_CMD_NACK:
			print "Eventlog is empty"
			return 1
		else :
			print "...Error"
			return -1
# SOYAL CLOCK

	def get_clock(self):
		length = 0x04
		xor = (SOYAL_ORIGINAL_XOR ^ self.node ^ SOYAL_GET_RTC) % 256
		sum1 = (self.node + SOYAL_GET_RTC + xor)% 256
		
		buffer1 = struct.pack('BBBBBB',SOYAL_HEADER_STANDARD,length,self.node,SOYAL_GET_RTC,xor,sum1)
		
		send_data = self.s.send(buffer1)
		recv_data = self.__read_packet()
		
		cmd = struct.unpack('B', str(recv_data)[3:4])[0]

		if cmd == 0x03:
#			print "...SUCCESS"
				
			self.clock.RID = struct.unpack('B', str(recv_data)[4:5])[0]
			self.clock.Second = struct.unpack('B', str(recv_data)[5:6])[0]
			self.clock.Minute = struct.unpack('B', str(recv_data)[6:7])[0]
			self.clock.Hour = struct.unpack('B', str(recv_data)[7:8])[0]
			self.clock.Weekday = struct.unpack('B', str(recv_data)[8:9])[0]
			self.clock.Day = struct.unpack('B', str(recv_data)[9:10])[0]
			self.clock.Month = struct.unpack('B', str(recv_data)[10:11])[0]
			self.clock.Year = struct.unpack('B', str(recv_data)[11:12])[0] + 2000

			return 0
		else:
			print "...ERROR"
			return -1
	
	def set_clock(self):
		dt = datetime.datetime.now()

		week_day_dict = {
		    1 : 2,
			2 : 3,
			3 : 4,
			4 : 5,
			5 : 6,
			6 : 7,
			7 : 1,
		}

		length = 0x0B
		
		second = dt.second
		minute = dt.minute
		hour = dt.hour
		week = week_day_dict[dt.isoweekday()]
		day = dt.day
		month = dt.month
		year = dt.year % 100
		
		xor = (SOYAL_ORIGINAL_XOR ^ self.node ^ SOYAL_SET_RTC ^ second ^ minute ^ hour ^ week ^ day ^ month ^ year) % 256
		sum1 = (self.node + SOYAL_SET_RTC + second + minute + hour + week + day + month + year + xor)% 256
		
		print dt

		buffer1 = struct.pack('BBBBBBBBBBBBB',SOYAL_HEADER_STANDARD,length,self.node,SOYAL_SET_RTC,second,minute,hour,week,day,month,year,xor,sum1)
		
		send_data = self.s.send(buffer1)
		recv_data = self.__read_packet()
		
		cmd = struct.unpack('B', str(recv_data)[3:4])[0]
		
		if cmd == SOYAL_CMD_ACK:
#			print "...SUCCESS"
			return 0
		else:
			print "...ERROR"
			return -1

	def __write_soyal_user(self):
		self.user.Records = self.mcs.Soyal_Data['Records']
		self.user.Addr = self.mcs.Soyal_Data['Addr']
		self.user.TagHi = self.mcs.Soyal_Data['TagHi']
		self.user.TagLo = self.mcs.Soyal_Data['TagLo']
		self.user.Pin = self.mcs.Soyal_Data['Pin']
		self.user.Mode = self.mcs.Soyal_Data['Mode']
		self.user.Door1 = self.mcs.Soyal_Data['Door1']
		self.user.Door2 = self.mcs.Soyal_Data['Door2']
		self.user.Year = self.mcs.Soyal_Data['Year']
		self.user.Month = self.mcs.Soyal_Data['Month']
		self.user.Day = self.mcs.Soyal_Data['Day']
		self.user.Level = self.mcs.Soyal_Data['Level']
		self.user.Zone = self.mcs.Soyal_Data['Zone']
		self.user.Option = self.mcs.Soyal_Data['Option']

	def set_user(self):
		self.__write_soyal_user()

		Records = struct.pack('B', self.user.Records)
		
		Addr = struct.pack('!H', self.user.Addr)												#Two bytes of address
		
		Tag = struct.pack('!4BHH', 0, 0, 0, 0, self.user.TagHi, self.user.TagLo,)		#Eight byte of Tag ID
																									#The upper 4 bytes = 0
		Pin = struct.pack('!I', self.user.Pin)												#4 Bytes of PIN Code
		
		payload = Records + Addr + Tag + Pin + struct.pack('12B', self.user.Mode,			#Access Mode
																  self.user.Zone,			#User Access Zone
																  self.user.Door1,			#Group 1
																  self.user.Door2,			#Group 2
																  self.user.Year-2000,		#Last Allowed Date
																  self.user.Month,
																  self.user.Day,
																  self.user.Level,			#User Level, Level 3 -> 192, Level 3 -> 192(11000000), Level 2 -> 128(10000000), Level 1 -> 64(01000000)
																  self.user.Option,			#Option
																  0,0,0								#Reserved 3 bytes
																  )
		length = len(payload) + 4
		
		data = struct.unpack('27B',payload)
		
		raw_xor = SOYAL_ORIGINAL_XOR ^ self.node ^ SOYAL_SET_USER_PARM1
		
		raw_sum1 = self.node + SOYAL_SET_USER_PARM1
		
		for i in range(0,len(payload),1):
			raw_xor = raw_xor ^ data[i]
			raw_sum1 = raw_sum1 + data[i]
			
		xor = raw_xor % 256
		sum1 = (raw_sum1 + xor) % 256
		
		buffer1 = struct.pack('BBBB', SOYAL_HEADER_STANDARD, length, self.node, SOYAL_SET_USER_PARM1) + payload + struct.pack('BB',xor,sum1)
		
		send_data = self.s.send(buffer1)
		recv_data = self.__read_packet()
		
		cmd = struct.unpack('B', str(recv_data)[3:4])[0]

		if cmd == SOYAL_CMD_ACK:
			print "...SUCCESS"
			return 0
		else:
			print "...ERROR"
			return -1

	def erase_user(self, SH, SL, EH, EL):
		length = 0x08
		
		StartH = SH
		StartL = SL
		EndH = EH
		EndL = EL
		
		xor = (SOYAL_ORIGINAL_XOR ^ self.node ^ SOYAL_ERASE_USER_DATA ^ StartH ^ StartL ^ EndH ^ EndL) % 256
		sum1 = (self.node + SOYAL_ERASE_USER_DATA + StartH + StartL + EndH + EndL + xor) % 256
		buffer1 = struct.pack('BBBBBBBBBB', SOYAL_HEADER_STANDARD, length, self.node, SOYAL_ERASE_USER_DATA, StartH, StartL, EndH, EndL, xor, sum1)
		
		send_data = self.s.send(buffer1)
		recv_data = self.__read_packet()
		
		cmd = struct.unpack('B', str(recv_data)[3:4])[0]
		
		if cmd == SOYAL_CMD_ACK:
			print "...SUCCESS"
			return 0
		else:
			print "...ERROR"
			return -1

	def get_user(self, AH, AL, N):
		length = 0x07
		
		AddrH = AH
		AddrL = AL
		Nums = N
		
		xor = (SOYAL_ORIGINAL_XOR ^ self.node ^ SOYAL_GET_USER_PARM ^ AddrH ^ AddrL ^ Nums) % 256
		sum1 = (self.node + SOYAL_GET_USER_PARM + AddrH + AddrL + Nums + xor) % 256
		
		buffer1 = struct.pack('BBBBBBBBB', SOYAL_HEADER_STANDARD, length , self.node, SOYAL_GET_USER_PARM, AddrH, AddrL, Nums, xor, sum1)
		
		send_data = self.s.send(buffer1)
		
		recv_data = self.__read_packet()
		
		cmd = struct.unpack('B', str(recv_data)[3:4])[0]
		
		if cmd == SOYAL_ECHO_DATA:
			print "...SUCCESS"
			
			self.user.get_data = struct.unpack('25B', str(recv_data)[4:29])
			
			return 0
		else:
			print "...ERROR"
			return -1

class MCS:
	def __init__(mcs, id, key):
		mcs.deviceId = id
		mcs.deviceKey = key

	def post_to_mcs(mcs, payload):
		headers = {"Content-type": "application/json", "deviceKey": mcs.deviceKey}
		not_connected = 1
		while (not_connected):
			try:
				conn = httplib.HTTPConnection("api.mediatek.com:80")
				conn.connect()
				not_connected = 0
			except (httplib.HTTPException, socket.error) as ex:
				print "Error: %s" % ex
				time.sleep(10)  # sleep 10 seconds#

		conn.request("POST", "/mcs/v2/devices/" + mcs.deviceId + "/datapoints", json.dumps(payload), headers)
		response = conn.getresponse()
		print( response.status, response.reason, json.dumps(payload), time.strftime("%c"))
		data = response.read()
		return response.status
		conn.close()

class Message_Server:
	def __init__(M_self, server_ip, server_port):
		M_self.address = (server_ip,server_port)
		M_self.event_log = Soyal_Event
	
	def connect(M_self):
		M_self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		M_self.s.bind(M_self.address)
		M_self.s.listen(1)
	
	def accept(M_self):
		M_self.conn, M_self.addr = M_self.s.accept()
		recv_data = M_self.conn.recv(SOYAL_MAX_DATA_TCP)

		header = struct.unpack('I', str(recv_data)[0:4])[0]
		length = struct.unpack('B', str(recv_data)[4:5])[0] * 256 + struct.unpack('B', str(recv_data)[5:6])[0]
		
		if header == 0xa55a00ff:
			if length == 0x21:
				M_self.event_log.EventCode = struct.unpack('B', str(recv_data)[7:8])[0]
				M_self.event_log.SourceNodeId = struct.unpack('B', str(recv_data)[8:9])[0]
#				Event time
				M_self.event_log.Second = struct.unpack('B', str(recv_data)[9:10])[0]
				M_self.event_log.Minute = struct.unpack('B', str(recv_data)[10:11])[0]
				M_self.event_log.Hour = struct.unpack('B', str(recv_data)[11:12])[0]
				M_self.event_log.Weekday = struct.unpack('B', str(recv_data)[12:13])[0]
				M_self.event_log.Day = struct.unpack('B', str(recv_data)[13:14])[0]
				M_self.event_log.Month = struct.unpack('B', str(recv_data)[14:15])[0]
				M_self.event_log.Year = struct.unpack('B', str(recv_data)[15:16])[0] + 2000
				
				t = datetime.datetime(M_self.event_log.Year, M_self.event_log.Month, M_self.event_log.Day, M_self.event_log.Hour, M_self.event_log.Minute, M_self.event_log.Second)
#				Timestamp is minisecond for MCS
				M_self.event_log.Timestamp = time.mktime(t.timetuple()) * 1000

#				Event User data
				M_self.event_log.Address = struct.unpack('B', str(recv_data)[17:18])[0] * 256 + struct.unpack('B', str(recv_data)[18:19])[0]
				M_self.event_log.Level = struct.unpack('B', str(recv_data)[22:23])[0]
				M_self.event_log.TagHi = struct.unpack('B', str(recv_data)[23:24])[0] * 256 + struct.unpack('B', str(recv_data)[24:25])[0]
				M_self.event_log.Door = struct.unpack('B', str(recv_data)[25:26])[0]
				M_self.event_log.TagLo = struct.unpack('B', str(recv_data)[27:28])[0] * 256 + struct.unpack('B', str(recv_data)[28:29])[0]
				return 0
				
				print 
			elif length == 0x04:
#				print "Eventlog is empty"
				return 1
			else:
				print "Error"
				return -1

		M_self.conn.close()

	def disconnect(M_self):
		M_self.s.close()

"""if __name__ == "__main__":
	
	soyal = Soyal('192.168.1.104', 1621, 1)
	
	soyal.connect()
	
	MS = Message_Server('192.168.1.105',1109)
	
	MS.connect()
	
	mcs = MCS("DH0ipQDb", "h82HqT0FnRMwr1PU")
	
	while True:
		if MS.accept() == 0:
			Log = {
					"EventCode" : MS.event_log.EventCode,
					"SourceNodeId" : MS.event_log.SourceNodeId,
					"Year" : MS.event_log.Year,
					"Month" : MS.event_log.Month,
					"Weekday" : MS.event_log.Weekday,
					"Day" : MS.event_log.Day,
					"Hour" : MS.event_log.Hour,
					"Minute" : MS.event_log.Minute,
					"Second" : MS.event_log.Second,
					"Address" : MS.event_log.Address,
					"Door" : MS.event_log.Door,
					"Level" : MS.event_log.Level,
					"TagHi" : MS.event_log.TagHi,
					"TagLo" : MS.event_log.TagLo
					}
			Log = json.dumps(Log)
			
			payload = {"datapoints":[
										{
											"dataChnId":"display2",
											"timestamp":MS.event_log.Timestamp,
											"values":{
														"value":Log
														}
										}
									]
								}
			
			mcs.post_to_mcs(payload)

			soyal.remove_oldest_eventlog()
		elif MS.accept() == 1:
			print "Eventlog is empty"
		
		time.sleep(1)

	soyal.disconnect()
	MS.disconnect()"""