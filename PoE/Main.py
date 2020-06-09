from http.server import HTTPServer, BaseHTTPRequestHandler 
from socketserver import ThreadingMixIn
import argparse
import logging
import json
#Custom Modules
from IoTPlatform import IoTPlatform
from EventHandler import EventHandler

# Args
parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--ip', default='127.0.0.1', action='store', type=str, help='ipaddres to connect')
args = parser.parse_args()

IPAddress = args.ip

logging.basicConfig(level=logging.INFO)
logging.info("StartCreate")

# Creating Custom Classes
iotPlatform = IoTPlatform(IPAddress)
eventHandler = EventHandler()

class ThreadingSimpleServer(ThreadingMixIn, HTTPServer):
    pass

class HTTPServer_RequestHandler(BaseHTTPRequestHandler):      
    def do_POST(self):
        self.send_response(200)
        # change to one origin
        self.send_header('Access-Control-Allow-Origin', '*') 
        self.end_headers()
        
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself  
        
        command, splittedMsg = self.extractObjFromMessage(post_data)
        responseMessage = self.executeRequest(command, splittedMsg)

        #time.sleep(0) #test slow callbacks, change value
        self.wfile.write(responseMessage)
        #self.wfile.write(bytes(message, "utf-8")) #message in bytes
        return
        
    # msg[0] is command, msg is splitted with command arguments
    # Send,name,ON -> msg[0]="Send", msg = {"Send", "name", "ON"}
    def extractObjFromMessage(self, requestMessage):
        requestMessage = requestMessage.decode('utf-8')
        j = json.loads(requestMessage)
        return j['command'], j
        #msg = requestMessage.split(",")
        #return #msg[0], msg

    def executeRequest(self, command, msg):
        result = "Not Implemented"

        if command == "GetNodes":
            result = iotPlatform.getNodes()
        elif command == "Add":
            iotPlatform.addNodeAndSaveFile(msg['msg'].split(",")[0])
            result = "Added"
        elif command == "Remove":
            pass
        elif command == "Test":
            nodePos = msg['msg'].find(",")
            nodeName = msg['msg'][0:nodePos]
            msgs = [msg['msg'][nodePos+1:len(msg['msg'])]]
            iotPlatform.nodeSendPayload(
                str(nodeName), 
                str(msgs))
            result = "Sent Message"
        elif command == "SpeechCall":
            pass
        elif command == "AddEvent":
            src = msg['msg']['src']
            des = msg['msg']['des']
            eventID = eventHandler.addEvent(src, des)
            iotPlatform.addTriggersToNodesAndSaveFile(src, eventID)
            print(iotPlatform.getNodes())
        else:
            result = "None"
        
        return bytes(result, "utf-8")

if __name__ == "__main__":
    try:
        server = ThreadingSimpleServer(("0.0.0.0", 8080), HTTPServer_RequestHandler)
        server.serve_forever()
    except Exception as e:
        logging.info(str(e))
        while True:
            pass

    
