import viz
import vizshape
import vizact
import random
import math

#copied code from cave
scaling = 5600
unit = 10 * scaling
rows = 9 #	horizontal
columns = 10
autopilot_origin = ( (rows/2 + 0.5)* unit, unit*0.01, (columns/2 + 0.5)*unit)		

SCALING = unit

random.seed()

###########################
# Add a zepplin model - you may have to set path to model
ZEP_MODEL = viz.addChild('Meshes/ZepZ.OSGB')

def getZep():
	ZEP = ZEP_MODEL.clone()
	
	# Add a propellor, spin it and position relative to Zepplin
	PROP = viz.addChild('Meshes/Prop.OSGB',parent=ZEP)
	PROP2 = viz.addChild('Meshes/Prop.OSGB',parent=ZEP)
	PROP3 = viz.addChild('Meshes/Prop.OSGB',parent=ZEP)
	PROP4 = viz.addChild('Meshes/Prop.OSGB',parent=ZEP)

	PROP.addAction( vizact.spin(0,0,1,-540) )
	PROP2.addAction( vizact.spin(0,0,1,510) )
	PROP3.addAction( vizact.spin(0,0,1,-545) )
	PROP4.addAction( vizact.spin(0,0,1,500) )

	PROP.setPosition([.0865,.0592,-0.1475])
	PROP2.setPosition([-.0865,.0592,-0.1475])
	PROP3.setPosition([.0836,.0589,-0.316])
	PROP4.setPosition([-.0836,.0589,-0.316])

	ZEP.setScale(1260,1260,1260)
	ZEP.alpha(.5)

	return ZEP
		
def getRandomPt():
#	a = random.randint(0,6*SCALING)
#	b = random.randint (0,(SCALING/2))
#	c = random.randint(0,6*SCALING)

	EXPAND = 0.1
	a = autopilot_origin[0] + random.randint(-unit*EXPAND, unit*EXPAND)
	b = autopilot_origin[1] + random.randint(-unit*EXPAND, unit*EXPAND)
	c = autopilot_origin[2] + random.randint(-unit*EXPAND, unit*EXPAND)
	
	return a,b,c
	
	
def setRandomPath(ZEP, start_pos = 0):
	#Generate random values for position 
	
	if start_pos == 0:
		x,y,z = getRandomPt()
	else:
		x,y,z = start_pos
	
	a,b,c = getRandomPt()

	q,w,e = getRandomPt()
	
	f,g,h = getRandomPt()

	i,j,k = getRandomPt()

	#Initialize an array of control points
	positions = [ [x,y,z], [a,b,c,], [q,w,e], [f,g,h], [i,j,k] ]
	print positions

	#Create an animation path
	path = viz.addAnimationPath()

	for x,pos in enumerate(positions):
		#Add a ball at each control point and make it
		#semi-transparent, so the user can see where the
		#control points are
		#b = viz.addChild('beachball.osgb',cache=viz.CACHE_CLONE)
		#b.setScale(10,10,10)
		#b.setPosition(pos)
		#b.alpha(0.2)
		#Add the control point to the animation path
		#at the new time
		path.addControlPoint(x+1,pos=pos)

	#Set the initial loop mode to circular
	path.setLoopMode(viz.CIRCULAR)

	#make it go in a bezier between points circle
	path.setTranslateMode(viz.CUBIC_BEZIER)

	#Automatically compute tangent vectors for cubic bezier translations
	path.computeTangents()

	#Automatically rotate the path
	path.setAutoRotate(viz.ON)

	#Link the ZEPPELIN to the path
	viz.link(path, ZEP)

	#Play the animation path
	path.play()

	#Set the animation path speed
	path.speed(.008)

	

zep_origin = (autopilot_origin[0], autopilot_origin[1], autopilot_origin[2] + unit*0.1)

for x in range(10):
	ZEP = getZep()
	setRandomPath(ZEP, zep_origin)

#this is the magic ZEP that gets its position date to the CAVe so we can get sound thingies
MAGIC = getZep()
setRandomPath(MAGIC, zep_origin)


##############LINK Viewpoint to Zepplin
#ZEPViewLink =  viz.link(ZEP, VIEW)
#ZEPViewLink.preTrans([0, 0, -202])#give it an offset to see the ZEP






