from HoverDrone import Drone
from HoverDrone.states import Arm
from HoverDrone.states import Disarm
from HoverDrone.states import Takeoff
from HoverDrone.states import Land, PrecisionLand

my_drone = Drone.connect("myDrone", "udp://:14540")
my_drone.start()
my_drone.add_roles({"Emergency", "Support", "Delivery"})
my_drone.add_state(Disarm)
my_drone.add_state(Takeoff(5.0))
my_drone.add_state(land)
my_drone.add_state(PrecisionLand(threshold=3.0, Guided=True, MarkerID=xxx))
my_drone.add_states_to_role("Emergency", {Arm, Disarm, Takeoff, Land})
my_drone.add_states_to_role("Support", {Arm, Disarm, Takeoff, Land, Loiter})
my_drone.add_states_to_role("Delivery", {Arm, Disarm, Takeoff, PrecisionLand})
my_drone.join()
