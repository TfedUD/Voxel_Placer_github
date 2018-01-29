from Person import Person
from Envelope import Envelope
from Schedule import people_dictionary
import random as r
import time

timestr = time.strftime("%Y%m%d-%H%M")
#print(timestr)
#################################################
#### Run Function ####
seed = 12
r.seed(seed)

# INPUT
mytick = 105   # what column in the schedule
ticks = 100   # how many times the brain runs
#########
x_s = 28 #28
y_s = 9 #9
z_s = 28 #28

value = "need"  # "desire"
#################################################
# random points generator

#points =  [(23, 0, 31), (31, 0, 28), (16, 0, 25), (25, 0, 0), (27, 0, 0), (6, 0, 19), (32, 0, 19), (27, 0, 7), (16, 0, 19), (12, 0, 31), (23, 0, 16), (36, 0, 10), (3, 0, 0), (4, 0, 27), (17, 0, 4), (14, 0, 11), (24, 0, 25), (22, 0, 10)]

points = []
for i in range(18):
    x = r.randint(0,x_s)
    y = r.randint(0,y_s)
    z = r.randint(0,z_s)
    point = (x, y, z)
    points.append(point)
print("points1", points)

####################################################
# BEFORE starting the time loop
# we need to create the Envelope and the People outside the time LOOP
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
####################################################
####################################################
####################################################
# STARTING THE TIME LOOP
states_of_machine = {}
all_personal_logs = {}
need_dict = {}
desire_dict = {}

for tick in range(ticks):

    states_of_machine[tick] = {}
    need_dict[tick] = {}
    desire_dict[tick] = {}

    timestr_2 = time.strftime("%Y%m%d-%H%M")
    print(timestr_2," : " ,tick)

    # [STEP 1]: Updating people
    # introduce_person
    for person in people_classes:
        person.introduce_person()

    # UPDATE POSITION
    for person in people_classes:
        person.update_position()

    # UPDATE ACTIVITY
    for person in people_classes:
        person.update_activity_pattern_to(mytick)


    # [STEP 2]: Placing the poeple in the envelope
    # Update the envelope and claimed cells by placing people
    e.place_people(people_classes)
    """
    for line in e.evaluate_states():
        print(line)
    print("___________")
    """

    for person in people_classes:
        person.evaluate_position(value)


    # [STEP 4]: outputting
    # every iteration we output the current state of the envelope and people!
    # all as OBJECTS/CLASSES
    envelope = e             # envelope as a state of the machine
    people = people_classes  # outputting people!


    inside_dictionary = states_of_machine[tick]
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
    inside_dictionary["conflict_need"] = conflict_list_need
    inside_dictionary["conflict_desire"] = conflict_list_desire

    inside_dictionary["notifications"] = envelope.notifications
    #print(envelope.notifications)

    for person in people:
        # the first
        inside_dictionary[person.name] = [person.activity] + person.claimed_cells
        #inside_log_dictionary[person.name] = person.personal_log

    # check_me : all need inside the main dictioanry
    all_need = []
    for person in people:
        # check_me
        personal_need = person.need()
        for position in personal_need:
            if position in person.claimed_cells:
                all_need.append(position)
    inside_dictionary["all_need"] = all_need


    # NEED DICTIONARY
    person_need_dict = need_dict[tick]
    for person in people:
        person_need_dict[person.name] = person.need()
        #print("person need", person.need_cells)

    # DESIRE DICTIONARY
    person_desire_dict = desire_dict[tick]
    for person in people:
        person_desire_dict[person.name] = person.desire()
        #print("person need", person.need_cells)



print("_________________")


################################
################################
################################
e.conflict_resolution()

states_of_machine[ticks] = {}
inside_dictionary = states_of_machine[ticks]
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
inside_dictionary["conflict_need"] = conflict_list_need
inside_dictionary["conflict_desire"] = conflict_list_desire

inside_dictionary["notifications"] = envelope.notifications
#print(envelope.notifications)

