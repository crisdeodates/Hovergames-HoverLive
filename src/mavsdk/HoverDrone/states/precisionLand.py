from HoverDrone import Drone
from HoverDrone.states.controlledLand import ControlledLand
from mavsdk import System
from mavsdk.offboard import (OffboardError,Attitude,VelocityNedYaw, PositionNedYaw)
import numpy as np
import asyncio
def distance_between(p1,p2):
	squared_dist = np.sum((p1-p2)**2, axis=0)
	return np.sqrt(squared_dist)
def saturate(lower,upper,value):
	if(value>upper):
		value = upper
	if(value<lower):
		value = lower
	return value
class ControlledLand:
	def __init__(self, threshold: float = 1.0, Guided: bool = True, MarkerID = ""):
		self.threshold = threshold
		self.Guided = Guided
		self.MarkerID = MarkerID

	async def __call__(self, drone):
		await drone.arm(coordinate=[0.0,0.0,0.0],attitude=[0.0,0.0,0.0])
		await drone.start_offboard()
		flag = True
		print(f"-- Precision Landing on Marker")		
		async for position_ned in drone.conn.telemetry.position_velocity_ned():
			currentposn = np.array([position_ned.position.north_m,position_ned.position.east_m, position_ned.position.down_m])

			xerror =  self.positions[0] - currentposn[0] 
			yerror = self.positions[1] - currentposn[1]

			xvelocity = xerror *2
			yvelocity = yerror *2
			zvelocity = -0.5 *currentposn[2]
			if(currentposn[2]>self.slowHeight):
				zvelocity = -0.1 *currentposn[2]

			await drone.conn.offboard.set_velocity_ned(VelocityNedYaw(xvelocity,yvelocity,zvelocity,0.0))
			await asyncio.sleep(0.01)

			if(currentposn[2]>-1):
				 break
