#import viz
import vizcave
import viztracker
import vizact
import time
import array
import socket
import artTracker
import random
import math
import vizjoy

#IMPORTANT: Need to add a joystick. This will return the first detected joystick
joy = vizjoy.add()
#####################
#get Zepplin
import Zeppelin
from Zeppelin import ZEP
#####################
#setup CAVE
viz.multiSample = 4
polyMode = viz.POLY_WIRE
#viz.setFarPlane(1)
#viz.setMultiSample(config.multiSample) seems to give this error message
viz.window.setPolyMode(viz.POLY_WIRE)
viz.MainWindow.fov(50)
viz.vsync(0)#this may increase frame rate but may get tears
speed = 22000 # move speed

compass = viz.addChild('Meshes/arrow.osgb')
compass.color(0.2,0.8,0.8)

GO_FAST = False
speed = 2000000 # move speed
rot_speed = 17 # rotate speed
#####################
#Setup OSC
from OSC import OSCClient, OSCMessage 
#OSCHOST  = "172.16.101.174"

OSCHOST  = "localhost" # On windows supercollider, use port 57121 instead of 57120
client = OSCClient()
client.connect( (OSCHOST, 57121) )
#####################
def setCave():
	global cave, height, width, depth
	viz.go(viz.FULLSCREEN |viz.QUAD_BUFFER)
	viz.window.setFullscreen(1)

	height = 3.049
	width = 5.638
	depth = 3.049

	#W,H,D
	blendVertical=0.19
	blendHorizontal=0.222
	A=-width/2,height,0
	B=-width/2,height,depth
	C=width/2,height,depth
	D=width/2,height,0

	E=-width/2,0,0
	F=-width/2,0,depth
	G=width/2,0,depth
	H=width/2,0,0

	AET=-width/2,height/2+blendVertical,0
	BFT=-width/2,height/2+blendVertical,depth
	AEB=-width/2,height/2-blendVertical,0
	BFB=-width/2,height/2-blendVertical,depth

	CGT=width/2,height/2+blendVertical,depth
	DHT=width/2,height/2+blendVertical,0
	CGB=width/2,height/2-blendVertical,depth
	DHB=width/2,height/2-blendVertical,0

	EFT=-width/2,0,depth/2+blendVertical
	EFB=-width/2,0,depth/2-blendVertical

	GHT=width/2,0,depth/2+blendVertical
	GHB=width/2,0,depth/2-blendVertical

	BCL=-blendHorizontal,height,depth
	BCR=+blendHorizontal,height,depth
	FGL=-blendHorizontal,0,depth
	FGR=+blendHorizontal,0,depth

	FET=-width/2,0,depth/2+blendVertical
	FEB=-width/2,0,depth/2-blendVertical

	EHL=-blendHorizontal,0,0
	EHR=blendHorizontal,0,0

	GHT=width/2,0,depth/2+blendVertical
	GHB=width/2,0,depth/2-blendVertical

	BCFGTL=-blendHorizontal,height/2+blendVertical,depth
	BCFGTR=+blendHorizontal,height/2+blendVertical,depth
	BCFGBL=-blendHorizontal,height/2-blendVertical,depth
	BCFGBR=+blendHorizontal,height/2-blendVertical,depth

	FGEHTL=-blendHorizontal,0,depth/2+blendVertical
	FGEHTR=+blendHorizontal,0,depth/2+blendVertical
	FGEHBL=-blendHorizontal,0,depth/2-blendVertical
	FGEHBR=+blendHorizontal,0,depth/2-blendVertical

	#-w,h,d
	Ch1 = vizcave.Wall(
		upperLeft=A,
		upperRight=B,
		lowerLeft=AEB,
		lowerRight=BFB,
		name='Left Top Wall' )

	Ch2 = vizcave.Wall(
		upperLeft=AET,
		upperRight=BFT,
		lowerLeft=E,
		lowerRight=F,
		name='Left Bottom Wall' )

	Ch3 = vizcave.Wall(
		upperLeft=B,
		upperRight=BCR,
		lowerLeft=BFB,
		lowerRight=BCFGBR,
		name='Front TL Wall' )

	Ch4 = vizcave.Wall(
		upperLeft=BFT,
		upperRight=BCFGTR,
		lowerLeft=F,
		lowerRight=FGR,
		name='Front BL Wall' )

	Ch5 = vizcave.Wall(
		upperLeft=BCL,
		upperRight=C,
		lowerLeft=BCFGBL,
		lowerRight=CGB,
		name='Front TR Wall' )

	Ch6 = vizcave.Wall(
		upperLeft=BCFGTL,
		upperRight=CGT,
		lowerLeft=FGL,
		lowerRight=G,
		name='Front BR Wall' )

	Ch7 = vizcave.Wall(
		upperLeft=C,
		upperRight=D,
		lowerLeft=CGB,
		lowerRight=DHB,
		name='Right Top Wall' )

	Ch8 = vizcave.Wall(
		upperLeft=CGT,
		upperRight=DHT,
		lowerLeft=G,
		lowerRight=H,
		name='Right Bottom Wall' )

	Ch9 = vizcave.Wall(
		upperLeft=F,
		upperRight=FGR,
		lowerLeft=FEB,
		lowerRight=FGEHBR,
		name='Bottom TL Wall' )

	Ch10 = vizcave.Wall(
		upperLeft=FET,
		upperRight=FGEHTR,
		lowerLeft=E,
		lowerRight=EHR,
		name='Bottom BL Wall' )

	Ch11 = vizcave.Wall(
		upperLeft=FGL,
		upperRight=G,
		lowerLeft=FGEHBL,
		lowerRight=GHB,
		name='Bottom TR Wall' )

	Ch12 = vizcave.Wall(
		upperLeft=FGEHTL,
		upperRight=GHT,
		lowerLeft=EHL,
		lowerRight=H,
		name='Bottom BR Wall' )

	FrontWall = vizcave.Wall(
		upperLeft=B,
		upperRight=C,
		lowerLeft=F,
		lowerRight=G,
		name='Front Wall' )

	cave.addWall(FrontWall, mask=viz.MASTER)
	cave.addWall(Ch1, mask=viz.CLIENT1)
	cave.addWall(Ch2, mask=viz.CLIENT2)
	cave.addWall(Ch3, mask=viz.CLIENT3)
	cave.addWall(Ch4, mask=viz.CLIENT4)
	cave.addWall(Ch5, mask=viz.CLIENT5)
	cave.addWall(Ch6, mask=viz.CLIENT6)
	cave.addWall(Ch7, mask=viz.CLIENT7)
	cave.addWall(Ch8, mask=viz.CLIENT8)
	cave.addWall(Ch9, mask=viz.CLIENT9)
	cave.addWall(Ch10, mask=1024)
	cave.addWall(Ch11, mask=2048)
	cave.addWall(Ch12, mask=4096)

	global viewTracker
	global cave_origin, counter
	viewTracker = viztracker.KeyboardMouse6DOF()
	magicCarpet = viztracker.KeyboardMouse6DOF()
	viewTracker.setPosition(0,0,0)
	cave.setTracker(pos=viewTracker)
	cave_origin = vizcave.CaveView(viewTracker)
	view = viz.MainView
	counter = 0

