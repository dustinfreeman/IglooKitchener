﻿import time
import array
import socket
import random
import math

import cave_man

import vizjoy
joy = vizjoy.add()
#above will return the first detected joystick

#####################
import Zeppelin
from Logo import *
from Wind import *
	
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
			piece.setScale( scaling, scaling, scaling )
			
			curCol = curCol + 1
			if curCol == columns:
				curCol = 0
				curRow = curRow + 1
				
placePieces()

###############################
#gives readout of which piece you are over
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
		#piece.alpha(1.0) 
		
vizact.ontimer(0.1,LandVisible) 
############################

###########################################
# prints out the position and rotation of the zep
# also, sends periodic position data to OSC.

#Setup OSC
from OSC import OSCClient, OSCMessage 
#OSCHOST  = "172.16.101.174"

OSCHOST  = "localhost" 
client = OSCClient()
client.connect( (OSCHOST, 57120) )

def printPOSITION ():
	ZEPPOSITION = Zeppelin.MAGIC.getPosition()
	ZEPROTATION = (Zeppelin.MAGIC.getEuler()[0])/360.0 + 180.0 #normalized 0..1
	CAVEPOS = cave.cave_origin.getPosition()
	CAVEROT = cave.cave_origin.getEuler()

	view = view = viz.MainView	

	ICESHEET = [227750.359375, 2701.13916015625, 272510.34375]
	ABANDONED = [95974.7109375, 1244.484130859375, 323311.78125]
	GLACIER = (435393.03125, 13339.1962890625, 346158.5)
	
	TWINKLY =[254979.25, 7813.31591796875, 401055.78125]
	WHALE = [318613.375, 6294.86279296875, 249989.15625]
	WIRES = [518248.15625, 4830.55615234375, 85015.921875]
	
#######VectorLength is the distance from us to Zeppelin.MAGIC
	ZepVect = viz.Vector(Zeppelin.MAGIC.getPosition())
	WhereAmIVect = viz.Vector(view.getPosition())
	newLook = ZepVect - WhereAmIVect
	distance_to_zep = newLook.length()
	#scale across entire map
	distance_to_zep /= rows*unit
	#the magic zeppelin should only be visible within distance_to_zep < 0.1
	
	ToIce = ICESHEET - WhereAmIVect
	distanceToIce = ToIce.length()
	
	ToABA = ABANDONED - WhereAmIVect
	distanceToAban= ToABA.length()
	
	ToGLA = GLACIER - WhereAmIVect
	distanceToGlac = ToGLA.length()
	
	ToTWINKLY = TWINKLY - WhereAmIVect
	distanceToTWINKLY = ToTWINKLY.length()
	
	ToWHALE = WHALE - WhereAmIVect
	distanceToWHALE= ToWHALE.length()
	
	ToWIRES = WIRES - WhereAmIVect
	distanceToWIRES= ToWIRES.length()
	
	#print "distanceTOZEP = "
	#print distance
	#print "Altitude = "
	#print WhereAmIVect

	#Send along position and rotation via OSC
#	ZPOSmsg = OSCMessage("/ZEPPOSITION")
#	ZPOSmsg.append(ZEPPOSITION)
#	client.send(ZPOSmsg)

	ZROTmsg = OSCMessage("/ZEPROTATION")
	ZROTmsg.append(ZEPROTATION)
	client.send(ZROTmsg)
	
	POSmsg = OSCMessage("/CAVEPOS")
	POSmsg.append(CAVEPOS)
	client.send(POSmsg)

