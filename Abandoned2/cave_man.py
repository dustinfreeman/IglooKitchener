#all the core code associated with the cave in Communitech
import viz
import vizcave
import viztracker
import vizact
import artTracker

class Cave:
	
	def __init__(self):

		viz.go(viz.FULLSCREEN |viz.QUAD_BUFFER)
		viz.window.setFullscreen(1)

		#####################
		#setup CAVE
		polyMode = viz.POLY_WIRE
		#viz.setFarPlane(1)
		#viz.setMultiSample(4) #didn't observe a difference in landscapes with anti-aliasing.
		viz.window.setPolyMode(viz.POLY_WIRE)
		viz.vsync(viz.ON)#this may increase frame rate but may get tears
		viz.ipd(0.2) #20 cm apart eyes seemed right for our scaling.

		self.cave = vizcave.Cave()
		#cave.setNearPlane(0.1)

	#####################
	def setCave(self):
		global height, width, depth
		
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

		self.cave.addWall(FrontWall, mask=viz.MASTER)
		self.cave.addWall(Ch1, mask=viz.CLIENT1)
		self.cave.addWall(Ch2, mask=viz.CLIENT2)
		self.cave.addWall(Ch3, mask=viz.CLIENT3)
		self.cave.addWall(Ch4, mask=viz.CLIENT4)
		self.cave.addWall(Ch5, mask=viz.CLIENT5)
		self.cave.addWall(Ch6, mask=viz.CLIENT6)
		self.cave.addWall(Ch7, mask=viz.CLIENT7)
		self.cave.addWall(Ch8, mask=viz.CLIENT8)
		self.cave.addWall(Ch9, mask=viz.CLIENT9)
		self.cave.addWall(Ch10, mask=1024)
		self.cave.addWall(Ch11, mask=2048)
		self.cave.addWall(Ch12, mask=4096)

		global viewTracker
		#global cave_origin, counter
		magicCarpet = viztracker.KeyboardMouse6DOF() #not sure what this is
		viewTracker = viztracker.KeyboardMouse6DOF() #the control that comes with the cave.
		viewTracker.setPosition(0,0,0)
		self.cave.setTracker(pos=viewTracker)
		
		self.cave_origin = vizcave.CaveView(viewTracker)
		view = viz.MainView
		counter = 0

	def viewTrackerUpdate(self):
		#viewTracker constants
		speed = 2000000 # move speed
		rot_speed = 17 # rotate speed
		
		
	#	print viz.elapsed() #about 0.003 @ 30 fps
		elapsed = viz.elapsed()
		fps_speed = elapsed*speed
		fps_rot_speed = elapsed*rot_speed
		
		viewTracker.setPosition(artTracker.x,artTracker.y,artTracker.z+depth/2)
		viewTracker.setEuler(artTracker.yaw,artTracker.pitch,artTracker.roll)
		
		self.cave_origin.setPosition(artTracker.jy*artTracker.x2*fps_speed, artTracker.jy*artTracker.y2*fps_speed, artTracker.jy*artTracker.z2*fps_speed,viz.REL_LOCAL)
		self.cave_origin.setEuler(fps_rot_speed*artTracker.jx,0.0,0.0,viz.REL_LOCAL)	 