def trackingEnable():
	artTracker.enable
		
def artTrackerUpdate():
	
#	print viz.elapsed() #about 0.003
	elapsed = viz.elapsed()
	fps_speed = elapsed*speed
	fps_rot_speed = elapsed*rot_speed
	
	if GO_FAST:
		fps_speed *= 10
		fps_rot_speed *= 5
	
	viewTracker.setPosition(artTracker.x,artTracker.y,artTracker.z+depth/2)
	viewTracker.setEuler(artTracker.yaw,artTracker.pitch,artTracker.roll)
	
	cave_origin.setPosition(artTracker.jy*artTracker.x2*fps_speed, artTracker.jy*artTracker.y2*fps_speed, artTracker.jy*artTracker.z2*fps_speed,viz.REL_LOCAL)
	cave_origin.setEuler(fps_rot_speed*artTracker.jx,0.0,0.0,viz.REL_LOCAL)	 
	
	
	pos = cave_origin.getPosition()
	eul = cave_origin.getEuler()
	
	
	
def updateVisibilityHive():
	updateVisibility(cave_origin.getPosition())
	pass
	
####################

PIECESNAMES=[
#groups of rows

'TerrainTestsSetof8/Grid2.OSGB',
'TerrainTestsSetof8/Grid2.OSGB',
'TerrainTestsSetof8/Grid2.OSGB',
'TerrainTestsSetof8/Grid2.OSGB',
'TerrainTestsSetof8/Grid2.OSGB',
'TerrainTestsSetof8/Grid2.OSGB',
'TerrainTestsSetof8/Grid2.OSGB',
'TerrainTestsSetof8/Grid2.OSGB',
'TerrainTestsSetof8/Grid2.OSGB',
'TerrainTestsSetof8/Grid2.OSGB',


'TerrainTestsSetof8/Grid2.OSGB',
'TerrainTestsSetof8/C1.OSGB',
'TerrainTestsSetof8/C2.OSGB',
'TerrainTestsSetof8/C3.OSGB',
'TerrainTestsSetof8/C4.OSGB',
'TerrainTestsSetof8/C5.OSGB',
'TerrainTestsSetof8/C6.OSGB',
'TerrainTestsSetof8/C7.OSGB',
'TerrainTestsSetof8/C8.OSGB',
'TerrainTestsSetof8/Grid2.OSGB',

'TerrainTestsSetof8/Grid2.OSGB',
'TerrainTestsSetof8/B13.OSGB',
'TerrainTestsSetof8/B14.OSGB',
'TerrainTestsSetof8/B15.OSGB',
'TerrainTestsSetof8/B16.OSGB',
'TerrainTestsSetof8/M.OSGB',
'TerrainTestsSetof8/N.OSGB',
'TerrainTestsSetof8/O.OSGB',
'TerrainTestsSetof8/P.OSGB',
'TerrainTestsSetof8/Grid2.OSGB',

'TerrainTestsSetof8/Grid2.OSGB',
'TerrainTestsSetof8/B9.OSGB',
'TerrainTestsSetof8/B10.OSGB',
'TerrainTestsSetof8/B11.OSGB',
'TerrainTestsSetof8/B12.OSGB',
'TerrainTestsSetof8/I.OSGB',
'TerrainTestsSetof8/J.OSGB',
'TerrainTestsSetof8/K.OSGB',
'TerrainTestsSetof8/L.OSGB',
'TerrainTestsSetof8/Grid2.OSGB',

'TerrainTestsSetof8/Grid2.OSGB',
'TerrainTestsSetof8/B5.OSGB',
'TerrainTestsSetof8/B6.OSGB',
'TerrainTestsSetof8/B7.OSGB',
'TerrainTestsSetof8/B8.OSGB',
'TerrainTestsSetof8/E.OSGB',
'TerrainTestsSetof8/F.OSGB',
'TerrainTestsSetof8/G.OSGB',
'TerrainTestsSetof8/H.OSGB',
'TerrainTestsSetof8/Grid2.OSGB',

'TerrainTestsSetof8/Grid2.OSGB',
'TerrainTestsSetof8/B1.OSGB',
'TerrainTestsSetof8/B2.OSGB',
'TerrainTestsSetof8/B3.OSGB',
'TerrainTestsSetof8/B4.OSGB',
'TerrainTestsSetof8/A.OSGB',
'TerrainTestsSetof8/B.OSGB',
'TerrainTestsSetof8/C.OSGB',
'TerrainTestsSetof8/D.OSGB',
'TerrainTestsSetof8/Grid2.OSGB',

'TerrainTestsSetof8/Grid2.OSGB',
'TerrainTestsSetof8/G00.OSGB',
'TerrainTestsSetof8/G10.OSGB',
'TerrainTestsSetof8/G20.OSGB',
'TerrainTestsSetof8/G30.OSGB',
'TerrainTestsSetof8/S01.OSGB',
'TerrainTestsSetof8/S02.OSGB',
'TerrainTestsSetof8/S03.OSGB',
'TerrainTestsSetof8/S04.OSGB',
'TerrainTestsSetof8/Grid2.OSGB',

'TerrainTestsSetof8/Grid2.OSGB',
'TerrainTestsSetof8/G01.OSGB',
'TerrainTestsSetof8/G11.OSGB',
'TerrainTestsSetof8/G21.OSGB',
'TerrainTestsSetof8/G31.OSGB',
'TerrainTestsSetof8/S05.OSGB',
'TerrainTestsSetof8/S06.OSGB',
'TerrainTestsSetof8/S07.OSGB',
'TerrainTestsSetof8/S08.OSGB',
'TerrainTestsSetof8/Grid2.OSGB',

'TerrainTestsSetof8/Grid2.OSGB',
'TerrainTestsSetof8/Grid2.OSGB',
'TerrainTestsSetof8/Grid2.OSGB',
'TerrainTestsSetof8/Grid2.OSGB',
'TerrainTestsSetof8/Grid2.OSGB',
'TerrainTestsSetof8/Grid2.OSGB',
'TerrainTestsSetof8/Grid2.OSGB',
'TerrainTestsSetof8/Grid2.OSGB',
'TerrainTestsSetof8/Grid2.OSGB',
'TerrainTestsSetof8/Grid2.OSGB'
]

