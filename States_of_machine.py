from Person import Person
from Envelope import Envelope
from Schedule import people_dictionary
import random as r

###################################################################
# these are from New_Patterns_Dictionary



#### Run Function ####




# INPUT
seed = 11
r.seed(seed)


x_s = 32 #28
y_s = 1 #9
z_s = 32 #28


# random points generator
points = []

for i in range(18):
    x = r.randint(0,x_s)
    y = r.randint(0,y_s)
    z = r.randint(0,z_s)

    point = (x, y, z)
    points.append(point)

print("points", points)


#points = [(12, 6, 1), (8, 8, 15), (12, 4, 15), (11, 9, 6), (16, 2, 9), (4, 1, 8), (17, 9, 4), (9, 1, 2), (10, 7, 17), (3, 5, 13), (10, 9, 6), (17, 7, 14), (16, 4, 1), (17, 0, 2), (12, 0, 15), (10, 3, 10), (2, 3, 18), (7, 3, 4)]

mytick = 105

#print(points)
#points = [ (2,3,3), (3,5,2), (4,6,5), (5,9,8), (2,3,3), (3,5,2), (4,6,5), (5,9,8), (2,3,3), (3,5,2), (4,6,5), (5,9,8), (2,3,3), (3,5,2), (4,6,5), (5,9,8), (2,3,3), (3,5,2) ]
factor = 1
ticks = 50 * factor

####################################################

#need_dictionary = get_need_dictionary()

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

#############


# STARTING THE TIME LOOP

states_of_machine = {}
all_personal_logs = {}


for tick in range(ticks):

    states_of_machine[tick] = {}
    #tick +=1
    #print(tick)

    # [STEP 1]: Updating people

    # introduce_person
    for person in people_classes:
        person.introduce_person()


    # UPDATE POSITION
    # based on the evaluation of previous iteration
    # (for the first iteration we take the initial position)
    for person in people_classes:
        person.update_position()


    # UPDATE ACTIVITY
    # This factor is for determining how often we change activity!
    #factor = 1 # it means every x iteration
    for person in people_classes:
        if tick % factor == 0:
            #print("After factor time is ", tick)
            person.update_activity_pattern_to(mytick)
            #person.update_activity_pattern_to(int(tick/factor))



    # [STEP 2]: Placing the poeple in the envelope
    # Update the envelope and claimed cells by placing people
    e.place_people(people_classes)
    for line in e.evaluate_states():
        print(line)
    print("___________")
    #print("num_of_needed_cells: " , e.num_of_needed_cells)
    #print("num_of_claimed_cells", )
    #print("num_of_empty_cells", len(e.empty_cells()))


    # [STEP 3]: People Evaluation of what they got!

    # a - evaluating Satisfaction
    # we did not write this part yet

    # b - evaluating Position

    # the evaluation can be based on need or desire
    # every person will evaluate its current position
    # if it needs to move it will return a movement vector
    for person in people_classes:
        person.evaluate_position("need")


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
        if conflict_dict[key][0] == 2:
            conflict_list_need.append(key.position)
        if conflict_dict[key][0] == 1:
            conflict_list_desire.append(key.position)
    inside_dictionary["conflict_need"] = conflict_list_need
    inside_dictionary["conflict_desire"] = conflict_list_desire

    for person in people:
        # the first
        inside_dictionary[person.name] = [person.activity] + person.claimed_cells
        #inside_log_dictionary[person.name] = person.personal_log


print("_________________")

#print(states_of_machine)


for person in people:
    all_personal_logs[person.name] = person.personal_log_dict

#### writing the file

both_names = "/Users/nourabuzaid/Google Drive/VoxelPlacer/__Output/rhino_tick_{}*{}_e_{}*{}*{}_seed={}.txt".format(mytick,ticks, x_s, y_s, z_s, seed)
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
####################################################

####################################################

# writing files for c4d

c4d_name = "/Users/nourabuzaid/Google Drive/VoxelPlacer/__Output/c4d_tick_{}*{}_e_{}*{}*{}_seed={}.txt".format(mytick,ticks, x_s, y_s, z_s, seed)
#### writing the dictionary into a text file!
#states_file_name = both_names + "_states_dictionary.txt"

file = open(c4d_name,"w")
file.write(str(states_of_machine))

####################################################