#	ROTmsg = OSCMessage("/CAVEROT")
#	ROTmsg.append(CAVEROT)
#	client.send(ROTmsg)
	
	#distance to zep IS normalized - everything else is not.
	DistToZep = OSCMessage("/DistToZep")
	DistToZep.append(distance_to_zep)
	client.send(DistToZep)
	
	DistToICESHEET = OSCMessage("/DistToIceSheet")
	DistToICESHEET.append(distanceToIce)
	client.send(DistToICESHEET)
	
	DistToABANDONED= OSCMessage("/DistToAbandoned")
	DistToABANDONED.append(distanceToAban)
	client.send(DistToABANDONED)
	
	DistToGLACIER = OSCMessage("/DistToGlacier")
	DistToGLACIER.append(distanceToGlac)
	client.send(DistToGLACIER)
	
	DistToWIRE = OSCMessage("/DistToWires")
	DistToWIRE.append(distanceToWIRES)
	client.send(DistToWIRE)
	
	DistToWHA = OSCMessage("/DistToWhale")
	DistToWHA.append(distanceToWHALE)
	client.send(DistToWHA)
	
	DistToTWINK = OSCMessage("/DistToTwinkly")
	DistToTWINK.append(distanceToTWINKLY)
	client.send(DistToTWINK)

	
	WindSpeed = OSCMessage("/WindSpeed")
	if IDLE_SPEED == 0:
		WindSpeed.append(0.0)
	else:
		WindSpeed.append(wind.wind_speed/(IDLE_SPEED*1.5))
	client.send(WindSpeed)
	
#	print "ICESHEET = "
#	print DistToICESHEET
#	
#	print "Abandoned = "
#	print DistToABANDONED
#	
#	print "Glacier = "
#	print DistToGLACIER
# Also Uncomment here to get position in the console & see below	
# Nb. set the number lower to print out the pos and rot more often
vizact.ontimer(1, printPOSITION)


#controls
WHEEL_DEAD_ZONE = 0.05
PEDAL_DEAD_ZONE = 0.15

#forward speed
MAX_SPEED = 3000.0
IDLE_SPEED = MAX_SPEED*0.1
ACCEL_FACTOR = MAX_SPEED/10.0 # seconds to max speed
BRAKE_FACTOR = MAX_SPEED/10.0 # seconds to stop
TO_IDLE_FACTOR = MAX_SPEED/30.0
blimp_speed = IDLE_SPEED

wind = Wind(MAX_WIND_SPEED = IDLE_SPEED*0.3)

#mouse-based speed control
SPEED_CONTROL_LEVER = False
SPEED_CONTOL_SCALE = 150.0
speed_control_lever = 0

#climbing
CLIMB_ACCEL_RATE = 2.0
climb_speed = 0
CLIMB_DAMPING = 1
CLIMB_PITCH_FACTOR = 3.0
CLIMB_LOWER_LIMIT = -unit
CLIMB_UPPER_LIMIT = unit

#mouse-based climbing control
CLIMB_CONTROL_LEVER = False
CLIMBING_CONTROL_SCALE = 150.0
climb_control_lever = 0

#turning
TURN_ACCEL_RATE = 30.0
turn_speed = 0
TURN_DAMPING = 1
ROLL_FACTOR = 1.0

#QUEUED TURNING - non-realistic wheel control
QUEUED_TURNING = True
turn_queue = 0
QUEUED_TURN_RATIO = 0.05
QUEUED_TURN_DEAD_ZONE = QUEUED_TURN_RATIO*2
QUEUED_TURN_DIRN = 1
QUEUED_TURN_MAX_RATE = 2.5
MAX_QUEUED_TURN_AMOUNT = QUEUED_TURN_MAX_RATE * 4.0 #the size of our queued turn buffer.

#autopilot to pos is a nice blank tile
def AUTOPILOT_TO_POS():
	return ( (rows/2 + 0.5)* unit, unit*0.01, (columns/2 + 0.5)*unit)

#autopilot
AUTOPILOT_WAIT_TIME = 90 #seconds
dead_control_time = AUTOPILOT_WAIT_TIME #start in autopilot
live_control_time = 0 #time someone has been flying it.
AUTOPILOT_WHEEL_TURN_AMOUNT = 0.3
AUTOPILOT_PEDAL_ACTIVATION = 0.3
AUTOPILOT_TURN_DEADZONE = 15
AUTOPILOT_CLIMB_DEADZONE = unit*0.001
VERBOSE_AUTOPILOT = False