################################
PIECES = []
scaling = 5600
unit = 10 * scaling
rows = 9 #	horizontal
columns = 10
def placePieces():
	curRow = 0
	curCol = 0
	for Name in PIECESNAMES:
		PIECES.append(viz.addChild(Name))
	for piece in PIECES:
			piece.setPosition(curCol * unit, 0 ,curRow * unit)
			piece.color(0.2,0.8,0.8)
			curCol = curCol + 1
			if curCol == columns:
				curCol = 0
				curRow = curRow + 1
				
placePieces()

def setScaling(): #Maybe dont use this until the unit thing is figured out for good
	for piece in PIECES:
		piece.setScale( scaling, scaling, scaling )
		
setScaling()

###############################
#gives readout of which pice you are over
def checkProx(player, piece):
	distance = math.sqrt((player[0] - piece[0])**2 + (player[2] - piece[2])**2)
	return distance
		
LastName = ''	
def IAmHere():
	global LastName
	view = view = viz.MainView
	position = viz.Vector(view.getPosition())
	currentPiece = -1
	smallestDistance = 9999999999
	for i in range(len(PIECES)):
		prox = checkProx(position, PIECES[i].getPosition())
		if prox < smallestDistance:
			smallestDistance = prox
			currentPiece = i
	if PIECESNAMES[currentPiece]!= LastName:
		LastName = PIECES[currentPiece]
