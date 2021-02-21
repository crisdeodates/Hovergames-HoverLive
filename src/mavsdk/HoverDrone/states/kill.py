from HoverDrone import Drone
from mavsdk import System
import numpy as np
import asyncio

class Kill:
	async def __call__(self, drone):
		await drone.kill()
		print("-- Drone Killed")
