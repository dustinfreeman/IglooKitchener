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

frameCount = 0

#load scene
ground = viz.add('tut_ground.wrl')
ground2 = viz.add('tut_ground.wrl', pos = (0,0,5), euler = (0,270,0) )
#Create shadow projector
#Shadow resolution (power of two)
#Higher values mean sharper shadows, but take more texture memory
SHADOW_RES = 256

#Postion of shadow projector
SHADOW_POS = [0,3,2]
SHADOW_EULER = [0,25,0]

#Controls size of orthographic shadow projector
#Large values mean larger area is covered, but resolution will be diluted
SHADOW_AREA = [5,5]
shadow = Shadow.ShadowProjector(size=SHADOW_RES,pos=SHADOW_POS,area=SHADOW_AREA, euler = SHADOW_EULER )
#Add ground as shadow receiver
shadow.addReceiver(ground)
shadow.addReceiver(ground2)
	
def start_avatar():
	
	avatar = viz.add('vcc_female.cfg', pos = (0,0,4), euler=(180,0,0))
	avatar.state(5)

	#Add avatar as a shadow caster
	shadow.addCaster(avatar)

#start_avatar()

DOWNSAMPLE = 16 #for visualization and saving.

class DepthFrame:
	#this totally exploits duck typing, so this
	# class looks like an openni.DepthMap


	def __init__(self,depthMap):
		self.time = time.clock()

		self.width = depthMap.width
		self.height = depthMap.height
		self.map = np.zeros((self.width/DOWNSAMPLE,self.height/DOWNSAMPLE))

		#copy dat map
		for y in range(0, self.height, DOWNSAMPLE):
			for x in range(0, self.width, DOWNSAMPLE):
				self[x,y] = depthMap[x,y]

	def __setitem__(self, addr_tuple, value):
		self.map[ addr_tuple[0]/DOWNSAMPLE, addr_tuple[1]/DOWNSAMPLE] = np.float16(value);

	def __getitem__(self, addr_tuple):
		return self.map[ addr_tuple[0]/DOWNSAMPLE, addr_tuple[1]/DOWNSAMPLE];



class DepthSequence:
	#intended to be a saveable sequence of PyOpenNI's openni.DepthMap
	
	def __init__(self):
		self.sequence = []
		self.play_marker = 0 #index in sequence
		self.play_start = time.clock()
		self.play_finished = False

	def addDepthMap(self,depthMap):
		frame = DepthFrame(depthMap)
		self.sequence.append(frame)

	def getCurrentDepthMap(self):
		now = time.clock()

		if len(self.sequence) < 2:
			return

		recording_start = self.sequence[0].time
		playing_timespan = now - self.play_start

		if self.play_marker >= len(self.sequence) - 2:
			self.play_finished = True
			return

		#check if we should be on the next frame
		if playing_timespan >= self.sequence[self.play_marker + 1].time - recording_start:
			self.play_marker += 1
			
		# print '---------'
		# print self.sequence[self.play_marker + 1].time - recording_start
		# print playing_timespan

		return self.sequence[self.play_marker]



current_sequence = None
sequence_filename = None
def start_sequence(filename):
	global current_sequence
	global sequence_filename

	current_sequence = DepthSequence()
	sequence_filename = filename

def stop_sequence():
	global current_sequence
	global sequence_filename

	print 'saving sequence to ' + sequence_filename + ' ...'

	seq_file = open(sequence_filename,'w')
	pickle.dump(current_sequence, seq_file)
	seq_file.close()
	print 'sequence saved.'
	current_sequence = None
	sequence_filename = None

playing_sequence = None
def play_sequence(filename):
	global playing_sequence

	seq_file = open(filename, 'r')
	sequence = pickle.load(seq_file)
	seq_file.close()

	print 'play sequence ' + filename + ' loaded.'

	playing_sequence = sequence

	#TODO play sequence


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
	global current_sequence
	global playing_sequence

	# Update to next frame
	nRetVal = ctx.wait_one_update_all(depth)
	
	depthMap = depth.map

	#saving out
	if current_sequence != None:
		current_sequence.addDepthMap(depthMap)

	#playing/injecting
	if playing_sequence != None:
		play_depthMap = playing_sequence.getCurrentDepthMap()

		print 'playing...' + str(playing_sequence.play_marker) + '/' + str(len(playing_sequence.sequence))
		if playing_sequence.play_finished:
			playing_sequence = None
			print 'play finished.'
		else:
			depthMap = play_depthMap
		

	#print type(depth)
	#print type(depth.map)
	# Get the coordinates of the middle pixel
	#x = depthMap.width / 2
	#y = depthMap.height / 2
	# Get the pixel at these coordinates
	#pixel = depthMap[x,y]

	#print "The middle pixel is %d millimeters away." % pixel
	return depthMap
	

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


BACKGROUND_VISIBLE = True
def update_kinect_mesh(kinect_mesh, depthMap, backgroundMap = None):
	kinect_mesh.clearVertices()
	
	for y in range(0,depthMap.height,DOWNSAMPLE):
		for x in range(0,depthMap.width,DOWNSAMPLE):
			
			(depth_val, isForeground) = backgroundMap.getForegroundPixel(depthMap,x,y)
			depth_val /=(4*1000.0)
			#depth_val = depthMap[x,y]/(4*1000.0);
			if (depth_val == 0.0 or (not isForeground and not BACKGROUND_VISIBLE) ):
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
			

def update_shadows():
	#SHADOW_POS = [0,3,2]
	#SHADOW_EULER = [0,25,0]

	#slowly moves shadow, ideally should react to projection.
	
	SHADOW_POS[1] = 3 + (1.0/100)*(frameCount%100)

	shadow.setPosition(SHADOW_POS)
	#shadow.setEuler((-5 + frameCount % 10, 25, 0 ))

	
GET_FRESH_BACKGROUND = False
BACKGROUND_FILENAME = 'background'

backgroundMap = None

def get_kinect_background():
	print 'doing background subtraction'
	
	global backgroundMap
	background = None

	if not GET_FRESH_BACKGROUND:
		try:
		   	background_file = open(BACKGROUND_FILENAME,'r')
		   	background = pickle.load(background_file)
		   	background_file.close

		   	#set global variable
			backgroundMap = background
		   	
		   	print 'background loaded'
		except IOError:
		   	print 'Could not find or open background file.'

	if background == None:
		get_fresh_background()

	
def get_fresh_background():
	print 'Capturing new background'
	global backgroundMap

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

	#set global variable
	backgroundMap = background


#always get background at beginning
get_kinect_background()


#create mesh initially.
depthMap = update_kinect()
kinect_mesh = make_kinect_mesh(depthMap)
# Notify Vizard that the vertices of the object are going to be updated frequently
kinect_mesh.dynamic() 

#cast Kinect Shadows
shadow.addCaster(kinect_mesh)


def frame_tick():
	global frameCount

	frameCount+=1
	depthMap = update_kinect()
	update_kinect_mesh(kinect_mesh, depthMap, backgroundMap)
	update_shadows()
	
	
#frame_tick()
vizact.ontimer(0, frame_tick)

viz.go()