#		uncomment print line below to get a readout of what pice you are over
#		print PIECESNAMES[currentPiece]	

vizact.ontimer(1,IAmHere)
#################################

############################
############################
#this thing makes the tiles fade over distance
maxDISTANCE = 56000	# smaller value means faded sooner
minAlpha = 0.0		# MIN brightness
maxAlpha = 0.6 		# MAX brightness

def LandVisible():
	view = view = viz.MainView
	WhereAmIVect = viz.Vector(view.getPosition())
	for piece in PIECES:
		box = piece.getBoundingBox(mode = viz.ABS_GLOBAL)#get the bounding box of each piece
		tilePosition = box.center #	want to get the distance to centre not  corner
		newLook = tilePosition - WhereAmIVect
		distancetoPiece = newLook.length()
		fadefactor = 1-(((distancetoPiece - minAlpha)/( maxDISTANCE-minAlpha) )* maxAlpha)
		fadefactorCLAMP = viz.clamp(fadefactor,minAlpha,maxAlpha )
		piece.alpha(fadefactorCLAMP)

vizact.ontimer(0.1,LandVisible) # fast speed 
############################
############################

###########################################
# A thing that prints out the position and rotation of the zep
def printPOSITION ():
	ZEPPOSITION = ZEP.getPosition()
	ZEPROTATION = ZEP.getEuler()
	CAVEPOS = cave_origin.getPosition()
	CAVEROT = cave_origin.getEuler()

	view = view = viz.MainView
	
	whereAmIx = view.getPosition()[0]
	whereAmIy = view.getPosition()[1]
	whereAmIz = view.getPosition()[2]
	
	ZEPPOSITIONx = ZEP.getPosition()[0]
	ZEPPOSITIONy = ZEP.getPosition()[1]
	ZEPPOSITIONz = ZEP.getPosition()[2]
	
	differencex = ZEPPOSITIONx -whereAmIx 
	differencey = ZEPPOSITIONy -whereAmIy 
	differencez = ZEPPOSITIONz -whereAmIz
	
	ICESHEET = (3872.9387207, 315.1769104, 83884.96875)
	
	
