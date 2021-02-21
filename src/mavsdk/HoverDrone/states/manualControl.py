from HoverDrone import Drone
from mavsdk import System
from mavsdk.offboard import (OffboardError,Attitude, AttitudeRate, PositionNedYaw, ActuatorControl)
import numpy as np
import asyncio

class ManualControl:
	async def __call__(self, drone):
		await drone.arm(coordinate=[0.0,0.0,0.0],attitude=[0.0,0.0,0.0])
		print("-- Starting offboard")
		try:
			await drone.conn.offboard.start()
		except OffboardError as error:
			print(f"Starting offboard mode failed with error code: {error._result.result}")
			print("-- Disarming")
			await drone.conn.action.disarm()
			return
		print("-- Starting Manual Control")
		await drone.conn.offboard.set_actuator_control(ActuatorControl(({1.0,1.0,1.0,1.0})))
