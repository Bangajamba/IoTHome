from influxdb import InfluxDBClient
import logging
import datetime

class InfluxDB():
    def __init__(self, ip):
        
        #InfluxDB
        self.inflexConnected = False #not in use
        self.ip = ip
        self.connectInflexDB() 

    def connectInflexDB(self):
        try:
            self.influx_client = InfluxDBClient(self.ip, 8086, username='admin', password='secretpassword',database='iot')
            self.inflexConnected = True
        except:
            logging.info("Failed Connect InflexDB")

    def returnValue(self, strValue):
        result = strValue
        try:
            result = float(strValue)
            if result.is_integer():
                result = int(strValue)
        except:
            try:
                result = int(strValue)
            except:
                
                try:
                    print(result)
                    if result == "True" or result == "true":
                        result = 1
                    elif result == "False" or result == "false":
                        result = 0
                except:
                    pass    
        return result

    def sendToInfluxDB(self, topic, msg):
        current_time = datetime.datetime.utcnow().isoformat()

        result = {}
        if len(msg) > 1:
            for m in msg:
                result[m['key']] = m['value']
        elif len(msg) == 1:
            result['PAYLOADSTRING'] = msg[0] 
        else:
            logging.info("payload weird size, payload<=0")

        json_body = [
            {
                "measurement": str(topic),
                "tags": {},
                "time": current_time,
                "fields": result
            }
        ]
        try:
            logging.info(json_body)
            self.influx_client.write_points(json_body)
        except Exception as e:
            logging.info("fail write to influx:" + str(e))