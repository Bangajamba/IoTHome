from influxdb import InfluxDBClient
import datetime

#InfluxDB

influx_client = InfluxDBClient("localhost", 8086,database='iot')
#influx_client.create_database('iot')

current_time = datetime.datetime.utcnow().isoformat()
json_body = [
    {
        "measurement": "Pir",
        "tags": {},
        "time": current_time,
        "fields": {
            "value": 5 
        }
    }
]
try:
    influx_client.write_points(json_body)
except Exception as e:
    print(str(e))