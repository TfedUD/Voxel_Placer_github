

# ;sldjkflaksdfj
###################################################################

class Envelope_Cell:


    def __init__(self, position):
        # position should be a tuple of (x,y,z)
        # state
        self.state = 0 # start with empty

        # position
        self.position = position
        self.x = position[0]
        self.y = position[1]
        self.z = position[2]

    # not used
    def update_state(self, state):
        self.state = state

###################################################################

print (‘/x1b[0;32;48m’ + “Succesfully Finished” + ‘/x1b[0m’)
