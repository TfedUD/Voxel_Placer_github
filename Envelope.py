
from Envelope_Cell import Envelope_Cell

###################################################################

class Envelope:


    def __init__(self, x_span, y_span, z_span):
        self.x_span = x_span
        self.y_span = y_span
        self.z_span = z_span
        self.cells = self.create_cells() # a dictionary


    def create_cells(self):

        cells = {}

        for x in range(self.x_span):
            for y in range(self.y_span):
                for z in range(self.z_span):
                # add z later
                    cells[x,y,z] = Envelope_Cell((x,y,z)) # add z
        # returns a dictionary
        return cells


    def evaluate_states(self):
        # 1. total size aka num of voxels
        x = self.x_span
        y = self.y_span
        z = self.z_span
        total_size = x*y*z
        # 2. number of needed voxels
        needed_cells = self.num_of_needed_cells
        # 3. number allocated cells
        amount_allocated = len(self.allocated_cells())
        # 4. number of cells in conflict
        amount_conflict = len(self.cells_in_conflict_attr)
        # 5. number of empty cells
        amount_empty = len(self.empty_cells_readable())

        self.personal_log = []
        self.personal_log.append("Total size aka #of voxels is {}".format(total_size))
        self.personal_log.append("Total # of needed voxels is {}".format(needed_cells))
        self.personal_log.append("Total # of allocated voxels is {}".format(amount_allocated))
        self.personal_log.append("Total # of conflict voxels is {}".format(amount_conflict))
        self.personal_log.append("Total # of empty voxels is {}".format(amount_empty))
        return self.personal_log

    #___________________________________________________
    #________________Initial_Evaluation_________________
    #___________________________________________________


    def all_cells_evaluation(self, people):

        # the goal of this function is returning dictionaries with this format:
        # "KEY = cell" : "VALUE = {another dictionary whose key is a person and value is hierarchy number}
        # example:
        # cells_status = { cell_1 :{ person_1 : 2, person_2 : 1, person_3: 2},
        #                  cell_2 :{ person_5 : 3},
        #                  cell_3 :{ person_4 : 3, person_8 : 1} ,
        #                  cell_4 :{ person_7 : 1, person_9 : 2}   }

        # TWO DICTIONARIES
        # the first dictionary uses instances of cell class and person class
        # > so it's hard to read!
        # we create another dictionary with the cell coordinates and person name
        # > just to make it easy to understand what's going on
        cells_status = {}
        cells_status_readable = {}

        # initiating an empty dictionary for every cell in the envelope
        for key in self.cells:
            # outside dictionary: cell : persons_claiming
            cells_status[self.cells[key]] = {}
            cells_status_readable[self.cells[key].position] = {}


        #### filling these empty dictionary with people trying to claim the cell
        #### creating the dictionary in dictionary
        self.num_of_needed_cells = 0

        for person in people:

            # this is a part I added to calculate how many cells we need per time
            person_need = person.need()
            self.num_of_needed_cells += len(person_need)

            pattern_heirarchy = person.pattern_heirarchy()

            for key in pattern_heirarchy:
                ###### I overlooked ==
                ###### half of our scenarios happen when cells have the same value
                ###### find out how to incorporate that!!
                if key in self.cells:
                    envelope_cell = self.cells[key]
                    pattern_cell_state = pattern_heirarchy[key]

                    # outside dictionary: cell : persons_claiming
                    # inside dictionary: person: claiming_value
                    # adding new keys
                    cells_status[envelope_cell][person] = pattern_cell_state
                    cells_status_readable[envelope_cell.position][person.name] = pattern_cell_state


                    # updating the grid cells states
                    # > according to the placed patterns
                    #### DO WE NEED THIS PART HERE?
                    ### THE LINE AFTER
                    envelope_cell.state = pattern_cell_state
                    #person.cells_status.append(key)


        return [cells_status, cells_status_readable]


    def claimed_cells(self):
        people = self.people
        # CLEANING DICTIONARIES
        # Deleting the cells with empy dictionaries in claimed_cells

        # instead of deleting items from the first dictionary
        # save the cells we want to a new one!
        all_cells = self.all_cells_evaluation(people)[0]
        claimed_cells = {}
        for key in all_cells:
            people_claiming = all_cells[key]
            if len(people_claiming) > 0:
                claimed_cells[key] = people_claiming
        return claimed_cells


    def claimed_cells_readable(self):

        people = self.people
        # Deleting the cells with empy dictionaries in claimed_cells_readable
        # instead of deleting items from the first dictionary
        # save the cells we want to a new one!
        all_cells = self.all_cells_evaluation(people)[1]
        claimed_cells_readable = {}
        for key in all_cells:
            people_claiming = all_cells[key]
            if len(people_claiming) > 0:
                claimed_cells_readable[key] = people_claiming
        return claimed_cells_readable


    # Karim:
    # a function that returns the empty cells that no one tried to claim
    # it will look like claimed_cells() above but with some changes

    def empty_cells(self):
        people = self.people
        all_cells = self.all_cells_evaluation(people)[0]
        empty_cells = []
        for key in all_cells:
            if all_cells[key] == {}:
                empty_cells.append(key)
        return empty_cells


    def empty_cells_readable(self):
        people = self.people
        all_cells = self.all_cells_evaluation(people)[1]
        empty_cells = []
        for key in all_cells:
            if all_cells[key] == {}:
                empty_cells.append(key)
        return empty_cells


    def refresh_cells_states(self):
        for position in self.cells:
            cell = self.cells[position]
            cell.state = 0

    #___________________________________________________
    #________________Main_Method________________________
    #___________________________________________________


    def place_people(self, people):
        # people are a list of person classes/objects
        # can I define a global variable inside a function?
        self.people = people

        #### clean people before placing them!!!!
        for person in people:
            ##### refresh person here?
            person.refresh_claimed()
            #### this refreshes person's conflicts
            #### not the conflic list in the envelope!
            person.refresh_conflicts()

        #### nope!
        #### we need to refresh the envelope too!!!
        self.refresh_cells_states()

        ######
        claimed_cells = self.claimed_cells()

        #############
        # ALLOCATING CELLS - FINDING CELLS IN CONFLICT
        #############
        # all the claimed cells will either go to one person
        # become allocated
        # or become in conflict

        allocated_cells = {}
        cells_in_conflict = {}

        ######

        """
        now before starting this stage we already know that some cells are claimed by one person
        so we can append these to a differnt list first
        and go through the rest
        if the max_priority has one person then the cell goes to him > no conflict
        else we have a conflict

        so we have three scenerios
        a. one person only tries to claim and takes the cell
        b. more than one person but one with higher priority so he takes it
        c. conflict

        the thing I did below does not differentiate between cases a & b
        - do we want to differentiate between them though?
        doesn't sound bad!
        > maybe in the simulation we can show this part when one priority overrides
        the other
        > maybe this will also help to fix the issues with cells_in_conflict
        order of appearing? not sure if related or not

        """

        for cell_key in claimed_cells:
            ### finding the highest claiming value = priority
            cell_claimers = claimed_cells[cell_key]

            # case 'a'
            if len(cell_claimers) == 1:
                for person in cell_claimers: # for one time!
                    person.claimed_cells.append(cell_key.position)
                    # updating the cell status
                    priority = cell_claimers[person]
                    cell_key.state = priority

                    allocated_cells[cell_key] = ["Without Conflict", person.name ]


            elif len(cell_claimers) > 1:

                conflicting_people = [] # peopel trying to claim the same cell with max_priority
                max_priority = 0

                # finding the max_priority first
                for person in cell_claimers:
                    priority = cell_claimers[person]
                    # just sorting the numbers here to find max_priority
                    if priority > max_priority:
                        max_priority = priority

                # finding all the people having this max_priority
                for person in cell_claimers:
                    priority = cell_claimers[person]
                    # finding how many people match max_priority
                    if priority == max_priority:
                        conflicting_people.append(person)
            #####
                # if only one person has this priority
                # case 'b'
                if len(conflicting_people) == 1:
                    # this person with max_priority wins the cell
                    # the cells goes to conflicting_people[0]
                    # updating the person status
                    the_only_person = conflicting_people[0]
                    the_only_person.claimed_cells.append(cell_key.position)
                    # updating the cell status
                    allocated_cells[cell_key] = ["Overruled", the_only_person.name]
                    cell_key.state = max_priority

                # if more than one have this priority
                elif len(conflicting_people) > 1:
                    #cells_in_conflict.append(cell_key) # yes or no?
                    """
                    #This part is not necessary here
                    names = []

                    for person in conflicting_people:
                        names.append(person.name)
                    """
                    cells_in_conflict[cell_key] = [max_priority, conflicting_people]
                    cell_key.state = "Unknown"

                    ###
                    ### what does this part do?
                    for person in conflicting_people:
                        person.conflicts[cell_key.position] = max_priority

                    # the cell goes to the cells_in_conflict dictionary
                    # this is a temporary dictionary till we figure out what to do with the conflict

        #return [allocated_cells, cells_in_conflict]
        #### is this here a good idea or not!!!
        self.allocated_cells_attr = allocated_cells
        self.cells_in_conflict_attr = cells_in_conflict



    def allocated_cells(self):
        #return self.place_people(self.people)[0]
        return self.allocated_cells_attr


    def cells_in_conflict(self):
        #return self.place_people(self.people)[1]
        return self.cells_in_conflict_attr


    def allocated_cells_readable(self):
        readable_dictionary = {}
        #dictionary =  self.place_people(self.people)[0]
        dictionary = self.allocated_cells_attr
        for cell in dictionary:
            readable_dictionary[cell.position] = dictionary[cell]
        return readable_dictionary


    def cells_in_conflict_readable(self):
        readable_dictionary = {}
        #dictionary =  self.place_people(self.people)[1]
        dictionary = self.cells_in_conflict_attr
        for cell in dictionary:
            value = dictionary[cell][0]
            conflicting_people = dictionary[cell][1]
            names = []
            for person in conflicting_people:
                names.append(person.name)
            readable_dictionary[cell.position] = [value, names]
        return readable_dictionary



###################################################################