FADE_TIME = 7.5
LOGO_DISTANCE = 400
LOGO_FADE_TO_SPOT = -1000

def FadeLogoCheck():	
	#when user starts flying, logo should fade and fly away
	# once autopilot starts, the logo should fade and fly in.
	
	if dead_control_time >= AUTOPILOT_WAIT_TIME:
		#autopilot
		time_over = dead_control_time - AUTOPILOT_WAIT_TIME
		time_over = min(time_over, FADE_TIME)
		
		fade_amount = time_over/FADE_TIME
		
		Logo.setPosition(0,0,fade_amount*(LOGO_DISTANCE - LOGO_FADE_TO_SPOT) + LOGO_FADE_TO_SPOT)				
		
	else: 
		#positioning logo fade back.
		
		fade_amount = live_control_time/FADE_TIME
		fade_amount = min(1, fade_amount)
		
		Logo.setPosition(0,0,(1.0 - fade_amount)*(LOGO_DISTANCE - LOGO_FADE_TO_SPOT) + LOGO_FADE_TO_SPOT)
	
		
def start_autopilot():	
	global dead_control_time
	
	print "start autopilot"
	dead_control_time = AUTOPILOT_WAIT_TIME
	
		
#set blimp to start in the middle of the map
def to_start_location():
	cave.cave_origin.setPosition(AUTOPILOT_TO_POS())
	cave.cave_origin.setEuler(35,0,0)
	
	start_autopilot()

def steeringWheel():
	#move the cave.cave_origin around based on the steering wheel
	global SPEED_FACTOR
	global blimp_speed
	global climb_speed
	global turn_speed
	
	global dead_control_time
	global live_control_time
	
	global turn_queue
	global climb_control_lever
	
	elapsed = viz.elapsed()
	
	cave_pos = cave.cave_origin.getPosition()
	cave_eul = cave.cave_origin.getEuler()

	# ---------------------------------
	#default control values
	wheel_turn = 0
	climb_actuation = 0
	gas = False
	brake = False

	#joystick control values
	joy_pos = joy.getPosition()
	#wheel_turn = joy_pos[0] #we put that slot in the wood for a reason.
	climb_actuation = joy_pos[1]
	gas = joy.isButtonDown(5)
	brake = joy.isButtonDown(6)
	#dead zones
	if abs(climb_actuation) < PEDAL_DEAD_ZONE:
		climb_actuation = 0
	if abs(wheel_turn) < WHEEL_DEAD_ZONE:
		wheel_turn = 0
		
	#keyboard controls
	if viz.key.isDown('a'):
		wheel_turn = -1
	if viz.key.isDown('d'):
		wheel_turn = +1
	if viz.key.isDown('w'):
		climb_actuation = +1
	if viz.key.isDown('s'):
		climb_actuation = -1
	if viz.key.isDown(viz.KEY_SHIFT_L):
		gas = True
	if viz.key.isDown(viz.KEY_CONTROL_L):
		brake = True
	
	if CLIMB_CONTROL_LEVER:
		climb_actuation += climb_control_lever/CLIMBING_CONTROL_SCALE
	
	throttle = 0
	if SPEED_CONTROL_LEVER:
		if speed_control_lever < 0:
			throttle += speed_control_lever/SPEED_CONTOL_SCALE
		else:
			throttle += speed_control_lever/SPEED_CONTOL_SCALE
	
	
	if QUEUED_TURNING:
		#turn queued turning into wheel_turn
		if abs(turn_queue) < QUEUED_TURN_DEAD_ZONE:
			turn_queue = 0
		if turn_queue != 0:
			wheel_turn += math.copysign(min(1, math.pow(abs(turn_queue/QUEUED_TURN_MAX_RATE), 0.5)), turn_queue)	
	
	# ---------------------------------
	#AUTOPILOT
	controls_dead = (not gas) and (not brake) and \
		(climb_actuation == 0) and (wheel_turn == 0)	
	
	if controls_dead:
		dead_control_time += elapsed
	else: #controls are live
		dead_control_time = 0
		
	if dead_control_time < AUTOPILOT_WAIT_TIME:
		# controls are "live"
		live_control_time += elapsed	
	else:
		#running on autopilot
		if VERBOSE_AUTOPILOT:
			print "autopilot at: " + str(cave_pos)
		
		live_control_time = 0
		
		#elevation
		if abs(AUTOPILOT_TO_POS()[1] - cave_pos[1]) > AUTOPILOT_CLIMB_DEADZONE:
			if cave_pos[1] < AUTOPILOT_TO_POS()[1]:
				climb_actuation = AUTOPILOT_PEDAL_ACTIVATION
			else:
				climb_actuation = -AUTOPILOT_PEDAL_ACTIVATION
			
		#turning to centre, if near edge
		near_edge = cave_pos[0] < unit*1.5 or cave_pos[0] > (columns - 2.5)*unit or \
			cave_pos[2] < unit*1.5 or cave_pos[2] > (rows - 2.5)*unit

		yaw = cave_eul[0]	
		goal_yaw = yaw
		
		if near_edge:
			#turn towards centre
			goal_yaw = 180.0/(math.pi)*math.atan2(AUTOPILOT_TO_POS()[0] - cave_pos[0], AUTOPILOT_TO_POS()[2] - cave_pos[2])
			
			if abs(goal_yaw - yaw) > AUTOPILOT_TURN_DEADZONE:
				# we opt to turn in just one direction consistently
				# this is to solve an odd edge case (jokes) ,
				# where goal_yaw alternates between 179 and -179 degrees and
				# the blimp isn't able to chase it down before it goes
				# out of bounds.
				wheel_turn = AUTOPILOT_WHEEL_TURN_AMOUNT
				
