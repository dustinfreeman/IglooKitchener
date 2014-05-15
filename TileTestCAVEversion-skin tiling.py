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
rot_speed = 0.1 # rotate speed

speed *= 5 #MUST GO FASTER
rot_speed *= 5

compass = viz.addChild('Meshes/arrow.osgb')
compass.color(0.2,0.8,0.8)

#####################
#Setup OSC
from OSC import OSCClient, OSCMessage 
#OSCHOST  = "172.16.101.174"
OSCHOST  = "localhost" # On windows supercollider, use port 57121 instead of 57120
client = OSCClient()
client.connect( (OSCHOST, 57120) )
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
	
def flip():
	# flips all the pieces. Not useful.

	for piece in PIECES:
		curr_scale = piece.getScale()
		piece.setScale(-curr_scale[0], curr_scale[1], curr_scale[2])
	#print "done flip!"
	
def artTrackerUpdate():
	viewTracker.setPosition(artTracker.x,artTracker.y,artTracker.z+depth/2)
	viewTracker.setEuler(artTracker.yaw,artTracker.pitch,artTracker.roll)
	cave_origin.setPosition(artTracker.jy*artTracker.x2*speed,artTracker.jy*artTracker.y2*speed,artTracker.jy*artTracker.z2*speed,viz.REL_LOCAL)
	cave_origin.setEuler(rot_speed*artTracker.jx,0,0,viz.REL_LOCAL)	 
	compass.setPosition(cave_origin.getPosition())
	
	pos = cave_origin.getPosition()
	eul = cave_origin.getEuler()
	#check out of bounds
	
# def updateVisibilityHive():
# 	updateVisibility(cave_origin.getPosition())
# 	pass
	
####################

PIECESNAMES=[
#groups of rows
'TerrainTestsSetof8/C1.OSGB',
'TerrainTestsSetof8/C2.OSGB',
'TerrainTestsSetof8/C3.OSGB',
'TerrainTestsSetof8/C4.OSGB',
'TerrainTestsSetof8/C5.OSGB',
'TerrainTestsSetof8/C6.OSGB',
'TerrainTestsSetof8/C7.OSGB',
'TerrainTestsSetof8/C8.OSGB',

'TerrainTestsSetof8/B13.OSGB',
'TerrainTestsSetof8/B14.OSGB',
'TerrainTestsSetof8/B15.OSGB',
'TerrainTestsSetof8/B16.OSGB',
'TerrainTestsSetof8/M.OSGB',
'TerrainTestsSetof8/N.OSGB',
'TerrainTestsSetof8/O.OSGB',
'TerrainTestsSetof8/P.OSGB',

'TerrainTestsSetof8/B9.OSGB',
'TerrainTestsSetof8/B10.OSGB',
'TerrainTestsSetof8/B11.OSGB',
'TerrainTestsSetof8/B12.OSGB',
'TerrainTestsSetof8/I.OSGB',
'TerrainTestsSetof8/J.OSGB',
'TerrainTestsSetof8/K.OSGB',
'TerrainTestsSetof8/L.OSGB',

'TerrainTestsSetof8/B5.OSGB',
'TerrainTestsSetof8/B6.OSGB',
'TerrainTestsSetof8/B7.OSGB',
'TerrainTestsSetof8/B8.OSGB',
'TerrainTestsSetof8/E.OSGB',
'TerrainTestsSetof8/F.OSGB',
'TerrainTestsSetof8/G.OSGB',
'TerrainTestsSetof8/H.OSGB',

'TerrainTestsSetof8/B1.OSGB',
'TerrainTestsSetof8/B2.OSGB',
'TerrainTestsSetof8/B3.OSGB',
'TerrainTestsSetof8/B4.OSGB',
'TerrainTestsSetof8/A.OSGB',
'TerrainTestsSetof8/B.OSGB',
'TerrainTestsSetof8/C.OSGB',
'TerrainTestsSetof8/D.OSGB',

'TerrainTestsSetof8/G00.OSGB',
'TerrainTestsSetof8/G10.OSGB',
'TerrainTestsSetof8/G20.OSGB',
'TerrainTestsSetof8/G30.OSGB',
'TerrainTestsSetof8/S01.OSGB',
'TerrainTestsSetof8/S02.OSGB',
'TerrainTestsSetof8/S03.OSGB',
'TerrainTestsSetof8/S04.OSGB',

'TerrainTestsSetof8/G01.OSGB',
'TerrainTestsSetof8/G11.OSGB',
'TerrainTestsSetof8/G21.OSGB',
'TerrainTestsSetof8/G31.OSGB',
'TerrainTestsSetof8/S05.OSGB',
'TerrainTestsSetof8/S06.OSGB',
'TerrainTestsSetof8/S07.OSGB',
'TerrainTestsSetof8/S08.OSGB',
]

################################
PIECES = []
scaling = 5600
unit = 10 * scaling
rows = 7 #	horizontal
columns = 8

def getPieceName(column, row):
	#print("index " + str(row*columns + column))
	index = row*columns + column
	if (index < 0 or index > len(PIECESNAMES) -1):
		return "out of range"
	return PIECESNAMES[index]

def getPiece(column, row):
	#print ("index " + str(row*columns + column));
	return PIECES[row*columns + column]

def placePieces():	
	curRow = 0
	curCol = 0
	for Name in PIECESNAMES:
		PIECES.append(viz.addChild(Name))
	
	#old piece placement code
