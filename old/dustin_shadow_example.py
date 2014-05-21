import viz
from ShadowTheatre import *

ground = viz.add('tut_ground.wrl')
ground2 = viz.add('tut_ground.wrl', pos = (0,0,8), euler = (0,270,0) )

#Add avatar
avatar = viz.add('vcc_female.cfg',pos=(0,0,6),euler=(180,0,0))
avatar.state(5)

SHADOW_RES = 256

#Postion of shadow projector
SHADOW_POS = [0,2,3]
SHADOW_EULER = [0,25,0]

#Controls size of orthographic shadow projector
#Large values mean larger area is covered, but resolution will be diluted
SHADOW_AREA = [5,5]
shadow = ShadowProjector(size=SHADOW_RES,pos=SHADOW_POS,area=SHADOW_AREA, euler = SHADOW_EULER )

#Add avatar as a shadow caster
shadow.addCaster(avatar)

#Add ground as shadow receiver
shadow.addReceiver(ground)
shadow.addReceiver(ground2)


def update_shadows():
	
	#moving shadow in x
	SHADOW_POS[0] = -1 + (2.0/100)*(frameCount%100)
	#SHADOW_POS[2] = 2 + (2.0/100)*(frameCount%100)

	shadow.setPosition(SHADOW_POS)
	
frameCount = 0
def frame_tick():
	global frameCount
	frameCount+=1
	
	update_shadows()

#runs each frame
vizact.ontimer(0, frame_tick)

viz.go()