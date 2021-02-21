from HoverDrone import Drone
from mavsdk import System
import numpy as np
import asyncio

class Land:
	async def __call__(self, drone):
		await drone.land()
		print("-- Landing")
