import socket
import vizact
import viz
import random
import math

random.seed(1)

class TrackedBody():
	def __init__(self):
		self.x = 0
		self.y = 0
		self.z = 0
		self.yaw = 0.0
		self.pitch = 0.0
		self.roll = 0.0

#The maximum amount of data to receive at a time
MAX_DATA_SIZE = 512
global splits
global x,y,z,jx,jy,flystickx,flysticky,flystickz,flystickButtons,fsx,fsy,fsz, fsYaw, fsPitch, fsRoll, fsDerp,x1,y1,z1,x2,y2,z2,x3,y3,z3,yaw,pitch,roll
global default
flystickButtons = [False,False,False,False,False]
default = [0,1.7,0]
x=default[0]
y=default[1]
z=default[2]
jx=0
jy=0
flystickx=0
flysticky=0 
flystickz=0
fsx = 0
fsy = 0
fsz = 0
x1=0
x2=0
x3=0
y1=0
y2=0
y3=0
z1=0
z2=0
z3=0
yaw = 0.0
pitch = 0.0
roll = 0.0
#array = (1,2,3) #populate the array with random 

lantern = TrackedBody()
#array = (1,2,3) #populate the array with random 

#The port to send/receive data on - this must be configured in DTrack for it to work. :)
PORT = 5001

#Create a socket to receive data via udp from (datagram socket = udp)
InSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
InSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
InSocket.bind(('', PORT))
InSocket.setblocking(0)

def ReceiveData():
	lastLine = ""
	try:
		#print "START LISTENING FOR DATA:"
		while(1):
			lastLine = InSocket.recv(MAX_DATA_SIZE)
	except socket.error:
		#Insert error handling code here
		#print "Nothing to receive!"
		return lastLine
		#pass

global enabled
enabled=True
def enable():
	global enabled
	enabled=True
	print 'enabling tracking'
def disable():
	global x,y,z
	global default
	global enabled
	enabled=False
	print 'disabling tracking.'
	x=default[0]
	y=default[1]
	z=default[2]
def getLocation(): #this is called by whatever program is using this script
	return (x,y,z)
def PrintData(): #this prints the splits array so you can identify what is going on
	print '--------------------------------------------------------'
	buf = ""
	for index in range(len(splits)):
		buf += str(index)+"<"+splits[index]+">\t" 
	print "glasses euler: "+str(yaw)+","+str(pitch)+","+str(roll)
	print buf
def CheckSocket():
	global x,y,z,jx,jy,flystickx,flysticky,flystickz,flystickButtons,fsx,fsy,fsz, fsPitch, fsRoll, fsYaw, fsDerp,x1,y1,z1,x2,y2,z2,x3,y3,z3,yaw,pitch,roll
	global splits
	if enabled == True:
		#Try to receive data from socket
		data = ReceiveData()
		if data:
			#print 'Received Message: <<<',data,'>>>'
			#based on the datat that is received, if we search and replace stuff within the data string, we end up with data separated by a single space.
			data = data.replace("["," ")
			data = data.replace("]"," ")
			data = data.replace("\n"," ") 
			data = data.replace("\r"," ")
			data = data.replace("  "," ")
			data = data.replace("  "," ")
			data = data.replace("  "," ")
			#data is now separated by a single space
			splits = data.split(' '); #split the data string into chunks delimited by ' '
			
			
			
		
			if(len(splits)>27): #when splits array has less than 30 elements, it doesn't have the glasses tracking. (There may be other cases when this is true.)
				x=float(splits[28])/1000 #28 left/right right+ 0 in centre
				y=float(splits[30])/1000 #30 up/down up+ 0 on floor
				z=float(splits[29])/1000 #29 in/out in+
				yaw=-float(splits[33]) #28 left/right right+ 0 in centre Verified 0 forward -90 right -180 backwards  to +90 left (range -180 to +180)
				pitch=-float(splits[31]) #30 up/down up+ 0 on floor Verified 0 forward -90 down -180 backwards +90 up (range -180 to +180)
				roll=-float(splits[32]) #29 in/out in+ 
				
				if(len(splits)>45):
					lantern.x = float(splits[45])/1000
					lantern.y = float(splits[47])/1000
					lantern.z = float(splits[46])/1000
					lantern.yaw = -float(splits[50])
					lantern.pitch=float (splits[48])
					lantern.roll =- float(splits[49])
				
			jx=float(splits[22]) #joystick x forward = +1, backward = -1 
			jy=float(splits[23]) #joystick y left = -1, right = +1
			
			
			fsx = float(splits[9])/1000 #flystick x left = -1, right = +1
			fsy = float(splits[11])/1000 #flystick y down= -1, up = +1
			fsz = float(splits[10])/1000 #flystick z out = -1, i = +1
			
			'''
			fsYaw= float(splits[13]) #left +1, right -1
			fsPitch = float(splits[17]) #up +1, down -1
			fsRoll = float(splits[14]) #cw+1, ccw -1
			fsDerp = float (splits[12]) #forward +1 , backwards -1, tracks the motion when controller aim towards the screen/vice versa
'''
			
			x1= float(splits[12])/1000
			y1= float(splits[14])/1000
			z1= float(splits[13])/1000
			
			x2= float(splits[15])/1000
			y2= float(splits[17])/1000
			z2= float(splits[16])/1000
			
			x3= float(splits[18])/1000
			y3= float(splits[20])/1000
			z3= float(splits[19])/1000
			
			#print 'fsx', fsx
			for button in range(0,5):
				if(int(splits[21]) & int(math.pow(2,button))):
					flystickButtons[button] = True
				else:
					flystickButtons[button] = False
	else: #tracking is disabled. Set to default
		x=default[0]
		y=default[1]
		z=default[2]

enable() #enable tracking by default
vizact.ontimer(0.01,CheckSocket) #check the socket as fast as possible
vizact.onkeydown(' ',PrintData) #in order to debug and reverse engineer what number is what within the splits array
#viz.go()