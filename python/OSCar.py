from OSC import OSCServer,OSCClient, OSCMessage
import types
import serial

server = OSCServer( ("192.168.240.1", 8000) )
client = OSCClient()
client.connect( ("192.168.240.195", 9000) )
arduino = serial.Serial('/dev/ttyATH0', 115200)

#waits for slider change
def handle_timeout(self):
    print ("Timeout")

server.handle_timeout = types.MethodType(handle_timeout, server)

# function to do the work. path refers to the fader name, args refers to the value of the slider
def fader_callback(path, tags, args, source):
    global fader1Feedback
    if path=="/1/fader1":
        fader1Feedback = int(args[0])
        msg = OSCMessage("/1/label1")
        msg.insert(0, fader1Feedback)
        print "Fader 1 %i" % fader1Feedback
        client.send(msg)
        if (fader1Feedback > 100):
            arduino.write('F')
            arduino.write('\n')
            arduino.write('%i' % fader1Feedback)
            arduino.write('\n')
        if (fader1Feedback < 90):
            arduino.write('B')
            arduino.write('\n')
            arduino.write('%i' % fader1Feedback)
            arduino.write('\n')
        elif ((fader1Feedback < 100) and (fader1Feedback > 90)):
            arduino.write('S')
            arduino.write('\n')
            arduino.write('%i' % fader1Feedback)
            arduino.write('\n')
            
        

        
def fader2_callback(path, tags, args, source):
    global fader2Feedback
    if path=="/1/fader2":
        fader2Feedback = int(args[0])
        msg = OSCMessage("/1/label2")
        msg.insert(0, fader2Feedback)
        print "Fader 2 %i" % fader2Feedback
        client.send(msg)
        arduino.write('Y')
        arduino.write('\n')
        arduino.write('%i' % fader2Feedback)
        arduino.write('\n')
        
def xypad(path, tags, args, source):
    yy=int(args[0])
    xx=int(args[1])#Value 2 is used with XP pads, it will get the 'x' value
    print "Value of Y:", yy,  "    Value of X:", xx
    if (xx > 100):
            arduino.write('F')
            arduino.write('\n')
            arduino.write('%i' % xx)
            arduino.write('\n')
    if (xx < 90):
            arduino.write('B')
            arduino.write('\n')
            arduino.write('%i' % xx)
            arduino.write('\n')
    elif ((xx < 100) and (xx > 90)):
            arduino.write('S')
            arduino.write('\n')
            arduino.write('%i' % xx)
            arduino.write('\n')
    arduino.write('Y')
    arduino.write('\n')
    arduino.write('%i' % yy)
    arduino.write('\n')

def kill_switch(path, tags, args, source):
    state=int(args[0])
    print "Kill Switch:", state
    if state == 1:
        arduino.write('S')
        
def lights(path, tags, args, source):
    state=int(args[0])
    print "Lights:", state
    arduino.write('L')
    arduino.write('\n')
    arduino.write('%i' % state)
    arduino.write('\n')
#execute


    
server.addMsgHandler( "/1/fader1", fader_callback)
server.addMsgHandler( "/1/fader2", fader2_callback)
server.addMsgHandler("/1/xy1", xypad)
server.addMsgHandler("/1/push1", kill_switch)
server.addMsgHandler("/1/toggle1", lights)
while True:
    server.handle_request()

#arduino.close()
server.close()