#	for piece in PIECES:
#		piece.setPosition(curCol * unit, 0 ,curRow * unit)
#		piece.color(0.2,0.8,0.8)
#		curCol = curCol + 1
#		if curCol == columns:
#			curCol = 0
#			curRow = curRow + 1
			
	#using getPiece refactor
	for row in range(rows):
		for column in range(columns):
			#print (str(column) + "," + str(row))
			piece = getPiece(column, row)		
			piece.setPosition(column * unit, 0 , row * unit)
			piece.setScale( scaling, scaling, scaling )
			piece.color(0.2,0.8,0.8)

def placePieceSkin(num_tiles_border = 1):
	#places a number of tiles around the edge of a single grid, flipped so the boundaries are smooth

	SKIN_COLOR = (0.8, 0.2, 0.2)

	#along x = 0 (top row)
	#print ("ADDING TOP ROW")
	for row in range(num_tiles_border):
		for column in range(columns):
			piece_name = getPieceName(column, row)
			#print "placing piece skin..." + piece_name + " at " + str(column) + "," + str(-row)
			piece = viz.addChild(piece_name)
			PIECES.append(piece)
			piece.color(SKIN_COLOR)
			piece.setPosition(column * unit, 0, (-1 -row)*unit)
			piece.setScale(scaling, scaling, -scaling)
	
	#along z = 0 (top column)
	#print ("ADDING TOP COLUMN")
	for column in range(num_tiles_border):
		for row in range(rows):
			piece_name = getPieceName(column, row)
			#print "placing piece skin..." + piece_name + " at " + str(-column) + "," + str(row)
			piece = viz.addChild(piece_name)
			PIECES.append(piece)
			piece.color(SKIN_COLOR)
			piece.setPosition((-1 - column) * unit, 0, row*unit)
			piece.setScale(-scaling, scaling, scaling)

	#diagonal from x,z = 0,0
	#cheat and just add corner one (assuming num_tiles_border == 1)
	corner_name = getPieceName(0,0)
	corner_piece = viz.addChild(corner_name)
	PIECES.append(corner_piece)
	corner_piece.color(SKIN_COLOR)
	corner_piece.setPosition(-1*unit, 0, -1*unit)
	corner_piece.setScale(-scaling, scaling, -scaling)
	
	#along x = columns (bottom row)
	#print ("ADDING BOTTOM ROW")
	for row in range(rows - 1, rows - 1 - num_tiles_border, - 1):
		for column in range(columns):
			piece_name = getPieceName(column, row)
			#print "placing piece skin..." + piece_name #+ " at " + str(column) + "," + str(-row)
			piece = viz.addChild(piece_name)
			PIECES.append(piece)
			piece.color(SKIN_COLOR)
			piece.setPosition(column * unit, 0, (rows - 1 + (rows - row))*unit)
			#print str(piece.getPosition()[0]/unit) + "," + str(piece.getPosition()[2]/unit)
			piece.setScale(scaling, scaling, -scaling)
	
	#along z = rows (bottom column)
	for column in range(columns - 1, columns - 1 - num_tiles_border, -1):
		for row in range(rows):
			piece_name = getPieceName(column, row)
			#print "placing piece skin..." + piece_name + " at " + str(-column) + "," + str(row)
			piece = viz.addChild(piece_name)
			PIECES.append(piece)
			piece.color(SKIN_COLOR)
			piece.setPosition((columns - 1 + (columns - column)) * unit, 0, row*unit)
			piece.setScale(-scaling, scaling, scaling)
	
	#(columns, 0) corner
	corner_name = getPieceName(columns - 1,0)
	corner_piece = viz.addChild(corner_name)
	PIECES.append(corner_piece)
	corner_piece.color(SKIN_COLOR)
	corner_piece.setPosition((columns - 1 + 1)*unit, 0, -1*unit)
	corner_piece.setScale(-scaling, scaling, -scaling)
	
	#(0, rows) corner
	corner_name = getPieceName(0, rows - 1)
	corner_piece = viz.addChild(corner_name)
	PIECES.append(corner_piece)
	corner_piece.color(SKIN_COLOR)
	corner_piece.setPosition(-1*unit, 0, (rows - 1 + 1)*unit)
	corner_piece.setScale(-scaling, scaling, -scaling)

	#(columns, rows) corner
	corner_name = getPieceName(columns - 1, rows - 1)
	corner_piece = viz.addChild(corner_name)
	PIECES.append(corner_piece)
	corner_piece.color(SKIN_COLOR)
	corner_piece.setPosition((columns - 1 + 1)*unit, 0, (rows - 1 + 1)*unit)
	corner_piece.setScale(-scaling, scaling, -scaling)


				
placePieces()
placePieceSkin(1) #should be the number of tiles your sight has


###############################
#gives readout of which pice you are over
def checkProx(player, piece):
	distance = math.sqrt((player[0] - piece[0])**2 + (player[2] - piece[2])**2)
	return distance
		
LastName = ''	
def IAmHere(print_out = False):
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
			
	if currentPiece >= len(PIECESNAMES):
		return #out of bounds.
			
	if PIECESNAMES[currentPiece]!= LastName:
		LastName = PIECES[currentPiece]
#		uncomment print line below to get a readout of what pice you are over
		if (print_out):
			print PIECESNAMES[currentPiece]	

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

######################
cave = vizcave.Cave()
cave.setFarPlane(11*scaling)
cave.setNearPlane(1)
vizact.ontimer(0.0,artTrackerUpdate) #as fast as possible!

setCave()
#######################


#Dustin mucking around below
cave_origin.setPosition(0,unit/3.0,0);
#cave_origin.setPosition((columns - 1)*unit, unit/3.0,(rows - 1)*unit);