for person in people:
    # the first
    inside_dictionary[person.name] = [person.activity] + person.claimed_cells
    #inside_log_dictionary[person.name] = person.personal_log

# check_me : all need inside the main dictioanry
all_need = []
for person in people:
    # check_me
    personal_need = person.need()
    for position in personal_need:
        if position in person.claimed_cells:
            all_need.append(position)
inside_dictionary["all_need"] = all_need


# NEED DICTIONARY
person_need_dict = need_dict[tick]
for person in people:
    person_need_dict[person.name] = person.need()
    #print("person need", person.need_cells)

# DESIRE DICTIONARY
person_desire_dict = desire_dict[tick]
for person in people:
    person_desire_dict[person.name] = person.desire()
    #print("person need", person.need_cells)
################################
################################
################################


###########################
# personal_log dictionary
for person in people:
    all_personal_logs[person.name] = person.personal_log_dict

#### writing the file

#both_names = "/Users/karimdaw/Google Drive/VoxelPlacer/__Output/"+timestr+"rhino_tick_{}*{}_e_{}*{}*{}_seed={}_value={}.txt".format(mytick,ticks, x_s, y_s, z_s, seed, value)
both_names = "/Users/nourabuzaid/Google Drive/VoxelPlacer/__Output/"+timestr+"rhino_tick_{}*{}_e_{}*{}*{}_sd={}_val={}.txt".format(mytick,ticks, x_s, y_s, z_s, seed, value)
#### writing the dictionary into a text file!

#states_file_name = both_names + "_states_dictionary.txt"

file = open(both_names,"w")

file.write("#"+both_names + "states")
file.write("\n")
file.write("def states():")
file.write("\n")
file.write("    dict = " + str(states_of_machine))
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
file.write("    dict = " + str(all_personal_logs))
file.write("\n")
file.write("    return dict")
file.write("\n")
file.write("b_logs = logs")
file.write("###########################")
file.write("\n")
file.write("#"+both_names + "need_dict")
file.write("\n")
file.write("def need_pos():")
file.write("\n")
file.write("    dict = " + str(need_dict))
file.write("\n")
file.write("    return dict")
file.write("\n")
file.write("c_need = need_pos")
file.write("###########################")
file.write("\n")
file.write("#"+both_names + "desire_dict")
file.write("\n")
file.write("def desire_pos():")
file.write("\n")
file.write("    dict = " + str(desire_dict))
file.write("\n")
file.write("    return dict")
file.write("\n")
file.write("c_desire = desire_pos")
####################################################

####################################################

# writing files for c4d
#c4d_name = "/Users/karimdaw/Google Drive/VoxelPlacer/__Output/"+timestr+"c4d_tick_{}*{}_e_{}*{}*{}_seed={}_value={}.txt".format(mytick,ticks, x_s, y_s, z_s, seed, value)
c4d_name = "/Users/nourabuzaid/Google Drive/VoxelPlacer/__Output/"+timestr+"c4d_tick_{}*{}_e_{}*{}*{}_seed={}_value={}.txt".format(mytick,ticks, x_s, y_s, z_s, seed, value)
#### writing the dictionary into a text file!
#states_file_name = both_names + "_states_dictionary.txt"

file = open(c4d_name,"w")
file.write(str(states_of_machine))

####################################################
log_name = "/Users/nourabuzaid/Google Drive/VoxelPlacer/__Output/"+timestr+"c4d_tick_{}*{}_e_{}*{}*{}_seed={}_value={}_log.txt".format(mytick,ticks, x_s, y_s, z_s, seed, value)
#### writing the dictionary into a text file!
file = open(log_name,"w")
file.write(str(all_personal_logs))

####################################################

"""
for i in range(ticks):
    print("++++++++++++++++++++")
    print (i)
    all_list = all_personal_logs["person_15"][i]
    for line in all_list:
        print(line)
"""
points2 = []
for person in people:
    points2.append(person.position)

print("points2", points2)
