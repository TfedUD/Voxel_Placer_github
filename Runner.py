from Person import Person
from Envelope import Envelope
from Schedule import people_dictionary
import random as r
import time

timestr = time.strftime("%Y%m%d-%H%M")

###################################################################
#### ALL INPUTS ##############
x_s = 37 #28
y_s = 1 #9
z_s = 37 #28

### SEED
seed = 0 # not doing anything if we use ready points
r.seed(seed)
########## THE RUNNER INPUTS
tick_start = 150
tick = tick_start # starting frame of render
tick_max = 160 # ending frame -# ticks and tick_max are the same
evaluation_num = 0 # it will be reset to 0 every tick iteration later
evaluation_max = 100 # how many times the brain should try to compute positions

value = "need"  # "desire"

# GENERATING ENVELOPE AND PEOPLE FOR ONE TIME
# the envelope and people should be already generated here

# these are tested points based on tick 105 after 100 iterations

points = [(20, 0, 31), (31, 0, 28), (16, 0, 23), (16, 0, 0), (31, 0, 0), (6, 0, 17), (32, 0, 20), (29, 0, 10), (14, 0, 13), (17, 0, 31), (20, 0, 15), (36, 0, 4), (1, 0, 0), (4, 0, 27), (9, 0, 1), (4, 0, 10), (24, 0, 24), (22, 0, 8)]

"""
# POINTS FOR PEOPLE CENTERS
points = []

for i in range(18):
    x = r.randint(0,x_s)
    y = r.randint(0,y_s)
    z = r.randint(0,z_s)

    point = (x, y, z)
    points.append(point)
"""
#print(points)

# ENVELOPE
e = Envelope(x_s, y_s, z_s)

# PEOPLE
names_and_schedules = people_dictionary()
people_classes = []
index_counter = 0

# CREATING PEOPLE
for name in names_and_schedules:
    #print name
    person = Person(name, (points[index_counter][0], points[index_counter][1],points[index_counter][2]), e )
    people_classes.append(person)
    index_counter += 1


##############################################
################ DICTIONARIES ################
# we have two output types: every one has two dictionaries.. one for positions and one for logs!!
# THE BRAIN
# positions
brain_states = {}
# logs
brain_personal_logs = {}
# later we will add brain_envelope_logs

# THE ORGANIZATION
# positions
organized_states = {}
# logs
organized_personal_logs = {}

brain_counter = 0 # updates in the two time loops
#### I don't think we need the organized counter.. it's replaced with tick
organized_counter = 0 #update one time at the end of the inner loop

# the value stored in each of these keys is a dictionary of persons, conflicts as keys
# and the value inside in the positions of them


