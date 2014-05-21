import viz
viz.go()

#Add ground model
ground = viz.add('tut_ground.wrl')

#Add avatar
avatar = viz.add('vcc_female.cfg',pos=(0,0,8),euler=(180,0,0))
avatar.state(5)

#Shadow resolution (power of two)
#Higher values mean sharper shadows, but take more texture memory
SHADOW_RES = 256

#Postion of shadow projector
SHADOW_POS = [0,10,8]

#Controls size of orthographic shadow projector
#Large values mean larger area is covered, but resolution will be diluted
SHADOW_AREA = [5,5]

#Create shadow projector
import Shadow
shadow = Shadow.ShadowProjector(size=SHADOW_RES,pos=SHADOW_POS,area=SHADOW_AREA)

#Add avatar as a shadow caster
shadow.addCaster(avatar)

#Add ground as shadow receiver
shadow.addReceiver(ground)