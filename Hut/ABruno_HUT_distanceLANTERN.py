import viz
import vizcave
import viztracker
import vizact
import time
import array
import artTracker
import random
import math
import vizmat
import vizshape

#import hut
#from hut import hut



#lantern_light = viz.addChild('Pyramid.OSGB')
#lantern_light.alpha(0.5)


hut = viz.addChild('HutTexturedWireversion.OSGB')
hut.setPosition( 0 , 0, 1.5)
hut.setEuler( [ 90, 0, 0 ] )
hut.setScale( 0.5, 0.5, 0.5)

lantern_light = viz.addChild('SphereOfDarkness.OSGB')



#lantern_light = vizshape.addCube(size=1.0)
#lantern_light = vizshape.addPyramid(base=1.0,1.0,height=1.0,axis=vizshape.AXIS_Y,splitFaces=False)

viz.go(viz.FULLSCREEN |viz.QUAD_BUFFER)
viz.window.setFullscreen(1)

iWantACompass = True

if iWantACompass:
	compass = viz.addChild('arrow.osgb')
	

#################################
#cave settings
height = 3.049
width = 5.638
depth = 3.049

#origional settings
#height = 3.049
#width = 5.638
#depth = 3.049


blendVertical=0.192
blendHorizontal=0.234

#origional settings
#blendVertical=0.19
#blendHorizontal=0.222
##################################



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

cave = vizcave.Cave()

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


#def trackingEnable():
#	artTracker.enable
#	
#LANTERN_OFFSET = (0.0,0,1.5)for spehere of darkness
LANTERN_OFFSET = (0.0,-1.0,1.5)#for labntern

def artTrackerUpdate():
	
	global counter, cave_origin,arrow,blinderbox,arrow1,arrow2,arrow3, blinderbox
	speed = 100
	viewTracker.setPosition(artTracker.x,artTracker.y,artTracker.z+depth/2)
	viewTracker.setEuler(artTracker.yaw,artTracker.pitch,artTracker.roll)
	
	
	cave_origin.setPosition(artTracker.jy*artTracker.x2*speed,artTracker.jy*artTracker.y2*speed,artTracker.jy*artTracker.z2*speed,viz.REL_LOCAL)
	cave_origin.setEuler(1*artTracker.jx,0,0,viz.REL_LOCAL)
	
	
	lantern_light.setPosition(artTracker.lantern.x + LANTERN_OFFSET[0], artTracker.lantern.y  + LANTERN_OFFSET[1], artTracker.lantern.z + LANTERN_OFFSET[2])
	lantern_light.setEuler(artTracker.lantern.yaw, artTracker.lantern.pitch, artTracker.lantern.roll)
	
	if iWantACompass:
		compass.setPosition(cave_origin.getPosition())
		

vizact.ontimer(0.0,artTrackerUpdate) #as fast as possible!
#cave.drawWalls()
global angle
angle = 0

#def printCAVELocation():
#	print cave_origin.getPosition()
#	print cave_origin.getEuler()
	
	
	#this gets the distance from player view (view) and then sets the alpha according to distace 
#problem is that the distance to pieces seems to be measured from the piece corner not centre


############################
############################
#this thing makes the tiles fade over distance

maxDISTANCE = 1	# smaller value means faded sooner
minAlpha = 0.0		# MIN brightness
maxAlpha = 0.6 		# MAX brightness

def LandVisible():
	view = view = viz.MainView
	WhereAmIVect = viz.Vector(view.getPosition())
	box = hut.getBoundingBox(mode = viz.ABS_GLOBAL)#get the bounding box of each piece
	tilePosition = box.center #	want to get the distance to centre not  corner
	newLook = tilePosition - WhereAmIVect
	distancetoPiece = newLook.length()
	fadefactor = 1-(((distancetoPiece - minAlpha)/( maxDISTANCE-minAlpha) )* maxAlpha)
	fadefactor = max(0, fadefactor)
	#print "distancetoPiece ="
	#print distancetoPiece
	#print fadefactor
	hut.alpha(fadefactor)
	
#vizact.ontimer(0.1,LandVisible) # fast speed 
############################
############################


