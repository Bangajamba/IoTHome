
def returnValue(strValue):
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

def changeData(msg):
    result = "_"
    try:
        #TODO CHANGE BACK MSG
        msgs = msg.split(",") #msg.payload.decode().split(",")
        size = len(msgs)
        if size > 1 and size % 2 == 0:
            arr = []
            index = 0
            while index < size:
                temp = {}
                temp['key'] = msgs[index]
                temp['value'] = returnValue(msgs[(index+1)])
                arr.append(temp)
                index += 2
            result = arr
            
    except Exception as e:
        print(e)

    return result

data = changeData('temp,5.5,hum,30,isDead,1')

result = {}
for d in data:
    result[d['key']] = d['value']
print(result)