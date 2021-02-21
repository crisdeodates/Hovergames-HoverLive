from HoverDrone import Drone
from mavsdk import System
import numpy as np

class Disarm:
	async def __call__(self, drone):
		await drone.disarm()
		print("-- Disarming")
