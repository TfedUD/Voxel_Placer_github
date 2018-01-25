
#################################
# 2d
# need 2d
with open('__Input_dictionaries/Dictionary_2d_test_01.txt','r') as inf:
    dict_from_file = eval(inf.read())
need_dictionary = (dict_from_file)

# desire 2d
with open('__Input_dictionaries/Dictionary_2d_test_DESIRE_____________________final.txt','r') as inf:
    dict_from_file = eval(inf.read())
desire_dictionary = (dict_from_file)

#################################
"""
# 3d
# need 3d
with open('Dictionary_3d_test_04.txt','r') as inf:
    dict_from_file = eval(inf.read())
need_dictionary = (dict_from_file)

# desire 3d
with open('Dictionary_3d_test_DESIRE.txt','r') as inf:
    dict_from_file = eval(inf.read())
desire_dictionary = (dict_from_file)


#################################
"""



class Activity_Pattern:
    def __init__(self, activity, position):
        self.activity = activity

        self.position = position

        self.x = position[0]
        self.y = position[1]
        self.z = position[2]


    def need(self):
        # this should return a list of the need positions
        need = []

        # it should read these positions from a dictionary outside
        rhino_positions = need_dictionary[self.activity]

        for position in rhino_positions:
            old_x = position[0]
            old_y = position[1]
            old_z = position[2]

            new_x = int(self.x + old_x)
            new_y = int(self.y + old_y)
            new_z = int(self.z + old_z)

            new_position = (new_x, new_y, new_z)
            need.append(new_position)

        return need


    def desire(self):

        desire = []


        rhino_positions = desire_dictionary[self.activity]

        need_positions = self.need()

        only_desire = [position for position in rhino_positions if position not in need_positions]

        for position in only_desire:
            old_x = position[0]
            old_y = position[1]
            old_z = position[2]

            new_x = int(self.x + old_x)
            new_y = int(self.y + old_y)
            new_z = int(self.z + old_z)

            new_position = (new_x, new_y, new_z)
            desire.append(new_position)

        return desire












#Sleeping_Pattern = Activity_Pattern("Sleeping", position)
#Toilet_Pattern = Activity_Pattern("Toilet use", position)

#Showering_Pattern = Activity_Pattern("Showering", position)


########################

a = Activity_Pattern
