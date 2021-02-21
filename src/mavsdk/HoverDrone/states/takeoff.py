from HoverDrone import Drone
from mavsdk import System
import numpy as np
import asyncio

class land:
	async def __call__(self, drone):
		await drone.takeoff()
		print("-- Taking Off")