#				if yaw < goal_yaw:
#					wheel_turn = AUTOPILOT_WHEEL_TURN_AMOUNT
#				else:
#					wheel_turn = -AUTOPILOT_WHEEL_TURN_AMOUNT
			
		if VERBOSE_AUTOPILOT:
			print "\t yaw: " + str(yaw) + " goal yaw: " + str(goal_yaw) + " " ,
					
		if VERBOSE_AUTOPILOT:
			print ""
			
	# ---------------------------------
	#forward thrust
	thrust_accel = 0
	if gas and not brake:
		thrust_accel += ACCEL_FACTOR*elapsed
		GasOn = OSCMessage("/GasOn")
		client.send(GasOn)
	else:
		GasOff = OSCMessage("/GasOff") 
		client.send(GasOff)
	if brake:
		thrust_accel -= BRAKE_FACTOR*elapsed
		BrakeOn = OSCMessage("/BrakeOn")
		client.send(BrakeOn)
	else:
		BrakeOff = OSCMessage("/BrakeOff") 
		client.send(BrakeOff)
	if not gas and not brake: 
		#no finger trigger touched, seek idle speed
		to_idle_amount = TO_IDLE_FACTOR*elapsed
		
		if not SPEED_CONTROL_LEVER and abs(IDLE_SPEED - blimp_speed) > to_idle_amount:
			if IDLE_SPEED > blimp_speed:
				thrust_accel += to_idle_amount
			else:
				thrust_accel -= to_idle_amount
		
	if SPEED_CONTROL_LEVER:
		if throttle > 0:
			thrust_accel += throttle*ACCEL_FACTOR*elapsed
		else: #throttle < 0
			thrust_accel += throttle*BRAKE_FACTOR*elapsed

	blimp_speed += thrust_accel
	#bounding
	blimp_speed = max(0, blimp_speed)
	blimp_speed = min(MAX_SPEED, blimp_speed)
	
	#print "throttle " + str(throttle) + " thrust_accel " + str(thrust_accel) + " blimp_speed " + str(blimp_speed)
	cave.cave_origin.setPosition(0, 0, blimp_speed*elapsed, viz.REL_LOCAL) 
	
	#wind
	#adjust max wind speed based on height
	wind.MAX_WIND_SPEED = max(IDLE_SPEED*1.5*(cave.cave_origin.getPosition()[1])/unit, 0) + IDLE_SPEED*0.3
	wind.update(elapsed)
	cave.cave_origin.setPosition(wind.vx, wind.vy, wind.vz, viz.REL_GLOBAL)
	
	# ---------------------------------
	#climb & elevation
	#height limits
	if cave_pos[1] < CLIMB_LOWER_LIMIT:
		climb_actuation = +1
	elif cave_pos[1] > CLIMB_UPPER_LIMIT:
		climb_actuation = -1
	
	climb_speed += CLIMB_ACCEL_RATE*elapsed*climb_actuation
	climb_speed *= (1 - CLIMB_DAMPING*elapsed)
	cave.cave_origin.setPosition(0, climb_speed, 0, viz.REL_LOCAL) 

	
	# ---------------------------------
	#rotation
	# yaw, pitch, roll
	# yaw is controlled by steering
	# bank or roll happens when we're steering and moving fast
	# pitch happens when we're ascending or descending.
	
	turn_speed += TURN_ACCEL_RATE*elapsed*wheel_turn
	turn_speed *= (1 - TURN_DAMPING*elapsed)
	
	#yawing
	turn_amount = turn_speed*elapsed
	if QUEUED_TURNING and turn_queue != 0:
		turn_queue -= turn_amount
		if turn_queue != 0:
			#print "turn_queue: " + str(turn_queue)
			pass
	cave.cave_origin.setEuler(turn_amount, 0, 0, viz.REL_LOCAL)
	cave_eul = cave.cave_origin.getEuler()
	
	#climbing pitch
	cave_eul[1] = -climb_speed*CLIMB_PITCH_FACTOR
	
	#banking roll
	cave_eul[2] = -turn_speed*math.sqrt(blimp_speed/MAX_SPEED)*ROLL_FACTOR
	
	cave.cave_origin.setEuler(cave_eul)
	
	#indicators & other UI
	
	#set it so compass does not yaw
	compass.setEuler(-cave_eul[0], 0, 0, )
	turn_queue_compass.setEuler(-cave_eul[0] + turn_queue, 0, 0)
	
	windspeed_indicator.setEuler(-cave_eul[0] + wind.angle*2*math.pi, 0, 0)
	wind_scale = wind.wind_speed/(IDLE_SPEED*0.3)
	windspeed_indicator.setScale(1,1,wind_scale)
	
	# ---------------------------------
	#safety bounds check for the entire map.
	cave_pos = cave.cave_origin.getPosition()
	if cave_pos[0] < -unit*0.5 or cave_pos[0] > unit*(columns - 1 + 0.5) or\
		cave_pos[1] < -unit*0.5 or cave_pos[1] > unit*1.0 or\
		cave_pos[2] < -unit*0.5 or cave_pos[2] > unit*(rows - 1  + 0.5):
		print "out of bounds reset"
		to_start_location()