#######VectorLength is the distance from us to ZEP
	ZepVect = viz.Vector(ZEP.getPosition())
	WhereAmIVect = viz.Vector(view.getPosition())
	newLook = ZepVect - WhereAmIVect
	distance = newLook.length()
	
	ToIce = ICESHEET - WhereAmIVect
	distanceToIce = ToIce.length()
	
	
	#print "distanceTOZEP = "
	#print distance
	
	#print "Altitude = "
	#print whereAmIy

	#Send along position and rotation via OSC
	ZPOSmsg = OSCMessage("/ZEPPOSITION")
	ZPOSmsg.append(ZEPPOSITION)
	client.send(ZPOSmsg)

	ZROTmsg = OSCMessage("/ZEPROTATION")
	ZROTmsg.append(ZEPROTATION)
	client.send(ZROTmsg)
	
	POSmsg = OSCMessage("/CAVEPOS")
	POSmsg.append(CAVEPOS)
	client.send(POSmsg)

	ROTmsg = OSCMessage("/CAVEROT")
	ROTmsg.append(CAVEROT)
	client.send(ROTmsg)
	
	DistToZep = OSCMessage("/DistToZep")
	DistToZep.append(distance)
	client.send(DistToZep)
	
	DistToICESHEET = OSCMessage("/DistToIceSheet")
	DistToICESHEET.append(distanceToIce)
	client.send(DistToICESHEET)
	
#	print "DistToICESHEET = "
#	print distanceToIce
# Also Uncomment here to get position in the console & see below	
# Nb. set the number lower to print out the pos and rot more often
vizact.ontimer(1, printPOSITION)

#controls
WHEEL_DEAD_ZONE = 0.05
PEDAL_DEAD_ZONE = 0.15

#forward speed
MAX_SPEED = 3000.0
IDLE_SPEED = MAX_SPEED*0.1
ACCEL_FACTOR = MAX_SPEED/14 # seconds to max speed
BRAKE_FACTOR = MAX_SPEED/7 # seconds to stop
TO_IDLE_FACTOR = MAX_SPEED/30
blimp_speed = IDLE_SPEED

#climbing
CLIMB_ACCEL_RATE = 1.0
climb_speed = 0
CLIMB_DAMPING = 1
CLIMB_PITCH_FACTOR = 0.3
CLIMB_LOWER_LIMIT = -unit*0.05
CLIMB_UPPER_LIMIT = unit

#turning
TURN_ACCEL_RATE = 0.3
turn_speed = 0
TURN_DAMPING = 1
ROLL_FACTOR = 300.0

#autopilot to pos is a nice blank tile
AUTOPILOT_TO_POS = (4.5* unit, unit*0.01, 5.5*unit)

#autopilot
AUTOPILOT_WAIT_TIME = 180 #seconds
dead_control_time = 0
AUTOPILOT_WHEEL_TURN_AMOUNT = 0.1
AUTOPILOT_PEDAL_ACTIVATION = 0.3
AUTOPILOT_TURN_DEADZONE = 5
AUTOPILOT_CLIMB_DEADZONE = unit*0.001

