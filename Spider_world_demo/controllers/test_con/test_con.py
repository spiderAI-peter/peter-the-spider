from controller import Robot

robot = Robot()

timestep = int(robot.getBasicTimeStep())

print("TEST CONTROLLER STARTED")

while robot.step(timestep) != -1:
    pass