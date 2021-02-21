from HoverDrone import Drone
from mavsdk import System
import numpy as np
import asyncio

class Arm:
	async def __call__(self, drone):
		await drone.arm(coordinate=[0.0,0.0,0.0],attitude=[0.0,0.0,0.0])
		print("-- Arming")