def steeringWheel():
	#move the cave_origin around based on the steering wheel
	global SPEED_FACTOR
	global blimp_speed
	global climb_speed
	global turn_speed
	global dead_control_time
	
	elapsed = viz.elapsed()
	
	cave_pos = cave_origin.getPosition()
	cave_eul = cave_origin.getEuler()

	#get control values
	joy_pos = joy.getPosition()
	wheel_turn = joy_pos[0]
	pedal_actuation = joy_pos[1]
	left_finger_trigger = joy.isButtonDown(1)
	right_finger_trigger = joy.isButtonDown(2)
	
	#dead zones
	if abs(pedal_actuation) < PEDAL_DEAD_ZONE:
		pedal_actuation = 0
	if abs(wheel_turn) < WHEEL_DEAD_ZONE:
		wheel_turn = 0
		
	controls_dead = (not left_finger_trigger) and (not right_finger_trigger) and \
		(pedal_actuation == 0) and (wheel_turn == 0)
	
	if controls_dead:
		dead_control_time += elapsed
	else:
		dead_control_time = 0
	if dead_control_time >= AUTOPILOT_WAIT_TIME:
		#running on autopilot
		
		#elevation
		if abs(AUTOPILOT_TO_POS[1] - cave_pos[1]) > AUTOPILOT_CLIMB_DEADZONE:
			if cave_pos[1] < AUTOPILOT_TO_POS[1]:
				pedal_actuation = AUTOPILOT_PEDAL_ACTIVATION
			else:
				pedal_actuation = -AUTOPILOT_PEDAL_ACTIVATION
			
		#turning to centre, if near edge
		near_edge = cave_pos[0] < unit or cave_pos[0] > (columns - 2)*unit or \
			cave_pos[2] < unit or cave_pos[2] > (rows - 2)*unit
		
		if near_edge:
			#turn towards centre
			yaw = cave_eul[0]			
			goal_yaw = 180.0/(math.pi)*math.atan2(AUTOPILOT_TO_POS[0] - cave_pos[0], AUTOPILOT_TO_POS[2] - cave_pos[2])
			
			if abs(goal_yaw - yaw) > AUTOPILOT_TURN_DEADZONE:
				if yaw < goal_yaw:
					wheel_turn = AUTOPILOT_WHEEL_TURN_AMOUNT
				else:
					wheel_turn = -AUTOPILOT_WHEEL_TURN_AMOUNT
	
	#forward thrust
	if right_finger_trigger:
		blimp_speed = max(0, blimp_speed - BRAKE_FACTOR*elapsed)
	elif left_finger_trigger:
		blimp_speed = min(blimp_speed + ACCEL_FACTOR*elapsed, MAX_SPEED)
	else: 
		#no finger trigger touched, seek idle speed
		to_idle_amount = TO_IDLE_FACTOR*elapsed
		if abs(IDLE_SPEED - blimp_speed) < to_idle_amount:
			blimp_speed = IDLE_SPEED
		elif IDLE_SPEED > blimp_speed:
			blimp_speed += to_idle_amount
		else:
			blimp_speed -= to_idle_amount
		
	cave_origin.setPosition(0, 0, blimp_speed*elapsed, viz.REL_LOCAL) 
	
	
	#climb & elevation
	#height limits
	if cave_pos[1] < CLIMB_LOWER_LIMIT:
		pedal_actuation = +1
	elif cave_pos[1] > CLIMB_UPPER_LIMIT:
		pedal_actuation = -1
	
	climb_speed += CLIMB_ACCEL_RATE*elapsed*pedal_actuation
	climb_speed *= (1 - CLIMB_DAMPING*elapsed)
	cave_origin.setPosition(0, climb_speed, 0, viz.REL_LOCAL) 
	
	compass.setPosition(cave_origin.getPosition())
	
	#rotation
	# yaw, pitch, roll
	# yaw is controlled by steering
	# bank or roll happens when we're steering and moving fast
	# pitch happens when we're ascending or descending.
	
	turn_speed += TURN_ACCEL_RATE*elapsed*wheel_turn
	turn_speed *= (1 - TURN_DAMPING*elapsed)
	
	cave_origin.setEuler(turn_speed, 0, 0, viz.REL_LOCAL)
	eul = cave_origin.getEuler()
	
	#climbing pitch
	eul[1] = -climb_speed*CLIMB_PITCH_FACTOR
	
	#banking roll
	eul[2] = -turn_speed*blimp_speed/MAX_SPEED*ROLL_FACTOR
	
	cave_origin.setEuler(eul)
	
	#banking
	#    un-bank first
	#eul = viz.MainView.getEuler()
	#eul[2] = 0
	#viz.MainView.setEuler(eul, viz.HEAD_ORI, viz.ABS_GLOBAL)

#    turn
	#viz.MainView.setAxisAngle(0,1,0,turn_rate,viz.HEAD_ORI,viz.REL_LOCAL)
	#eul = viz.MainView.getEuler()
	
#    bank
	#eul[2] = -wheel_turn*10
	#viz.MainView.setEuler(eul, viz.HEAD_ORI, viz.ABS_GLOBAL)
	

######################
#unit = tile size
viz.fog(0.7*unit, 1.0*unit) #settings seem good
cave = vizcave.Cave()
cave.setFarPlane(0.95*unit)##needs the farplane to have compass
#cave.setNearPlane(0.1)
vizact.ontimer(0.0,artTrackerUpdate) #as fast as possible!
vizact.ontimer(0.0,steeringWheel)
setCave()
#######################

#set blimp to start in the middle of the map
cave_origin.setPosition(AUTOPILOT_TO_POS)

