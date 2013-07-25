import viz
import numpy as np
import time 
import pickle

import Shadow

from openni import *
ctx = Context()
ctx.init()

# Create a depth generator
depth = DepthGenerator()
depth.create(ctx)

# Set it to VGA maps at 30 FPS
depth.set_resolution_preset(RES_VGA)
depth.fps = 30

# Start generating
ctx.start_generating_all()

#load scene
ground = viz.add('tut_ground.wrl')
ground2 = viz.add('tut_ground.wrl', pos = (0,0,5), euler = (0,270,0) )
#Create shadow projector
#Shadow resolution (power of two)
#Higher values mean sharper shadows, but take more texture memory
SHADOW_RES = 256

#Postion of shadow projector
SHADOW_POS = [0,3,2]

#Controls size of orthographic shadow projector
#Large values mean larger area is covered, but resolution will be diluted
SHADOW_AREA = [5,5]
shadow = Shadow.ShadowProjector(size=SHADOW_RES,pos=SHADOW_POS,area=SHADOW_AREA, euler = [0,10,0] )
#Add ground as shadow receiver
shadow.addReceiver(ground)
shadow.addReceiver(ground2)
	
def start_avatar():
	
	avatar = viz.add('vcc_female.cfg', pos = (0,0,4), euler=(180,0,0))
	avatar.state(5)

	#Add avatar as a shadow caster
	shadow.addCaster(avatar)

#start_avatar()

class DepthFrame:
	def __init__(self,depthMap):
		self.map = depthMap
		self.time = time.clock()

class DepthSequence:
	#intended to be a saveable sequence of PyOpenNI's openni.DepthMap
	
	def __init__(self):
		self.sequence = []


	

BACKGROUND_THRESHOLD = 100 #mm must be in front of something to be beyond the background.
class DepthBackgroundSubtraction:
	# a class to do averaging and background subtraction
	# based on PyOpenNI's openni.DepthMap
	
	def __init__(self):
		self.background = None
		self.num_merges = 0
		pass
		
	def get_width(self):
		return self.background.shape[0]
	def get_height(self):
		return self.background.shape[1]
		
	def addToBackground(self, depthMap):
		#adds the given depthMap to the background
		
		if (self.num_merges == 0):
			self.background = np.zeros( (depthMap.width, depthMap.height) )
		
		self.num_merges += 1
		
		for y in range(self.get_height()):
			for x in range(self.get_width()):
				if depthMap[x,y] == 0:
					continue
				
				self.background[x,y] = self.background[x,y]*(1.0*self.num_merges - 1)/self.num_merges \
					+ depthMap[x,y]/self.num_merges
				
		
	# Convention is that a pixel value of 0 means "in background"
	def doBackgroundSubtraction(self, depthMap):
		# takes the given depthMap, subtracts the background from it,
		# and returns it
		
		pass
		
	def getForegroundPixel(self, depthMap, x, y):
		# returns a (pixel,bool) with background subtracted
		# bool is true if the pixel is foreground
		
		depthVal = depthMap[x,y]
		backgroundVal = self.background[x,y]
		
		if depthMap[x,y] != 0.0 and \
			self.background[x,y] == 0.0 or \
			self.background[x,y] - depthMap[x,y] > BACKGROUND_THRESHOLD:
			
			return (depthMap[x,y], True)
		else:
			return (self.background[x,y], False)
		
	
def update_kinect():
	# Update to next frame
	nRetVal = ctx.wait_one_update_all(depth)
	
	depthMap = depth.map
	#print type(depth)
	#print type(depth.map)
	# Get the coordinates of the middle pixel
	x = depthMap.width / 2
	y = depthMap.height / 2

	# Get the pixel at these coordinates
	pixel = depthMap[x,y]

	#print "The middle pixel is %d millimeters away." % pixel
	return depthMap
	

