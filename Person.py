
from Schedule import people_dictionary
from New_Patterns_Dictionary import Activity_Pattern

#update test

####################################################


class Person:

    #___________________________________________________
    #________________Attributes?_Methods________________
    #___________________________________________________

    def __init__(self,name, position, envelope):

        self.envelope = envelope
        # position should be (x,y,z)
        self.name = name
        self.position = position
        self.x = self.position[0]
        self.y = self.position[1]
        self.z = self.position[2] # later


        self.destination = None # should be a dictionary key later
        self.destination_dic = {'ground_floor': (None,None,0)}



        self.personal_log_dict = {}
        self.evaluation_num = -1
        self.introduce_person()
        #self.personal_log = []
        #self.personal_log.append("Hey! My name is {}".format(self.name))


        # from old person class:
        t = 0
        self.schedule = people_dictionary()[name]
        self.activity = self.update_activity_pattern_to(t)


        #######
        self.pattern = self.activity_pattern()
        self.claimed_cells = []

        self.conflicts = {}

        self.movement_vector = None

        self.movement_history = []
        self.notification_inbox = []
        self.vectors_away_from_neighbors_NEED = []
        self.vectors_away_from_neighbors_DESIRE = []
        self.vectors_away_from_neighbors_BOTH = []

    def introduce_person(self):

        self.evaluation_num += 1

        self.personal_log_dict[self.evaluation_num] = []
        self.personal_log = self.personal_log_dict[self.evaluation_num]

        self.personal_log.append("Hey! My name is {}".format(self.name))
        self.personal_log.append("___Position Evaluation #: {}".format(self.evaluation_num))
        self.personal_log.append("Destination is: [{}]".format(self.destination))


    def sharing_per_activity(self):

        # this function returns True or Flase
        # True if: my_sharing preference is 1 and this activity is in the sharing list
        # False: if not

        # these are the activities that a person would share?
        # write it somewehre outside?
        sharing_activity_list = [ "Sleep", "Work" ]

        # get my current activity
        my_activity = self.activity
        # check if my current activity is something I would like to share
        if my_activity in sharing_activity_list:
            self.sharing_pref = 1
            self.personal_log.append(" I don't mind sharing '{}' ".format(my_activity))

        else:
            self.sharing_pref = 0
            self.personal_log.append(" I don't like sharing '{}' ".format(my_activity))


    def get_age(self):
        age = 30

        self.age = age
        #return age


    def refresh_claimed(self):
        self.claimed_cells = []


    def refresh_conflicts(self):
        self.conflicts = {}


    def need(self):

        return self.pattern.need()


    def desire(self):

        return self.pattern.desire()


    def need_and_desire(self):
        # initiating an attributes for person called need_and_desire
        #self.need_and_desire_cells = []
        need_and_desire_cells = []
        heirarchy_dictionary = self.pattern_heirarchy()
        for position in heirarchy_dictionary:
            self.need_and_desire_cells.append(position)
        # OUTPUT: positions (x,y) of need_and_desire voxels
        #return self.need_and_desire_cells
        return need_and_desire_cells


    # Karim :)
    def satisfaction(self):
        # evalauate satisfaction here
        # unsatisfied if num of claimed cells < needed cells
        self.satisfaction_log = []

        if len(self.claimed_cells) < len(self.need()):
            status = "Im pissed the fuck off, i need more space mofo"
            satisfaction_level = "I'm " + format(len(self.claimed_cells) / len(self.need()),'.2f') + "% " + "Satisfied"
            happy_level = "I'm 0% " + "happy"

        # satisfied = all need cells claimed
        elif len(self.claimed_cells) == len(self.need()):
            status = "Im satisfied homie"
            satisfaction_level = "I'm 100%" + "Satisfied"
            happy_level = "I'm 0%" + "happy"

        if self.desire():
        # happy =  if any %of desire cells claimed
            if len(self.claimed_cells) / len(self.desire()) > 0.35:
                status = "Im quite happy"
                satisfaction_level = "I'm 100%" + "Satisfied"
                happy_level = "I'm " + format(len(self.claimed_cells) / len(self.desire()),'.2f') + "% " + "Happy"

        # fuckin ecstac = if > 75% of desire cells claimed
            elif len(self.claimed_cells) / len(self.desire()) > 0.65:
                status = "Im fucking exstatic braa"
                satisfaction_level = "I'm 100%" + "Satisfied"
                happy_level = "I'm " + format(len(self.claimed_cells) / len(self.desire()),'.2f') + "% " + "Happy"

            # pure bliss = if == 100# of desire claimed
            elif len(self.claimed_cells) / len(self.desire()) > 0.85:
                status = "I think im gonna throw up im so happy"
                satisfaction_level = "I'm 100%" + "Satisfied"
                happy_level = "I'm " + format(len(self.claimed_cells) / len(self.desire()),'.2f') + "% " + "Happy"


        self.satisfaction_log.append(status)
        self.satisfaction_log.append(satisfaction_level)
        self.satisfaction_log.append(happy_level)


        return self.satisfaction_log

    #___________________________________________________
    #________________Activity_Methods___________________
    #___________________________________________________


    def update_activity_pattern_to(self, time):
        """
        self.evaluation_num += 1


        self.personal_log_dict[self.evaluation_num] = []
        self.personal_log = self.personal_log_dict[self.evaluation_num]

        self.personal_log.append("Hey! My name is {}".format(self.name))
        self.personal_log.append("___Position Evaluation #: {}".format(self.evaluation_num))
        """

        # setting a time attribute
        self.time = time

        # time is a number!
        # every iteration will be five mins for now then!

        # both update the current activity and returns it
        self.activity = self.schedule[time]

        # Leaving building [step 1]: update destination
        # leaving_building
        if self.activity == 'out':
            self.destination = 'ground_floor'
            #print("Destination set to {}".format(self.destination))
            self.personal_log.append("Destination set to {}".format(self.destination))
        # if the activity is something other than out:
        # we make it None? to override out one
        # make sure this doesn't create problems later
        else:
            self.destination = None


        # updating the log!
        self.personal_log.append("___Current Time is: {}".format(self.time))
        self.personal_log.append("My Current Activity is {}".format(self.activity))

        # updating the pattern
        self.pattern = self.activity_pattern()

        return self.activity


    # I need a function that only returns future activity?
    def get_activity_at(self, time):
        return self.schedule[time]


    def get_next_activity(self):
        return self.schedule[self.time + 1]


    def set_activity(self, activity):
        # we're forcing activity?
        # can be usefel in the case of leaving the building
        self.activity = activity


    def set_position(self,position):
        self.position = position
        self.x = self.position[0]
        self.y = self.position[1]
        self.z = self.position[2]


    def activity_pattern_old(self):
        # activity:pattern dictionary
        # find the pattern according to the activity
        # the pattern will be a class! can it be a dictionary?
        # pattern = { "center" : (x,y),
        #             "need"   : [ a list of (x,y) positions],
        #             "desire" : [ a list of (x,y) positions] }
        # would this work or not?
        # chech the way we create the pattern: p = pattern(self.x, self.y)
        # would the (x,y) of need and desire be updated based on the center in dictionary?

        pattern = self.activity_pattern_dict()[self.activity]
        # build the pattern?
        p = pattern(self.x, self.y, self.z)
        # p is a class and not a list of positions
        return p
        #return p.build(p.need()) # do we return p as it is?


    def activity_pattern(self):
        # we should create an instance of Activity_Pattern class
        pattern = Activity_Pattern(self.activity, self.position)
        return pattern


    # This function takes in the current_cloud and the desire cloud,
    # And returns the voxels that are on the border of the current_cloud
    # This funciton represents the gradient of desire functions
    # To implement this correctly, for every time frame, a new layer of desire
    # voxels needs to be added to the current_cloud if there are no conflicts

    def find_immmediate_border(self, current_cloud,target_cloud):
        # both current_cloud and target_cloud are a list of positions
        # returns the positions of the boundary positions of self.
        border_voxels = []
        target_positions_without_current_positions = []
        check_counter = 0

        # 1. for every point in target cloud:
        for position in target_cloud:
            # find all the points that are not inside the current_cloud
            if position not in current_cloud:
            # Append these points to a list "target_cloud_sans_current" current cloud positions
                target_positions_without_current_positions.append(position)
        #print(target_positions_without_current_positions)

        # 2. Here is where we need to check every point in in target_cloud_sans_current
        for position_target in target_positions_without_current_positions:
        # 3. we have have a condition that each point needs to satisfy
            for position_current in current_cloud:
                counter_x = 0
                counter_y  = 0
                counter_z = 0
                # x conditions
                if position_current[0] == position_target[0] \
                or position_current[0] + 1 == position_target[0] \
                or position_current[0] - 1 == position_target[0]:
                    counter_x += 1

                    #print("counter_x",counter_x)
                # y conditions
                if position_current[1] == position_target[1] \
                or position_current[1] + 1 == position_target[1] \
                or position_current[1] - 1 == position_target[1]:
                    counter_y += 1
                    #print("counter_y",counter_y)
                # z conditions
                if position_current[2] == position_target[2] \
                or position_current[2] + 1 == position_target[2] \
                or position_current[2] - 1 == position_target[2]:
                    counter_z += 1

                if counter_x + counter_y + counter_z == 3:
                    border_voxels.append(position_target)



        border_voxels = list(set(border_voxels))

        return border_voxels


    def gradual_pattern_heirarchy(self):
        # wehere to update this thing!!!

        current_cloud = self.claimed_cells + self.need()
        current_cloud = list(set(current_cloud))

        target_cloud = self.desire()
        extra_layer = self.find_immmediate_border(current_cloud,target_cloud)

        all_to_claim = current_cloud + extra_layer
        # what are we going to ask the envelope for is the current cloud (claimed)
        # and the extra layer
        # and they should be in pattern heiracy format
        # so the envelope know where to place 2 and 1

        # we need to sort positions in all_to_claims to need and desire
        actitivy_cell_value = {}

        for position in all_to_claim:
            if position in self.need():
                actitivy_cell_value[position] = 2
            if position in self.desire():
                actitivy_cell_value[position] = 1

        return actitivy_cell_value

    def pattern_heirarchy(self):
        # we are not using this anymore!!!!!!!
        pattern = self.activity_pattern()
        actitivy_cell_value = {}
        # I am setting the values here based on which list the position is in
        # should we do that in the function that reads the matrices?
        for position in pattern.desire():
            actitivy_cell_value[position] = 1

        for position in pattern.need():
            actitivy_cell_value[position] = 2 # make this one 3 later

        return actitivy_cell_value


    def activity_pattern_dict(self):
        # Reads the dictionary of patterns
        dictionary = patterns_dictionary()
        return dictionary


    #___________________________________________________
    #________________Position_Methods___________________
    #___________________________________________________


    """
    Hierarchy for movement decisions!
    1. stay within the building borders
    2. if you have a desired position try to go there
    3. get away from conflicts

    how to integrate these three movements together!
    right now I will start with implementing them in this order
    and see what happens
    they won't be interacting with each other
    I mean that when a person moves toward a destination he's moving in that
    direction even if it will create conflicts!
    maybe his neighbors will try to solve the conflict by moving away from him
    but at the same time what would they do if they went outside the building!

    later every person will have a package from movement to choose within and
    it should be able to make a smart decision based on the evaluation of the
    outcome of every movement

    this will include options like:
    - checking for possible future conflicts if I took this step
    - looking at multiple future generations of the simulation to figure out which
      path to choose in the way to a destination

    >   when does conflict resolutions starts?
        when steps above don't help in reaching a full organized situation?

    >   remember that we need some conflicts!!! these will trigger sharing and
        negotiation scenarios

    """

    # [1]
    def position_inside_envelope_vectors(self, position, pattern, value = "need" ):
        # should take into consideration the same value Conflict vectors is looking
        # for.. desire or need
        # here I am looking at need only

        # these should replace self.x and self.y
        pos_x = position[0]
        pos_y = position[1]
        pos_z = position[2]

        """
        [STEP 1]
        Fidning the min and max x,y coordinates for the pattern cells!
        This is not related to the center yeah?

        With no relation to the envelope yet

        """

        # these values should always be positive
        # we're not talking about rhino x,y
        # but the envelope domain

        envelope_class = self.envelope

        x_min = envelope_class.x_span # this relation to the envelope is arbitrary, I can add any other number "smart one"
        x_max = 0

        y_min = envelope_class.y_span
        y_max = 0

        z_min = envelope_class.z_span
        z_max = 0

        # Thisssssss line!!!!
        # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ #
        #self.pattern = self.activity_pattern()
        #pattern_class = self.pattern
        pattern_class = pattern

        #X# self.personal_log.append("This is the activity pattern {}".format(pattern_class.need()))

        # finding the min-max of x,y for the voxel cloud
        if value == "need":
            for cell in pattern_class.need():
                x = cell[0]
                y = cell[1]
                z = cell[2]

                if x > x_max:
                    x_max = x
                if x < x_min:
                    x_min = x

                if y > y_max:
                    y_max = y
                if y < y_min:
                    y_min = y

                if z > z_max:
                    z_max = z
                if z < z_min:
                    z_min = z


        if value == "desire":
            both = pattern_class.need() + pattern_class.desire()
            for cell in both:
                x = cell[0]
                y = cell[1]
                z = cell[2]

                if x > x_max:
                    x_max = x
                if x < x_min:
                    x_min = x

                if y > y_max:
                    y_max = y
                if y < y_min:
                    y_min = y

                if z > z_max:
                    z_max = z
                if z < z_min:
                    z_min = z


        """
        [STEP 2]
        Finding how many voxels the center needs around
        This is now related to the center or reference point
        How many max cells we have around the center from every directon

        no relation to the envelope yet?

        """
        # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ #
        from_right = x_max - pos_x
        from_left = pos_x - x_min

        from_front = y_max - pos_y
        from_back = pos_y - y_min

        from_up = z_max - pos_z
        from_down = pos_z - z_min


        """
        [STEP 3]
        Finding where to place the center within the envelope now!
        This is all based on the envelope boundries

        These min and max positions values are a kind of domain
        the center should be placed with it so the pattern doesn't have
        any cells outside the envelope

        """

        position_min_x = from_left
        position_max_x = envelope_class.x_span - from_right

        position_min_y = from_back
        position_max_y = envelope_class.y_span - from_front

        position_min_z = from_down
        position_max_z = envelope_class.z_span - from_up


        """
        [STEP 4]

        EVALUATION: we evaluate the current position of the center in relation to
        where it should be based on the previous stage

        IMPORTANT STEP HERE!
        The most important step here would be adding a movement vector to correct
        the position of the position of the center

        instead of printing "go to the left"
        add a vector that goes to the left!
        ______

        General Format for vectors!!!!!
        strings: "left", "right", "down", "up"
        and I can read the equivalent tuple form a dictionary later?

        """

        vectors = []

        # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ #
        if  pos_x < position_max_x \
        and pos_x >= position_min_x \
        and pos_y < position_max_y \
        and pos_y >= position_min_y \
        and pos_z < position_max_z \
        and pos_z >= position_min_z:
            pass
            #print("This is a nice place to settle down!")

            # return True  # shouldn't return True or False, return vectors!

        if pos_x >= position_max_x:
            #print("Go Left!")
            for i in range(int(pos_x - position_max_x)+1):
                vectors.append("left")
            #return False

        if pos_x < position_min_x:
            #print("Go Right!")
            for i in range(int(position_min_x - pos_x)):
                vectors.append("right")
            #return False



        if pos_y >= position_max_y:
            #print("Go Back!")
            for i in range(int(pos_y - position_max_y)+1):
                vectors.append("back")
            #return False

        if pos_y < position_min_y:
            #print("Go Front!")
            for i in range(int(position_min_y - pos_y)):
                vectors.append("front")


        if pos_z >= position_max_z:
            #print("Go Down!")
            for i in range(int(pos_z - position_max_z)+1):
                vectors.append("down")
            #return False

        if pos_z < position_min_z:
            #print("Go Up!")
            for i in range(int(position_min_z - pos_z)):
                vectors.append("up")
            #return False


            #return False
        #X# self.personal_log.append( "I evaluating position based on {} with x and y {} and {}".format(self.position, self.x, self.y))
        #X# self.personal_log.append("And this is what I returned: {}".format(vectors))

        return vectors

    # [2]
    # leaving_building
    def vectors_for_intentional_mov(self):

        if self.destination:


            vectors = self.vectors_toward_a_destination(self.destination)
            self.personal_log.append("These vectors [{}] will take me to my destination [{}]".format(vectors, self.destination))
            return vectors

        else:
            return None

        """
        # this function should return the vectors for the intentional movement
        # these vectors are the ones taking me toward my destination
        # which can be a floor like the ground with z = 0
        # or a neighbor who has a certain position

        # so find the desired_position first

        # we need to find if there's a position preference to start with
        if self.position_pref:
            # then we need to find the type of this position preference
            # it can be the closest_neighbor I want to share activity with
            # or it can be a destination in the buidling like the exit floor

            # let's check if it's a neighbor?
            if self.position_pref == "Exit":
                desired_position = (None, None, 0)
                vectors = self.vectors_toward_a_position(desired_position)
                return vectors

            if self.position_pref = "N":
                # find the neighbor that you will share with

                # we will write a function that returns the neigbor you want to share with
                # neighbor = self.neighbor_to_share_with()

                # desired_position = neighbor.position
                # vectors = self.vectors_toward_a_position(desired_position)
                # return vectors
                pass

        else:
            # there's not intentional movement
            return False
        """


    # IMPORTANT
    def update_position(self):


        if self.movement_vector:
            self.move_according_to(self.movement_vector)
            self.move_check = 1
            ### added today
            self.movement_history.append(self.movement_vector)
        else:
            self.personal_log.append("DID NOT MOVE!")
            self.move_check = 0
        self.personal_log.append("My Current Position is {}".format(self.position))
        #self.personal_log.append("____________")


    def evaluate_position(self, value):
        ### ORDER
        # inside envelope
        # away from conflicts with neighbors
        # move to destination (intentional movement)
        # get away from notifications

        #for line in self.satisfaction():
            #self.personal_log.append(line)


        # This function should only return the vector that
        # person should move according to in the NEXT iteration!
        # write another function for update_position based on that!


        # RUN FUNCTIONS
        self.neighbors_Iam_conflicting_with()
        self.vectors_from_neighbors() # this is both need and desire - won't use it!

        need_neighbors_vectors = self.vectors_away_from_neighbors_NEED # this one comes first
        desire_neighbors_vectors = self.vectors_away_from_neighbors_DESIRE # the last decision to make

        intentional_vectors = self.vectors_for_intentional_mov()
        notifications_vectors = self.vectors_away_from_notifications()


        # I am not comparing the vectors to each other now
        # just forcing the heiracy of these decisions
        # look for vectors in:

        # [1]: stay inside envelope
        if self.position_inside_envelope_vectors(self.position, self.activity_pattern()):
            # move according to that
            vectors = self.position_inside_envelope_vectors(self.position, self.activity_pattern())
            self.personal_log.append("vectors for envelope are [{}]".format(vectors))

            my_vector = self.dominant_vector(vectors)
            self.personal_log.append("I will move [{}] to stay within the envelope!, current position is {}, current x,y,z are: {},{},{}".format(my_vector, self.position, self.x, self.y, self.z))
            #self.move_according_to(my_vector)
            self.movement_vector = my_vector


        # [2]: move away from NEIGHBOR! [IN NEED]
        #neighbors_vectors = self.vectors_from_neighbors()
        elif need_neighbors_vectors:
            self.personal_log.append("NEED NEIGBORS vectors: {}".format(need_neighbors_vectors))
            #self.personal_log.append(need_neighbors_vectors)
            my_vector = self.best_vector(need_neighbors_vectors)

            # check if my_vector has been tried a lot before using it again!

            if len(self.movement_history) > 30 \
            and my_vector == self.movement_history[-2] \
            and my_vector == self.movement_history[-4] \
            and my_vector == self.movement_history[-6] \
            and my_vector == self.movement_history[-8] \
            and my_vector == self.movement_history[-10] \
            and my_vector == self.movement_history[-12] \
            and my_vector == self.movement_history[-14] \
            and my_vector == self.movement_history[-16] \
            and my_vector == self.movement_history[-18] \
            and my_vector == self.movement_history[-20] :


                self.personal_log.append("Vector {} seems to be the best but I tried it before and didn't work! I will try the backup list!".format(my_vector))
                my_backup_vector = self.best_vector(self.backup_vectors)
                self.movement_vector = my_backup_vector

            else:

                #self.personal_log.append("[{}] is the best vector I found but didn't use?!!".format(my_vector))
                self.personal_log.append("I will move [{}] to get away from closest neighbor NEED!".format(my_vector))
                #self.move_according_to(my_vector)
                self.movement_vector = my_vector


        # [3]: go to destination
        # you take one step every iteration so we will use elif
        # leaving_building

        elif intentional_vectors:

            my_vector = self.best_vector(intentional_vectors)
            if self.check_clear_path(my_vector):
                self.personal_log.append("I will move [{}] to go to destination!".format(my_vector))
            #self.move_according_to(my_vector)
                self.movement_vector = my_vector

            else:
                self.personal_log.append("I want to go {} but I can't!".format(my_vector))

        else:
            self.personal_log.append("No need to update position! Staying where I am!")
            self.movement_vector = None


    def best_vector(self, list_of_vectors):

        if list_of_vectors:
            possible_vectors = self.dominant_items_in_list(list_of_vectors)


            #### possible vectors should have one of a kind!!
            #### it can't have two "left"'s for example!
            #### cause we did a previous analysis before we use it as input here!!

            #### this function should return ONE vector eventually!

            # this evaluation process has two steps!
            # FIRST: evaluate the new positions based on these centers


            # every vector should have:
            # a proposed position
            # this proposed position is either inside or outside the envelope
            # this proposed position will consume certain cells

            # so we need to return the vectors whose proposed positions are inside

            positions_by_vectors = {}
            # it will be like = {"left": position, "up": position}
            # so the key is the vector and the value is the position
            # a function that returns a proposed position based on a vector!
            for vector in possible_vectors:
                 positions_by_vectors[vector] = self.position_from_a_vector(vector)



            vectors_keeping_inside = []
            # then we take these positions and check if they are inside
            # we need a funtion that returns if this position is inside or outside the envelope
            # if they are inside we save the vector to the above mentioned list

            for vector in positions_by_vectors: # or possible_vectors, no difference
                proposed_position = positions_by_vectors[vector]
                if self.is_proposed_position_inside_envelope(proposed_position):
                    vectors_keeping_inside.append(vector)
                else:
                    self.personal_log.append("vector {} will move me outside the building!".format(vector))


            if vectors_keeping_inside:


                self.personal_log.append("These vectors keep me inside: {}".format(vectors_keeping_inside))
                ####### what happens if vectors_keeping_inside is empty?
                ####### all the vectors will move me outside?
                ####### then I don't move at all or I move according to least_consuming_value??
                ####### answer_me

                # then we loop through vectors_stay_inside to find

                # the second step is to calculate the value that this position will be consuming
                # we need a function that takes a proposed position and finds how much
                # it consumes (more than the current self.position)


                least_consuming_vectors = []
                least_consuming_value = 1000 # we just need a big number here
                # finding the least comsuming value:


                # I am running these two loops twice and repeating some functions
                # there should be a smarter way of doing that
                for vector in vectors_keeping_inside:

                    #self.personal_log("TESTING VECTOR: {}".format(vector))
                    #self.personal_log("out of {}".format(vectors_keeping_inside))

                    proposed_position = positions_by_vectors[vector]
                    consuming_value = self.consuming_value_of_proposed_position(proposed_position)
                    self.personal_log.append("If I moved {} I will consume {}".format(vector, consuming_value))
                    if consuming_value < least_consuming_value:
                        least_consuming_value = consuming_value

                # finding all the vectors achieving this least consuming value
                for vector in vectors_keeping_inside:
                    proposed_position = positions_by_vectors[vector]
                    consuming_value = self.consuming_value_of_proposed_position(proposed_position)
                    if consuming_value == least_consuming_value:
                        least_consuming_vectors.append(vector)

                # the vector that we will eventually choose is a one that:
                # 1- makes sure we stay inside the envelope
                # 2- consumes the least

                #### this line!
                if len(least_consuming_vectors) == 1:
                    my_best_vector = least_consuming_vectors[0]
                    self.personal_log.append("This is the best step to take: {}".format(my_best_vector))
                    return my_best_vector


                ### if we have more than one vectors with these conditions:
                ### we use self.vector_choice to select one of them!
                if len(least_consuming_vectors) > 1:
                    self.personal_log.append("All of these steps are fine: {}".format(least_consuming_vectors))
                    choosen_vector = self.vector_choice (least_consuming_vectors)
                    self.personal_log.append("I randomly chooses: {}".format(choosen_vector))
                    return choosen_vector

                # would there be a situation when the len(least_consuming_vectors) == 0?
                # this will only happen if len(vectors_keeping_inside) is 0!!!
                if len(least_consuming_vectors) == 0:
                    self.personal_log.append("Check what's wrong with me! I didn't return any vector")
                    return False

            else:
                #print("Gotta use the backup vectors!")
                self.personal_log.append("Gotta use the backup vectors!: {} ".format(self.backup_vectors))
                # this situation happens when vectors_keeping_inside is empty
                # in this case we need to use the backup_vectors
                # we need to repeat the same process
                # that's why we will call the same function within itself
                # using the backup_vectors this time
                return self.best_vector(self.backup_vectors)


        else:
            self.personal_log.append("The backup list is empty? I won't move?")
            #print("The backup list is empty?")



    def position_from_a_vector(self, vector):
        current_position = self.position
        proposed_position = self.position_plus_vector(current_position, vector)

        # returns proposed position as (x, y, z)
        return proposed_position

    # [√]
    def position_plus_vector(self, position, vector):
        x = position[0]
        y = position[1]
        z = position[2]

        if vector == "front":
            y += 1

        if vector == "back":
            y -= 1

        if vector == "right":
            x += 1

        if vector == "left":
            x -= 1

        if vector == "up":
            z += 1

        if vector == "down":
            z -= 1

        new_position = (x, y, z) # add z later

        return new_position


    def pattern_from_proposed_position(self, proposed_position):
        # the input of this method is a position

        # It will return the pattern as a class that contains both need and desire
        # we decide which one we want to use later!!

        # this line returns the pattern CLASS: Sleep or Eat etc
        pattern = Activity_Pattern(self.activity, proposed_position)

        # this line RUNS the pattern on a certain position
        x = proposed_position[0]
        y = proposed_position[1]
        z = proposed_position[2]

        #p = pattern(x, y, z)

        # p is a CLASS and not a list of positions
        return pattern



    def is_proposed_position_inside_envelope(self, proposed_position):
        # this also needs to handle need and desire
        # the main method is still dealing with need only!

        # the way we find that:

        if self.position_inside_envelope_vectors(proposed_position, self.pattern_from_proposed_position(proposed_position) ):
            # this method returns a list of vectors if the position needs to move
            # so in our case if it returned a vector this means that the proposed
            # position is outside!
            return False

        else:
            # if it's none this means the position is fine
            # so for us it should be a good position
            return True

        # the challange here is to make self.position_inside_envelope_vectors()
        # run accoroding to proposed_position and self.pattern_from_proposed_position(proposed_position)!
        # so I need to rewrite the orignial thing so it can be able to take some input
        # when we need that
        # otherwise it should keep using self.position and self.pattern


    def consuming_value_of_proposed_position(self, proposed_position, value = "need"):

        if value == "need":
            old_cells = self.pattern.need()
            new_cells = self.pattern_from_proposed_position(proposed_position).need()

        ##### this part here should be fixed somewhere else
        #### cause desire returns only desire cells and ignore need
        #### shouldn't it return both
        if value == "desire":
            old_cells = self.pattern.desire() + self.pattern.need()
            new_cells = self.pattern_from_proposed_position(proposed_position).desire() + self.pattern_from_proposed_position(proposed_position).need()

        # these are the new positions to consume (important input for check path clear function!!!!)
        positions_to_consume = [cell for cell in new_cells if cell not in old_cells]

        #self.personal_log.append("USING CONSUMING FUNCTION FOR POSITIONS: {}".format(positions_to_consume))

        #self.personal_log.append("I will consume these new positions : {}".format(positions_to_consume))
        # we need to find the equivalent cells for these positions in the envelope
        # and then check the state of these cells and save them to counter
        consuming_counter = 0
        for position in positions_to_consume:
            #cells is attribute of envelope which is a dict of all envelope cells
            if position in self.envelope.cells and position not in self.claimed:
                envelope_cell = self.envelope.cells[position]
                if envelope_cell.state == "Unknown":
                    #self.personal_log.append("Position {} has a conflict and will cost 2".format(position))
                    consuming_counter += 2 # not sure about that
                    #self.personal_log.append("This conflict position updated the counter to {}".format(consuming_counter))
                else:
                    consuming_counter += envelope_cell.state
                    #self.personal_log.append("This position {} updated the counter to {}".format(position, consuming_counter))
                #self.personal_log.append("this position {} has a state of {}".format(position, envelope_cell.state))
            else:
                self.personal_log.append("this position {} is outside the envelope!".format(position))

        #self.personal_log.append("I will be consuming {}".format(consuming_counter))
        return consuming_counter


    # leaving_building
    def check_clear_path(self,vector):
        proposed_position = self.position_from_a_vector(vector)
        activity_cloud = self.pattern_from_proposed_position(proposed_position)
        old_cells = self.pattern.need()
        new_cells = self.pattern_from_proposed_position(proposed_position).need()

        # these are the new positions to consume (important input for check path clear function!!!!)
        positions_to_consume = [cell for cell in new_cells if cell not in old_cells]

        for position in positions_to_consume:
            #cells is attribute of envelope which is a dict of all envelope cells
            if position in self.envelope.cells:
                envelope_cell = self.envelope.cells[position]
                if envelope_cell.state == "conflict_need" or envelope_cell.state == 3:
                    return False
                    # need to check conflict between other people in circulation
                else:
                    return True
            else:
                self.personal_log.append("this position {} is outside the envelope!".format(position))


    def vector_choice(self, possible_vectors):
        # this is a temporary function till we find a better way
        # to choose between all the possible movement vectors!

        # possible_vectors is a list like:
        # possible_vectors = ["left", "back"]

        if self.evaluation_num % 9 == 0:
            vectors_hierarchy = ["right", "left", "front", "back", "up", "down"]

        if self.evaluation_num % 9 == 1:
            vectors_hierarchy = ["right", "left", "up", "down",  "front", "back"]

        if self.evaluation_num % 9 == 2:
            vectors_hierarchy = ["front", "back", "right", "left", "up", "down"]

        if self.evaluation_num % 9 == 3:
            vectors_hierarchy = [ "front", "back", "up", "down", "right", "left",]

        if self.evaluation_num % 9 == 4:
            vectors_hierarchy = [ "up", "down", "right", "left", "front", "back"]

        if self.evaluation_num % 9 == 5:
            vectors_hierarchy = [ "up", "down", "front", "back", "right", "left"]

        ###
        if self.evaluation_num % 9 == 6:
            vectors_hierarchy = ["left", "right", "front", "back", "up", "down"]

        if self.evaluation_num % 9 == 7:
            vectors_hierarchy = ["right", "left","back", "front" , "up", "down"]

        if self.evaluation_num % 9 == 8:
            vectors_hierarchy = ["right", "left", "front", "back", "down", "up"]




        for vector in vectors_hierarchy:
            if vector in possible_vectors:
                selected_vector = vector
                break

        return selected_vector


    def dominant_vector(self, mylist):

        dominent_items = self.dominant_items_in_list(mylist)

        ###### find a better evaluation!
        ###### based on better moves!

        #choosen_vector = self.vector_choice(dominent_items)
        choosen_vector = self.vector_choice(dominent_items)

        return choosen_vector


    def dominant_in_list(self, mylist):

        # making the counters_dict
        counters_dict = {}
        for item in mylist:
            counters_dict[item] = 0

        # Counting
        for item in mylist:
            counters_dict[item] += 1

        max_counter = 0

        for item in counters_dict:
            if counters_dict[item] >= max_counter:
                max_counter = counters_dict[item]

        dominent_items = []

        for item in counters_dict:
            if counters_dict[item] == max_counter:
                dominent_items.append(item)

        ###### find a better evaluation!
        ###### based on better moves!
        random_dominent = dominent_items[0]

        for item in mylist:
            if item in dominent_items:
                the_item = item
        return the_item


    def dominant_items_in_list(self, mylist):

        # making the counters_dict
        counters_dict = {}
        for item in mylist:
            counters_dict[item] = 0

        # Counting
        for item in mylist:
            counters_dict[item] += 1

        max_counter = 0

        for item in counters_dict:
            if counters_dict[item] >= max_counter:
                max_counter = counters_dict[item]

        dominent_items = []

        for item in counters_dict:
            if counters_dict[item] == max_counter:
                dominent_items.append(item)

        return dominent_items


    def move_according_to(self, vector):
        # move the center according to a vector!
        if vector == "front":
            self.y += 1
            self.personal_log.append("I MOVED FRONT")

        if vector == "back":
            self.y -= 1
            self.personal_log.append("I MOVED BACK")

        if vector == "right":
            self.x += 1
            self.personal_log.append("I MOVED RIGHT")

        if vector == "left":
            self.x -=1
            self.personal_log.append("I MOVED LEFT")

        if vector == "up":
            self.z += 1
            self.personal_log.append("I MOVED UP")

        if vector == "down":
            self.z -= 1
            self.personal_log.append("I MOVED DOWN")


        # this line turned out to be very important!!
        # fix the relation between self.x, self.y and self.position !
        self.position = (self.x, self.y, self.z)



    def neighbors_Iam_conflicting_with(self):
        # uses conflicts to find neighbors

        neighbors_names = []
        self.neighbors_as_objects = []
        self.neighbors_in_need = []
        self.neighbors_in_desire = []

        if self.conflicts:

            # in this loop we're reading names to append them to the log
            for position in self.conflicts:

                # the one using the readable version
                conflict_value = self.envelope.cells_in_conflict_readable()[position][0]
                names = self.envelope.cells_in_conflict_readable()[position][1]

                # saving the others names only not mine!
                for name in names:
                    if self.name != name:
                        neighbors_names.append(name)


            # finding out which conflicts are need and which are desire

            #for position in self.conflicts:
                # THIS IS THE PART I AM returning NOW!
                # the one using classes version
                cell_object = self.envelope.cells[position]

                conflict_value = self.envelope.cells_in_conflict()[cell_object][0]
                conflicting_people = self.envelope.cells_in_conflict()[cell_object][1]

                # all conflicts no matter need or desire
                for person in conflicting_people:
                    if person.name != self.name:
                        self.neighbors_as_objects.append(person)
                    self.personal_log.append("all conflicts with [{}]".format([p.name for p in self.neighbors_as_objects ]))

                # need conflicts
                if conflict_value == 2:
                    for person in conflicting_people:
                        if person.name != self.name:
                            self.neighbors_in_need.append(person)
                    self.personal_log.append("NEED conflict with [{}]".format([p.name for p in self.neighbors_in_need ]))


                # desire conflicts
                if conflict_value == 1:
                    for person in conflicting_people:
                        if person.name != self.name:
                            self.neighbors_in_desire.append(person)
                    self.personal_log.append("DESIRE conflict with [{}]".format([p.name for p in self.neighbors_in_desire]))



        else:
            self.personal_log.append("I don't have any conflicts with my neighbors!")
            return False


    def closest_neighbors(self, all_neighbors):
        #all_neighbors = self.neighbors_Iam_conflicting_with()

        # now the closest neighbors can be more than one person!
        the_closest_neighbors = self.dominant_items_in_list(all_neighbors)

        tag = " My closest neighbor/s is/are {}".format([ n.name for n in the_closest_neighbors] )
        #  and its position is {} , the_closest_neighbors.position
        #if tag not in self.personal_log:
        self.personal_log.append(tag)

        # we are returning all closest neighbors
        # can be more than one!
        return the_closest_neighbors


    def neighbor_to_share_with(self):
        # this function should look at my closest neigbor or neigbors [a list]
        # and check if there's a neigbor to share activity with
        # based on our current activities and willing to share

        # make sure I want to share first
        #if self.sharing_per_activity():
            # then go through the neigbors list and see who would and see who is a good neighbor to share with
        pass


    def vectors_away_from_a_position(self, position):
        # so the input is one position only not a list
        # should be the neighbor.position
        # returns all the possible vectors away from a position

        if position:
            possible_vectors = []

            # the x
            if position[0] > self.x:
                vector = "left"
                possible_vectors.append(vector)

            if position[0] < self.x:
                vector = "right"
                possible_vectors.append(vector)

            # the y
            if position[1] > self.y:
                vector = "back"
                possible_vectors.append(vector)

            if position[1] < self.y:
                vector = "front"
                possible_vectors.append(vector)


            # the z
            if position[2] > self.z:
                vector = "down"
                possible_vectors.append(vector)

            if position[2] < self.z:
                vector = "up"
                possible_vectors.append(vector)

            if possible_vectors:
                return possible_vectors

            else:
                #print("for some reason I recieved a position but couldn't return a vector!")
                #print("I think it's because I have the exact position of my neigbor!")
                return False

        else:
            print("You did not enter a valid position?!")
            return False

    # Karim
    def vectors_toward_a_position(self, position):
        # so the input is one position only not a list
        # should be the neighbor.position
        # returns all the possible vectors towards from a position

        if position:
            possible_vectors = []

            # the x
            if position[0] > self.x:
                vector = "right"
                possible_vectors.append(vector)

            if position[0] < self.x:
                vector = "left"
                possible_vectors.append(vector)

            # the y
            if position[1] > self.y:
                vector = "front"
                possible_vectors.append(vector)

            if position[1] < self.y:
                vector = "back"
                possible_vectors.append(vector)


            # the z
            if position[2] > self.z:
                vector = "up"
                possible_vectors.append(vector)

            if position[2] < self.z:
                vector = "down"
                possible_vectors.append(vector)

            if possible_vectors:
                return possible_vectors

            else:
                #print("for some reason I recieved a position but couldn't return a vector!")
                #print("I think it's because I have the exact position of my neigbor!")
                return False

        else:
            print("You did not enter a valid position?!")
            return False


        #pass


    def vectors_toward_a_destination(self, des_key):
        # so the input is one position only not a list
        # should be the neighbor.position
        # returns all the possible vectors towards from a position
        # instead of having a certain position to go to
        # you have a general destination
        # like the ground floor (for exit)
        # or the top of the building for a view or something

        # so we have a z preference: z == 0 for the ground
        # keep moving down till z == 0
        #self.destination_dic = {'ground_floor': (None,None,0)}
        if des_key in self.destination_dic:
            floor = self.destination_dic[des_key]
            #print("The destination (floor) I should go to is {}".format(floor))
            possible_vectors = []

            # the x
            if floor[0] != None:
                if floor[0] > self.x:
                    vector = "right"
                    possible_vectors.append(vector)

                if floor[0] < self.x:
                    vector = "left"
                    possible_vectors.append(vector)

            # the y
            if floor[1] != None:
                if floor[1] > self.y:
                    vector = "front"
                    possible_vectors.append(vector)

                if floor[1] < self.y:
                    vector = "back"
                    possible_vectors.append(vector)

            # the z
            if floor[2] != None:
                if floor[2] > self.z:
                    vector = "up"
                    possible_vectors.append(vector)

                if floor[2] < self.z:
                    vector = "down"
                    possible_vectors.append(vector)

                #should i be adding a condition that says floor[2] == self.z
                #in which case dont chance z anymore?
                #not sure if this is already gonna do that


            if possible_vectors:
                return possible_vectors
                #print("vectors for destination returned these [{}]".format(possible_vectors))

            else:
                #print("for some reason I recieved a position but couldn't return a vector!")
                #print("I think it's because I have the exact position of my neigbor!")
                return False

        else:
            print("You did not enter a valid destination?!")
            return False

            #pass


    def vectors_from_neighbors(self):
        # in order not to run these functions more than one time!!
        #self.backup_vectors = []
        all_neighbors = self.neighbors_Iam_conflicting_with()

        # this part needs more evaluation!
        all_vectors = []

        if all_neighbors:
            closest_neighbors = self.closest_neighbors(all_neighbors)

            for neighbor in closest_neighbors:
                vectors = self.vectors_away_from_a_position(neighbor.position)
                #print("vectors away", vectors)
                if vectors:
                    all_vectors += vectors

            if all_vectors:
                dominant_vectors = self.dominant_items_in_list(all_vectors)


                self.backup_vectors = []
                for vector in all_vectors:
                    if vector not in dominant_vectors:
                        self.backup_vectors.append(vector)


                self.personal_log.append("These are dominant vectors away from neighbors {}".format(dominant_vectors))
                self.vectors_away_from_neighbors = dominant_vectors
                #print("These are dominant vectors away from neighbors {}".format(dominant_vectors))
                return dominant_vectors

            else:
                #print("I have neighbors but couldn't return vectors! why?!")
                return False
                #print("all_neighbors", all_neighbors)
                #print("all_vectors", all_vectors)

        else:
            self.personal_log.append("I don't have a close neighbor at the moment!")
            return False


    def notify_neighbor(self):
        # this function should send a notification for the neighbor we're trying to pass through
        # this means every person should have a personal attribute called self.notification
        # and this function will append stuff to this list
        # what are these stuff? what should self.notification include?

            # the positions that I want my neighbor to clear out
            # or the vectors that the neigbor should try to move to?

            # in both cases we need to write a function that finds the vector
            # a person should move to in order to clear out some positions
            # should it be perpendicular to the center, notification axis??
            # think about it!

        # eventually in evaluate position we will add the list of vectors
        # at the end of the decisions sequence and person

        pass



    #___________________________________________________
    #________________Evaluation_Methods_________________
    #___________________________________________________

    """
    What are the stuff the we need to evaluate for every person and for the
    system in general?

    PERSON:
    - how much it has acclaimed from its need or desire
    - does it have conflicts? what kind and with who
    - satisfaction about the position within the building

    its future moves:
    - does it create more conflicts?
    - in conflicts [ONLY ONE OF THE PEOPLE SHOULD MOVE!] how to find out how?
    - is it part of the negotiation model?
    - or part of the evaluation of options of every person? what will happen if
      any moved?
    - or is it part of the overall evaluation of the whole system.. like what is
      the best movement for everyone together!



    ENVELOPE:
    - is the envelope big enough to accomodate desires or only needs?

    - how to write a function that looks into the future.. I alreaday have
      place_people so what I can do is:
      - I don't have a relation with time!!!!!
      - people are not related to time in my Person class
      - should I take this step now or what?
      - is Person always defined by time?
      - how would that change the way everything is written?
      - currently the only function that uses time in person is activity_per_time
      - we use time to update the position of the people and then the way they're placed
      - there's no need to bring time inside Person class
      - do I write a new class for Evaluation?
                - in this class we run the different scenarios and give the
                  best option? wouldn't that create more mess?

      def evaluate_future()


    """



###################################################################
