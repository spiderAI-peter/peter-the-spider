import math
import random as rd
from controller import Robot

# =========================================================
# INITIALISE ROBOT
# =========================================================

robot = Robot()

timestep = int(robot.getBasicTimeStep())


# =========================================================
# LEGS
# =========================================================

right_legs = ["R1", "R2", "R3", "R4"]
left_legs  = ["L1", "L2", "L3", "L4"]

all_legs = right_legs + left_legs



# =========================================================
# TARGET STANDING POSITION
# =========================================================

TARGET_ANGLES = {

    "R": {
        "hip_joint": 0.0,
        "thigh_joint": 1.07,
        "knee_joint": -0.58
    },

    "L": {
        "hip_joint": 0.0,
        "thigh_joint": -1.07,
        "knee_joint": 0.58
    }
}



# =========================================================
# GPS
# =========================================================

gps = robot.getDevice("gps")

if gps is None:
    print("ERROR: GPS not found!")
    exit()

gps.enable(timestep)






# =========================================================
# MOTOR SETTINGS
# =========================================================

MOTOR_VELOCITY = 1.5

# Small movement made each cycle.
#
# 0.5 degrees is deliberately small so that we can
# observe the effect on the actual robot height.
#
LOWER_STEP = math.radians(0.5)


# =========================================================
# GET MOTORS
# =========================================================

motors = {}

for side, leg_list in [
    ("R", right_legs),
    ("L", left_legs)
]:

    for leg in leg_list:

        for joint_type in [
            "hip_joint",
            "thigh_joint",
            "knee_joint"
        ]:

            motor_name = f"{leg}_{joint_type}"

            motor = robot.getDevice(motor_name)

            if motor:

                motors[motor_name] = motor
                motor.setVelocity(MOTOR_VELOCITY)

            else:

                print(
                    f"WARNING: Motor '{motor_name}' not found!"
                )


# =========================================================
# SET INITIAL STANDING POSITION
# =========================================================

print("")
print("==============================================")
print("SETTING INITIAL STANDING POSITION")
print("==============================================")


for side, leg_list in [
    ("R", right_legs),
    ("L", left_legs)
]:

    angles = TARGET_ANGLES[side]

    for leg in leg_list:

        motors[
            f"{leg}_hip_joint"
        ].setPosition(
            angles["hip_joint"]
        )

        motors[
            f"{leg}_thigh_joint"
        ].setPosition(
            angles["thigh_joint"]
        )

        motors[
            f"{leg}_knee_joint"
        ].setPosition(
            angles["knee_joint"]
        )


# =========================================================
# WAIT FOR STANDING POSITION
# =========================================================

print("Waiting for standing position...")

for _ in range(
    int(3.0 * 1000 / timestep)
):

    if robot.step(timestep) == -1:
        exit()


# =========================================================
# READ INITIAL GPS HEIGHT
# =========================================================

position = gps.getValues()

current_z = position[2]



print("")
print("==============================================")
print("INITIAL GPS POSITION")
print("==============================================")
print(
    f"X = {position[0]:.4f} m"
)
print(
    f"Y = {position[1]:.4f} m"
)
print(
    f"Z = {position[2]:.4f} m"
)

print("")
print(
    f"Target Z = 0.3000 m"
)
print(
    f"Current Z = {current_z:.4f} m"
)


# =========================================================
# CURRENT JOINT TARGETS
# =========================================================

right_thigh = TARGET_ANGLES["R"]["thigh_joint"]
right_knee = TARGET_ANGLES["R"]["knee_joint"]

left_thigh = TARGET_ANGLES["L"]["thigh_joint"]
left_knee = TARGET_ANGLES["L"]["knee_joint"]


# =========================================================
# LOWER ROBOT
# =========================================================

print("")
print("==============================================")
print("LOWERING ROBOT")
print("==============================================")
print("")


TARGET_Z = 0.300


