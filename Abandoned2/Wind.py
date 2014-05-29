import math
import random

class Wind:
	#note: y is up.
	
	def update(self, elapsed):
		self.vy = 0
		
		#randomly adjust wind angle and speed
		self.angle += (random.random()*2.0 - 1.0)*self.MAX_ROTATE_SPEED*elapsed
		self.wind_speed += (random.random()*2.0 - 1.0)*self.WIND_SPEED_VARIATION*elapsed
		self.wind_speed = max(0, self.wind_speed)
		self.wind_speed = min(self.wind_speed, self.MAX_WIND_SPEED)
		
		#note: not sure if I have this correspondence between x&z right.
		self.vx = math.sin(self.angle)*self.wind_speed*elapsed
		self.vz = math.cos(self.angle)*self.wind_speed*elapsed
	
	def __init__(self, MAX_WIND_SPEED):
		self.MAX_WIND_SPEED = MAX_WIND_SPEED
		self.WIND_SPEED_VARIATION = self.MAX_WIND_SPEED*0.4
		self.MAX_ROTATE_SPEED = 0.6
		
		self.angle = 0
		self.wind_speed = self.MAX_WIND_SPEED
		
		self.vx = 0
		self.vy = 0
		self.vz = 0
		
		self.update(0)
		
	