DOWNSAMPLE = 16
MESH_VISIBLE = 1
def make_kinect_mesh(depthMap):
	#Build cube
	RADIUS = 1
	
	depthArray = depthMap.get_array()
	
	viz.startLayer(viz.QUADS)
	
	for y in range(0,depthMap.height-1,DOWNSAMPLE):
		for x in range(0,depthMap.width-1,DOWNSAMPLE):
			
			depth_val = depthMap[x,y]/(4*1000.0);

			viz.vertex([x*1.0/depthMap.width, 1 - y*1.0/depthMap.height, depth_val])
			viz.vertex([x*1.0/depthMap.width, 1 - (y+DOWNSAMPLE)*1.0/depthMap.height, depth_val])
			viz.vertex([(x+DOWNSAMPLE)*1.0/depthMap.width, 1 - (y+DOWNSAMPLE)*1.0/depthMap.height, depth_val])
			viz.vertex([(x+DOWNSAMPLE)*1.0/depthMap.width, 1 - (y)*1.0/depthMap.height, depth_val])
			
			pixel_colour = 1 - depthMap[x,y]/(1000.0 * 3.0)
			viz.vertexColor([ pixel_colour, 1, 1, MESH_VISIBLE ])

	kinect_mesh = viz.endLayer()
	kinect_mesh.setPosition([0,0.5,3])
	
	return kinect_mesh



def update_kinect_mesh(kinect_mesh, depthMap, backgroundMap = None):
	kinect_mesh.clearVertices()
	
	for y in range(0,depthMap.height,DOWNSAMPLE):
		for x in range(0,depthMap.width,DOWNSAMPLE):
			
			(depth_val, isForeground) = backgroundMap.getForegroundPixel(depthMap,x,y)
			depth_val /=(4*1000.0)
			#depth_val = depthMap[x,y]/(4*1000.0);
			if (depth_val == 0.0 or not isForeground):
				continue
			
			pixel_colour_val = 1 - depthMap[x,y]/(1000.0 * 4.0)
			pixel_colour = [ pixel_colour_val, pixel_colour_val, pixel_colour_val, MESH_VISIBLE ]
			if isForeground:
				pixel_colour = [ pixel_colour_val, 0, 0, MESH_VISIBLE ]
			
			kinect_mesh.addVertex( 
				x*1.0/depthMap.width, \
				1- y*1.0/depthMap.height, \
				depth_val, \
				pixel_colour )
			kinect_mesh.addVertex( 
				x*1.0/depthMap.width, \
				1- (y+DOWNSAMPLE)*1.0/depthMap.height, \
				depth_val, \
				pixel_colour )
			kinect_mesh.addVertex( 
				(x+DOWNSAMPLE)*1.0/depthMap.width, \
				1- (y+DOWNSAMPLE)*1.0/depthMap.height, \
				depth_val, \
				pixel_colour )
			kinect_mesh.addVertex( 
				(x+DOWNSAMPLE)*1.0/depthMap.width, \
				1- y*1.0/depthMap.height, \
				depth_val, \
				pixel_colour )
			

	
GET_FRESH_BACKGROUND = False
BACKGROUND_FILENAME = 'background'

def get_kinect_background():
	print 'doing background subtraction'

	background = None

	if not GET_FRESH_BACKGROUND:
		try:
		   	background_file = open(BACKGROUND_FILENAME,'r')
		   	background = pickle.load(background_file)
		   	background_file.close
		   	print 'background loaded'
		except IOError:
		   	print 'Could not find or open background file.'

	if background == None:
		print 'Capturing new background'

		background = DepthBackgroundSubtraction()
		
		for i in range(4):
			print '.'
			depthMap = update_kinect()
			background.addToBackground(depthMap)
			time.sleep(0.1)
			
		print 'done background subtraction.'

		print 'saving out background'
		   
		background_file = open(BACKGROUND_FILENAME,'w')
		pickle.dump(background,background_file)
		background_file.close()

	
	return background
	
backgroundMap = get_kinect_background()


#create mesh initially.
depthMap = update_kinect()
kinect_mesh = make_kinect_mesh(depthMap)
# Notify Vizard that the vertices of the object are going to be updated frequently
kinect_mesh.dynamic() 

#cast Kinect Shadows
shadow.addCaster(kinect_mesh)


def frame_tick():
	depthMap = update_kinect()
	update_kinect_mesh(kinect_mesh, depthMap, backgroundMap)
	
	
#frame_tick()
vizact.ontimer(0, frame_tick)

viz.go()