###############################
breath_time = 0
BREATH_DURATION = 10.0
BREATH_AMPLITUDE = 0.1

BREATHING = False

def breathe():
	#makes the pieces breathe
	if not BREATHING:
		return
	
	global breath_time
	global BREATH_DURATION
	global BREATH_AMPLITUDE
	
	elapsed = viz.elapsed()
	breath_time += elapsed
	
	#print ("breathing: " + str(vertical_scale))
	
	piece_count = 0
	for piece in PIECES:
		#per-piece phasing
		piece_phase = 0 # 1 == 0
		piece_phase = piece_count/5.0
		piece_count += 1
		
		vertical_scale = scaling + BREATH_AMPLITUDE*scaling*math.sin(((breath_time + piece_phase)/BREATH_DURATION)*2*math.pi)
		
		curr_scale = piece.getScale()
		curr_scale[1] = vertical_scale
		piece.setScale(curr_scale)

######################
#Piece sliding motion

#set up secondary pieces
#TODO: override LandVisible() calls to alpha

#looping call for sliding motion

#control calls

######################
#Turn queueing,
# i.e. bizarro mouse wheel steering wheel behaviour
def mouseWheel(direction):
	#print "mouseWheel: " + str(direction)
	global turn_queue
	turn_queue += QUEUED_TURN_DIRN*QUEUED_TURN_RATIO*direction
	
	if abs(turn_queue) > MAX_QUEUED_TURN_AMOUNT:
		turn_queue = math.copysign(MAX_QUEUED_TURN_AMOUNT, turn_queue)
		
	#print turn_queue
	
