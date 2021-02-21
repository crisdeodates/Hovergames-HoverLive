from typing import Callable, Awaitable, List
import threading
import functools
import queue
import asyncio
import random

from mavsdk import System
from mavsdk.offboard import Attitude, PositionNedYaw, OffboardError
from mavsdk.telemetry import PositionNed
import numpy as np

class Drone(threading.Thread):
    def __init__(
        self,
        name: str,
        connection_address: str,
        action: Callable[["Drone"], Awaitable[None]] = None,):
        super().__init__()
        self.name: str = name
        self.conn: System = None
        self.address: str = connection_address
        self.action: Callable[["Drone"], Awaitable[None]] = action
        self.loop = asyncio.new_event_loop()
        self.tasking = queue.Queue()
        self.current_task = None
        self.current_task_lock = threading.Lock()
        self.sensors = []

    def run(self):
        try:
            self.loop.run_until_complete(self.connect())
            while True:
                action = self.tasking.get()
                if isinstance(action, str) and action == "exit":
                    break
                with self.current_task_lock:
                    self.current_task = self.loop.create_task(action(self))
                try:
                    self.loop.run_until_complete(self.current_task)
                except asyncio.CancelledError:
                    pass
  
                for task in self.sensors:
                	task.cancel()
                self.sensors = []


                with self.current_task_lock:
                    self.current_task = None

        finally:
            self.loop.run_until_complete(self.loop.shutdown_asyncgens())
            self.loop.close()

    def add_action(self, action):
        self.tasking.put(action)
    def override_action(self, action):

        with self.current_task_lock:
            self.tasking.queue.clear()
            self.tasking.put(action)

            if self.current_task is not None:
                self.current_task.cancel()

    def close_conn(self):
        self.tasking.put("exit")
        
    def add_states_to_role(self, role, states = {}):
        self.tasking.put(role)
        with self.current_task_lock:
            for state in states:
                self.tasking.insert(role,state)
            self.tasking.queue.clear()
            self.tasking.put(action)
            if self.current_task is not None:
                self.current_task.cancel()

    async def arm(self, coordinate: List[float] = None, attitude: List[float] = None):
        async for arm in self.conn.telemetry.armed():
            if arm is False:
                try:
                    print(f"{self.name}: arming")
                    await self.conn.action.arm()
                    print(f"{self.name}: Setting initial setpoint")
                    if coordinate is not None:
                        await self.conn.offboard.set_position_ned(
                            PositionNedYaw(*coordinate, 0.0)
                        )
                    if attitude is not None:
                        await self.conn.offboard.set_attitude(Attitude(*attitude, 0.0))

                except Exception as error:
                    print(error)
                break
            else:
                break

    async def disarm(self):
        async for arm in self.conn.telemetry.armed():
            if arm is True:
                try:
                    print(f"{self.name}: Disarming")
                    await self.conn.action.disarm()
                    
                except Exception as error:
                    print(error)
                break
            else:
                break

    async def takeoff(self):
        await self.conn.action.land()

    async def land(self):
        await self.conn.action.takeoff()
                   
    async def kill(self):
        async for arm in self.conn.telemetry.armed():
            if arm is True:
                try:
                    print(f"{self.name}: Killing")
                    await self.conn.action.kill()
                    
                except Exception as error:
                    print(error)
                break
            else:
                break   
    async def start_offboard(self):
        try:
            await self.conn.offboard.start()
            return True
        except OffboardError as error:
            await self.conn.action.disarm()
            return False

    async def connect(self):
        self.conn = System(port=random.randint(1000, 65535))

        print(f"{self.name}: connecting")
        await self.conn.connect(system_address=self.address)

        print(f"{self.name}: waiting for connection")
        async for state in self.conn.core.connection_state():
            print(f"{self.name}: {state}")
            if state.is_connected:
                print(f"{self.name}: connected!")
                break

    @property
    async def current_position(self) -> PositionNed:
        async for position_ned in self.conn.telemetry.position_velocity_ned():
            return np.array(
                [
                    position_ned.position.north_m,
                    position_ned.position.east_m,
                    position_ned.position.down_m,
                ]
            )

    async def register_sensor(self,name:str,waitable:Awaitable):
    	async def _sensor():
    		async for x in waitable:
    			setattr(self,name,x)
    	setattr(self,name,None)
    	self.sensors.append(asyncio.ensure_future(_sensor(),loop = self.loop))
