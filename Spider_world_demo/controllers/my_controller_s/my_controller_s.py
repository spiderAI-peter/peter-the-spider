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

class spider ():

#this is what the individual "creature" holds
#some things to id it and track where it came from
#then the genes code such that 
#after will be the items that will be recored during the sim
#last is just the fitness code

#note parents will look like a tree in the end
#not add more with fitness not all the stuff we need 
#again fit function is NOT done
    def __init__(self,generation, number,parent1 = None, parent2 = None,genes = None):
        self.id=  f"G{generation}-R{number:03d}"
        
        self.generation = generation
        
        self.mother = parent1
        self.father = parent2
        
        self.genes = self.new_or_given(genes)
                        
                
        #for fitness evaluation
        self.hights  = []
        self.distance = 0
                
        self.fitness = 0
        
#creates angles values at random 
    def randam_rads(self):
        frame = []
        for _ in range (0,24):
            frame.append(rd.uniform(-1, 1))
        return frame

#determinds if there are now genes and need to make new ones
#or if it can just return the already made genes
#when making a new one to start for now the spiders genes are 12 frames that will be 
#cycled 25 times 
#note: if this does not work the first thing you can do is make it the full 300 
#could be slower but could make a big change
    def new_or_given(self,genes):
        
        if genes == None:
            frames = 12
            #should give x amount of frames 
            #so the list is 2D:
            # [[0.9,0.8,-0.6,....0.5],[0.6,.....],.....]
            # [12 x [24 x numbers]]
            return [self.randam_rads() for _ in range(0, frames)],
        else:
            return genes

#fitness functions 
#link to vid where some things could be based on e.g hight staying the same ish
#  - https://www.youtube.com/watch?v=NV8a4QJfHVg

#curently based on 
#  - keeping hight a on average constant 
#  - distance to make the thing move (z cord)

# note: need more prob after testing
# if it fall less points
# 
#this is not done and is almost meaninngless we need a proper one
#DO SOMETHING
    def fitness_f(self):
        distance = self.distance
        hights = self.hights
        hight_score = 1 - (max(hights) - min(hights))
        
        self.fitness = distance * hight_score


#make size x for testing
#just the brackets of being randomly made 
#this can have repeats 
def make_tournament_backets (population, size):
    wins = []
    
    for _ in range (0,len(population),size):
        backets = []
        for _ in range (0,size):
            individual = rd.choice(population)
            backets.append(individual)
              
        wins.append(tournament(backets))
    
    return wins

#when give the amount of individules find the one with highest fit 
#value and selects them to win with the highest number
def tournament (backets):
    fit_values = []
    for individual in backets:
        fit_values.append (individual.fitness)
    
        
    highest = max(fit_values)
    #this just find location of highest in the list and then collects 
    #same number as the full individual infomation 
    #more dumb - we get all the extra stuff like genes and parents
    winner = backets(fit_values(highest))
    return winner

#given 2 partents and mix their genes around for each frame 
def crossbreeding (par1, par2):
    child1 = []
    child2 = []
    
    par_split1 = par1.split()
    par_split2 = par2.split()
    for x in range (0,12):
        #the part of the frame is split diffrent for fun 
        #if this breakes dont keep
        split = rd.randint(4,20)
        
        par_first_genes1 = par_split1[x][:split]
        par_sec_genes1 = par_split1[x][split:]
        
        par_first_genes2 = par_split2[x][:split]
        par_sec_genes2 = par_split2[x][split:]
        
        
        child1.append(par_first_genes1 + par_sec_genes2)
        child2.append(par_first_genes2 + par_sec_genes1)
        
    return child1, child2

#gives a random chance to mutate change as you pled
def mutation (child, rate, max_power):
    
    for frame in child:
        for gene in frame:
            if rd.randint(1,11) <= rate:
                gene += rd.uniform(-max_power, max_power)
       