viz.callback(viz.MOUSEWHEEL_EVENT, mouseWheel) 

def onMouseMove(e): 
#    print e.x, 'is absolute x.' 
#    print e.y, 'is absolute y.' 
#    print e.dx, 'is the relative change in x.' 
#    print e.dy, 'is the relative change y.' 

	global climb_control_lever
	if CLIMB_CONTROL_LEVER:
		climb_control_lever += e.dy


	global speed_control_lever
	if SPEED_CONTROL_LEVER:
		speed_control_lever += e.dx

viz.callback(viz.MOUSE_MOVE_EVENT,onMouseMove)

#click to reset positions
def onMouseDown(button): 
	global turn_queue
	global climb_control_lever
	global speed_control_lever
	
	if button == viz.MOUSEBUTTON_LEFT: 
		turn_queue = 0
		climb_control_lever = 0
		speed_control_lever = 0
	
		
viz.callback(viz.MOUSEDOWN_EVENT,onMouseDown) 

######################

def onKeyDown(key): 
	
	if key == 'q':
		start_autopilot()
		
	if key == 'r': 
		to_start_location()


viz.callback(viz.KEYDOWN_EVENT,onKeyDown)


######################
#unit = tile size
cave = cave_man.Cave()
cave.cave.setFarPlane(0.95*unit) #needs the farplane to see close objects?
viz.fog(0.7*unit, 1.0*unit) #settings seem goodcave
cave.setCave()

#setting up objects.
Logo.setParent(cave.cave_origin)
Logo.setPosition(0,0,LOGO_DISTANCE)
vizact.ontimer(0.0,FadeLogoCheck)

compass = viz.addChild('Meshes/arrow.osgb')
compass.color(0.2,0.8,0.8)
compass.setParent(cave.cave_origin)
compass.setPosition(0, -5, 10)
compass.setScale(6, 6, 6)

turn_queue_compass = compass.copy()
turn_queue_compass.color(0.8, 0.2, 0.2)
turn_queue_compass.setParent(cave.cave_origin)
turn_queue_compass.setPosition(0, -5.5, 10)
turn_queue_compass.setScale(6, 6, 6)
turn_queue_compass.alpha(0)

windspeed_indicator = vizshape.addArrow(10000)
windspeed_indicator.setParent(cave.cave_origin)
windspeed_indicator.setPosition([0.0, -2800.0, 17000.0])
windspeed_indicator.color(254, 97, 52)
windspeed_indicator.alpha(0)

######################
#movement with art tracker.
vizact.ontimer(0.0,cave.viewTrackerUpdate)

#our steering controls, and assorted UI stuff
vizact.ontimer(0.0,steeringWheel)

#landscape effects
vizact.ontimer(0.03,breathe)

#######################
# start it all!
to_start_location()