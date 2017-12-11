import soyal
import datetime
import time
import json

deviceId = "DH0ipQDb"  
deviceKey = "h82HqT0FnRMwr1PU"
dataChnId = "display"

soyal2 = soyal.Soyal('192.168.1.104',1621,1)

soyal2.connect()

test_mcs = soyal.MCS(deviceId, deviceKey)

"""soyal.user.Records = 1
soyal.user.Addr = 16
soyal.user.TagHi = 12345
soyal.user.TagLo = 12345
soyal.user.Pin = 123
soyal.user.Mode = 143
soyal.user.Door1 = 255
soyal.user.Door2 = 255
soyal.user.Year = 2017
soyal.user.Month = 1
soyal.user.Day = 1
# Level 3 = 192(11000000), 2 = 128(10000000) , 1 = 64(01000000)
soyal.user.Level = 192
soyal.user.Zone = 0
soyal.user.Option = 128"""

#soyal.set_user()

#Set Soyal Clock

#soyal2.get_oldest_eventlog()

#print soyal.EventCode_Dict[soyal2.event_log.EventCode]

#soyal.get_clock()

#soyal.set_clock()

#soyal.empty_eventlog()

#print soyal.event_log.AddressHi
#print soyal.event_log.TagHi
#print soyal.event_log.AddressLo

#print soyal.clock.RID,soyal.clock.Year,soyal.clock.Month,soyal.clock.Day,soyal.clock.Weekday,soyal.clock.Hour,soyal.clock.Minute,soyal.clock.Second

#soyal.get_user(0,16,2)

#print soyal.user.get_data

#soyal.erase_user(0,24,0,24)

#soyal.remove_oldest_eventlog()


#a = soyal2.get_mcs(deviceId, deviceKey, dataChnId)

#print a

while True:
    print "========================================"
    log = soyal2.get_oldest_eventlog()


    if log == 0:
        r = {"EventCode" : soyal2.event_log.EventCode,
             "SourceNodeId" : soyal2.event_log.SourceNodeId,
             "Year" : soyal2.event_log.Year,
             "Month" : soyal2.event_log.Month,
             "Day" : soyal2.event_log.Day,
             "Hour" : soyal2.event_log.Hour,
             "Minute" : soyal2.event_log.Minute,
             "Second" : soyal2.event_log.Second,
             "Address" : soyal2.event_log.Address,
             "Door" : soyal2.event_log.Door,
             "Level" : soyal2.event_log.Level,
             "TagHi" : soyal2.event_log.TagHi,
             "TagLo" : soyal2.event_log.TagLo}

        r = json.dumps(r)

        payload = {"datapoints":[
                                    {
                                        "dataChnId":"display2",
                                        "timestamp":soyal2.event_log.Timestamp,
                                        "values":{
                                            "value":r
                                            }
                                        }
                                    ]
                                  }

        rc = test_mcs.post_to_mcs(payload)
		
        if rc == 200:
            soyal2.remove_oldest_eventlog()

    time.sleep(1)

"""    print "========================================"

    r = soyal2.get_mcs(deviceId, deviceKey, dataChnId)
    
    if a==r:
        print "MCS資料尚未更新:..."
    else:
        print "MCS資料已更新為:..."
        print r
        soyal2.set_user()
        a=r

    time.sleep(1)"""