#just fun function put together to make a child
#first collect genes 
#crossbreed dem
#mutation 
#add 1 to gen counter for id
#then create the next individuals with group used as ID in the generation 
#G1-R3 for example is gen 1 and 3rd individual in gen
def make_child(winner1, winner2, group,mutation_rate, mutation_max_power):
    par1 = winner1.genes
    par2 = winner2.genes
    
    child1, child2 = crossbreeding (par1, par2)

    fin_child1 = mutation (child1,mutation_rate, mutation_max_power)
    fin_child2 = mutation (child2,mutation_rate, mutation_max_power)
    
    generation = winner1["generation"] + 1
    end_child1 = spider(generation, group, winner1, winner2, fin_child1 )
    end_child2 = spider(generation, group+1, winner1, winner2, fin_child2 )
    
    return end_child1, end_child2
    
mutation_rate = 1 #%10
mutation_max_power = 0.2
size = 2

population = []
#create the first population 
for i in range(1, 25):

    individual = spider(1, i)

    population.append(individual)

# =========================================================
# sim starts
# =========================================================

#things to know about sim
#you will need to recoded things for fitness 
#like the hight at x intivales 
#the distance it travled 
#if it fell 

#also when doing the moving remember 12 frames will be done 25 times for now 

TARGET_ANGLES = { # this is setting the original target angles from the standing animation this in teroy is what we want to put the GA on

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

position = gps.getValues()

current_z = position[2]

print("") # this is the code that ioannis gave us to set up the moters so this persumibly is also where we want to apply the GA 
print("==============================================")
print("SETTING WALKING POSITION'S")
print("==============================================")

# i am adding the spider class to the legs i think this is what we are suposed to do to get it working i think
walinkg_cycle = spider (right_legs)
walinkg_cycle_2 = spider (left_legs)

backets = make_tournament_backets (walinkg_cycle, size)
# these two handels the tornment on the legs all this code has not been run 
tournament_backets = tournament (backets)

backets_2 = make_tournament_backets (walinkg_cycle, size)

tournament_backets_2 = tournament (backets_2)

backets_3 = make_tournament_backets (walinkg_cycle_2, size)

tournament_backets_3 = tournament (backets_3)

backets_4 = make_tournament_backets (walinkg_cycle_2, size)

tournament_backets_4 = tournament (backets_4)

winner1 = crossbreeding (tournament_backets, tournament_backets_2)

winner2 = crossbreeding (tournament_backets_3, tournament_backets_4)

child = make_child(winner1, winner2, all_legs,mutation_rate, mutation_max_power)


for side, child in [
    ("R", right_legs),
    ("L", left_legs)
]:

    angles = TARGET_ANGLES[side]
    
    walinkg_cycle_3 = spider (angles)# this if i think im remembering classes corectly and if what ive googled is correct this should be the base line 
    
    walinkg_cycle_4 = spider (position) # this should in theroy be apply the spider class to the position i think im suposed to do this.

    backets = make_tournament_backets (walinkg_cycle_3, size) # think this is correct still flying buy the seat of my pants i dont know what im doing but to my knowlege this should in theroy apply the tormaent on the  walking cycle onto 

    tournament_backets = tournament (backets) # this should in theroy apply the tournament function onto the torment barckets 

    backets_2 = make_tournament_backets (walinkg_cycle_4, size) # this is applying the tornment  onto the position i think im ment to do this.
    tournament_backets_2 = tournament (backets_2)

    for leg in child:

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
# sim end
# =========================================================

#DONT bother running if you have not made sim first 
#i dont know why youy tried looking when things have all nothing or 0
for x in population:
    x.fitness_f()

wins = make_tournament_backets (population,size)
for group in range (0,len(wins),2):
    winner1 = rd.choice(wins)
    wins.remove (winner1)
    
    winner2 = rd.choice(wins)
    wins.remove (winner2)
    
    make_child(winner1, winner2, group,mutation_rate, mutation_max_power)



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