while robot.step(timestep) != -1:

    # -----------------------------------------------------
    # READ GPS
    # -----------------------------------------------------

    position = gps.getValues()

    current_z = position[2]


    # -----------------------------------------------------
    # CHECK WHETHER TARGET HEIGHT HAS BEEN REACHED
    # -----------------------------------------------------

    if current_z >= TARGET_Z:

        print("")
        print("==============================================")
        print("TARGET HEIGHT REACHED")
        print("==============================================")

        print(
            f"GPS Z = {current_z:.4f} m"
        )

        break


    # -----------------------------------------------------
    # LOWER THE LEGS
    # -----------------------------------------------------
    #
    # Right side:
    #   thigh becomes more positive
    #   knee becomes more negative
    #
    # Left side:
    #   thigh becomes more negative
    #   knee becomes more positive
    #
    # This increases the absolute movement symmetrically.
    #
    # -----------------------------------------------------

    right_thigh += LOWER_STEP
    right_knee -= LOWER_STEP

    left_thigh -= LOWER_STEP
    left_knee += LOWER_STEP


    # -----------------------------------------------------
    # COMMAND RIGHT LEGS
    # -----------------------------------------------------

    for leg in right_legs:

        motors[
            f"{leg}_thigh_joint"
        ].setPosition(
            right_thigh
        )

        motors[
            f"{leg}_knee_joint"
        ].setPosition(
            right_knee
        )


    # -----------------------------------------------------
    # COMMAND LEFT LEGS
    # -----------------------------------------------------

    for leg in left_legs:

        motors[
            f"{leg}_thigh_joint"
        ].setPosition(
            left_thigh
        )

        motors[
            f"{leg}_knee_joint"
        ].setPosition(
            left_knee
        )


    # -----------------------------------------------------
    # REPORT POSITION
    # -----------------------------------------------------

    print(
        f"Z = {current_z:.4f} m | "
        f"R thigh = {math.degrees(right_thigh):.2f}° | "
        f"R knee = {math.degrees(right_knee):.2f}° | "
        f"L thigh = {math.degrees(left_thigh):.2f}° | "
        f"L knee = {math.degrees(left_knee):.2f}°"
    )


# =========================================================
# GA start 
# =========================================================

def randam_rads ():
    frame = []
    for _ in range (0,24):
        frame.append(rd.uniform(-1, 1))
    return frame

def create_individual(generation, number):

    individual = {
        "id": f"G{generation}-R{number:03d}",

        "generation": generation,

        "parents": [],

        "genes": [randam_rads() for _ in range(0, 12)],
        
        #for fitness evaluation
        "hights": [],
        "distance": 0,
        
        "fitness": 0,
    }

    return individual


#fitness functions 
#link to vid where some things could be based on e.g hight staying the same ish
#  - https://www.youtube.com/watch?v=NV8a4QJfHVg

#curently based on 
#  - keeping hight a on average constant 
#  - distance to make the thing move (z cord)

# note: need more prob after testing
# if it fall less points
# 

def fitness_f(individual):
    distance = individual[distance]
    hights = individual[hights]
    hight_score = 1 - (max(hights) - min(hights))
    
    score = distance * hight_score
    individual ["fitness"] = score

#make size 2 for testing
def make_tournament_backets (population,size):
    wins = []
    
    for _ in range (0,len(population),size):
        backets = []
        for _ in range (0,size):
            individual = rd.choice(population)
            backets.append(individual)
              
        wins.append(tournament(backets))
    
    return wins
        
def tournament (backets):
    fit_values = []
    for x in backets:
        fit_values.append (x["fitness"])
    
        
    highest = max(fit_values)
    winner = backets(fit_values(highest))
    return winner


def crossbreeding (par1, par2):
    child1 = []
    child2 = []
    for _ in range (0,12):
        split = rd.randint(4,20)
        
        par_first_genes1 = par1[:split]
        par_sec_genes1 = par1[split:]
        
        par_first_genes2 = par2[:split]
        par_sec_genes2 = par2[split:]
        
        
        child1.append(par_first_genes1 + par_sec_genes2)
        child2.append(par_first_genes2 + par_sec_genes1)
        
    return child1, child2

def mutation (child):
    rate = 1 #%10
    max_power = 0.2
    
    for x in child:
        if rd.randint(1,11) <= rate:
            x += rd.uniform(-max_power,max_power)
    
    
def create_child(generation, number, parent1, parent2,genes):

    individual = {
        "id": f"G{generation}-R{number:03d}",

        "generation": generation,

        "parents": [parent1,parent2],

        "genes": genes,
        
        #for fitness evaluation
        "hights": [],
        "distance": 0,
        
        "fitness": 0,
    }      
        
def make_child(winner1, winner2, group):
    par1 = winner1["genes"]
    par2 = winner2["genes"]
    
    child1, child2 = crossbreeding (par1, par2)
    
    fin_child1 = mutation (child1)
    fin_child2 = mutation (child2)
    
    generation = winner1["generation"]+1
    end_child1 = create_child(generation, group, winner1, winner2, fin_child1 )
    end_child2 =create_child(generation,group+1, winner1, winner2, fin_child2 )
    
    return end_child1, end_child2
    

population = []
#create the first population 
for i in range(1, 25):

    individual = create_individual(1, i)

    population.append(individual)

# =========================================================
# sim starts
# =========================================================


# =========================================================
# sim end
# =========================================================

for x in population:
    fitness_f(x)

size = 2
wins = make_tournament_backets (population,size)
for group in range (0,len(wins),2):
    winner1 = rd.choice(wins)
    wins.remove (winner1)
    
    winner2 = rd.choice(wins)
    wins.remove (winner2)
    
    make_child(winner1, winner2, group)



# =========================================================
# GA end 
# =========================================================

# =========================================================
# HOLD POSITION
# =========================================================

print("")
print("Robot is holding its position.")

while robot.step(timestep) != -1:

    pass