while tick < tick_max:
    # use the activity according to tick
    # it means we update the activity here

    evaluation_num = 0 ### important: this resets to 0 for every new tick
    # the brain counter should keep counting though!!
    # the evaluation_num tells us how many times brain will compute for one tick
    # but the output of that is saved in a flattened list for all the ticks
    # so the flattened list is stored by the brain_counter as a list
    while evaluation_num < evaluation_max:
        # update the position
        # THE INSIDE DICTIONARY OF BRAIN
        brain_states[brain_counter] = {}
        state_of_brain = brain_states[brain_counter] #group of positions ? for people and conflicts

        ############ RUN
        # [1]: update people
        # introduce_person
        for person in people_classes:
            person.introduce_person()

        # UPDATE POSITION
        for person in people_classes:
            person.update_position()

        # UPDATE ACTIVITY
        for person in people_classes:
            person.update_activity_pattern_to(tick) # activity is based on the outer loop tick

        # [2]: Placing the poeple in the envelope
        e.place_people(people_classes)

        # [3]: People Evaluation of what they got!
        for person in people_classes:
            person.evaluate_position(value) #or need?

        # [4]: outputting
        # every iteration we output the current state of the envelope and people!
        # all as OBJECTS/CLASSES
        envelope = e             # envelope as a state of the machine
        people = people_classes  # outputting people!

        # filling the inside dictionary state_of_brain
        #inside_log_dictionary = all_personal_logs[tick]

        conflict_dict = e.cells_in_conflict()
        #conflict_list = []
        conflict_list_need = []
        conflict_list_desire = []

        for key in conflict_dict:
            if conflict_dict[key][0] == 100:
                conflict_list_need.append(key.position)
            if conflict_dict[key][0] == 1:
                conflict_list_desire.append(key.position)


        all_need = []


        # this is the brain dictionary
        state_of_brain["conflict_need"] = conflict_list_need
        state_of_brain["conflict_desire"] = conflict_list_desire

        state_of_brain["notifications"] = envelope.notifications

        for person in people:
            # the first
            state_of_brain[person.name] = [person.activity] + person.claimed_cells
            #inside_log_dictionary[person.name] = person.personal_log

            # check_me
            personal_need = person.need()
            for position in personal_need:
                if position in person.claimed_cells:
                    all_need.append(position)

        state_of_brain["all_need"] = all_need



        movement_counter = 0
        for person in people:
            movement_counter += person.move_check

        if movement_counter == 0:
            print("I managed to organise in {} iterations".format(evaluation_num))
            break # this needs to stop the simulation
        else:
            pass # continue the loop to for the simulation

        ############################################################
        # right now we will keep it run the whole thing (100 or 200)
        # later we should add the function that checks if no one moved
        # and break
                # check if every one stopped moving
                # if they did break
                # else pass

        evaluation_num += 1
        brain_counter += 1 # this here is very important because brain counter should keep counting!!!

    # I don't know where to put this part!
    # I think it's here!

    ########################
    e.conflict_resolution()

    # check_me
    # brain_counter += 1
    state_of_brain["conflict_need"] = []
    state_of_brain["conflict_desire"] = []
    state_of_brain["notifications"] = envelope.notifications

    for person in people:
        # the first
        state_of_brain[person.name] = [person.activity] + person.claimed_cells
    ########################


    for person in people:
        brain_personal_logs[person.name] = person.personal_log_dict

    # tick is going to be the key for the organized_states
    # it will save the last state that the inner loop
    # THE INSIDE DICTIONARY OF ORGANIZED
    # every tick we save the last organized state of the machine
    organized_states[tick] = state_of_brain # the last state of the brain
    tick += 1

"""
for num in brain_states:
    print(num)
    print(brain_states[num])

for t in organized_states:
    print(t)
    print(organized_states[t])

for line in brain_personal_logs:
    print(line)
"""

for t in brain_personal_logs['person_1']:
    print(t)
    print(brain_personal_logs['person_1'][t])

###########################################
#### writing the file
both_names = "/Users/nourabuzaid/Google Drive/VoxelPlacer/__Output/"+timestr+"rhino_e_{}*{}*{}_seed={}_tick_{}to{}_eval={}.txt".format(x_s, y_s, z_s, seed, tick_start,tick_max,evaluation_max)
#### writing the dictionary into a text file!

#states_file_name = both_names + "_states_dictionary.txt"
file = open(both_names,"w")
file.write("\n")
file.write("#"+both_names)
file.write("\n")
file.write("def states():")
file.write("\n")
file.write("    dict = " + str(brain_states))
file.write("\n")
file.write("    return dict")
file.write("\n")
file.write("a_states = states")
file.write("\n")
file.write("###########################")
file.write("\n")
file.write("#"+both_names + "logs")
file.write("\n")
file.write("def logs():")
file.write("\n")
file.write("    dict = " + str(brain_personal_logs))
file.write("\n")
file.write("    return dict")
file.write("\n")
file.write("b_logs = logs")

###########################################
#### writing the file for c4d
c4d_name = "/Users/nourabuzaid/Google Drive/VoxelPlacer/__Output/"+timestr+"c4d_e_{}*{}*{}_seed={}_tick_{}to{}_eval={}.txt".format(x_s, y_s, z_s, seed, tick_start,tick_max,evaluation_max)

#### writing the dictionary into a text file!
#states_file_name = both_names + "_states_dictionary.txt"
file = open(c4d_name,"w")
file.write(str(brain_states))
