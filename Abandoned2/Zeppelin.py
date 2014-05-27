import viz
import vizshape
import vizact
import random
import math

SCALING = 56000 #Default Scaling (5600 is good)
SMALLSCALE = SCALING/25

###########################
# Add a zepplin model - you may have to set path to model


def setUpZEP(ZEP):	
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

	##########################################
	###################################
	##########################################
	#Generate random values for position 
	x = random.randint(0,6*SCALING)
	y = random.randint(0,(SCALING/2))
	z = random.randint(0,6*SCALING)
	
	a = random.randint(0,6*SCALING)
	b = random.randint (0,(SCALING/2))
	c = random.randint(0,6*SCALING)

	q = random.randint(0,6*SCALING)
	w = random.randint(0,(SCALING/2))
	e = random.randint (0,6*SCALING)
	
	f = random.randint(0,6*SCALING)
	g = random.randint(0,(SCALING/2))
	h = random.randint(0,6*SCALING)

	i = random.randint(0,6*SCALING)
	j = random.randint(0,(SCALING/2))
	k = random.randint(0,6*SCALING)

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


	
	
##############LINK Viewpoint to Zepplin
#ZEPViewLink =  viz.link(ZEP, VIEW)
#ZEPViewLink.preTrans([0, 0, -202])#give it an offset to see the ZEP

for x in range(0,10):
	ZEP = viz.addChild('Meshes/ZepZ.OSGB')
	ZEP.setScale(1260,1260,1260)
	ZEP.alpha(.5)
	setUpZEP(ZEP)


#this is the magic ZEP that gets its position date to the CAVe so we can get sound thingies
MAGIC_ZEP = viz.addChild('Meshes/ZepZ.OSGB')
MAGIC_ZEP.setScale(1260,1260,1260)
MAGIC_ZEP.alpha(.5)
setUpZEP(MAGIC_ZEP)






