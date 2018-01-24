
"""
[√] TO-DO 2018:
_______________
To do for 06-01-2018:

 >  fix need/desire issue
 >  when people have the same y they don't consider going up or down
    although it may solve some problems! look for the smarter decision!
 >  before making everything 3d rotate the y axis so it become front, back!
 >  fix the issue when "there are no vectors to keep me inside"!!!




05-01-2018
Important Questions to Answer!

>   When I have equal conflicts with two of my neighbor which one to get away from?
>   When two directions to get away from a neighbor/conflict, which one to choose?
    - what kind of evaluation will tell me to go down or right?
    - is it a future evaluation?
    - The system is still a bottom-up system in terms that every agent evaluates
      his state locally without being able to look at the envelope as a whole..
      no global evaluation of his position.. but the agent also is a smart one..
      so among all the possible steps it can take it should be able to take the best
      LOCAL DESCISION!
    - but is this 'local decision' based only on his current situation in this
      time frame or it should be able to see one step into the future to evaluate
      what is the best NEXT MOVE for the future instead of the best next move to
      solve current problems..??
    - or it can be both together? based on the current situation evaluation the
      agent figures out that it needs to update its position.. but there should be
      an evaluation of the new position it should take.. in two way:
            - 1 - if I have two vectors/directions to move which one is better
            - 2 - is the proposed position - based on the best movement vector -
                  is better than my current position or not?
                  if it wasn't better than my current position what happens?


_______
[ ] Solve the issue with moving inside position!
[ ] Prevent persons from leaving the envelope! at least 'need' cells
[ ] Make only one of the people move? not both?
[ ] Add intentional movement
[ ] Intentional movement cell value is 2, to allocate cells accordingly when placing people
[ ] SHARING AND NEGOTIATION :D

[ ] Compare Satisfaction rates between running the solver every 5 mins and every min
[ ] You can't leave the vector neighbors move accordingly random!! :|


[ ] Fix the relation between self.x, self.y and self.position!

[ ] When the system is in 'equilibrium' output a state of the machine?

>>> when a conflict happen because one person changed activity the cell should go to the one
    that didn't change first?


>>> some initial positions reduce the number of conflicts that will happen later!
    look for them!


TO-DO LIST:

[ ] VISUALIZATION: color by person? color by activity? or both
[ ] Satisfaction Evaluation
[ ] Rewrite pattern classes into dictionaries and rewrite the way Perosn reads them
[ ] movement types: intentional : not-intentional
[ ] change in activity when someone leaves the building?
[ ] find the best way to leave the building! least effort path! :( don't know how!)
[ ] finding a good way to define initial positons based on people analysis!!!

[√] a function that from a list of vectors returns the most needed one!!!



_________________________________
_________________________________

NOTES

[1]

> do I need a class to run people and envelope at the same time?
> because I need each one to be an input for the other
> how do we do that?

class Run:
    def __init__(envelope, people):
        pass?
        # how does this work

[2]

>   the output of the Run function should be 'states of the machine'
    in every time frame.. this is - the envelope with its cells,
                                  - the people (positions, claimed_cells, etc)


[3]

>   person class should add a person to envelope.people?
    what is the right order for doing so?
    who comes first? the envelope or the person classes?

>>> We can define self.people in Envelope class within the function
    place_people(people)
    this means the other functions using people should come after


[4]

>   when we place_people in the Envelope we make them claim cells based on their
    current position in the envelope
    the decision to change this position is based on their evaluation of what they claimed
    so updating the position or movement happens in Person Class

    the Run script structure should be like:

    for the first time:
    # envelope defined outside
    # people defined outside

    for t in range(time):
        # this is the Envelope part of the job! placing people
        # when we place people within the envelope we change its attributes
        # like the states of the cells and who's occupied and who's not
        # so we need to output this new machine state of the envelope

        e.place_people(people)
        [OUTPUT] = e

        # WHEN DO WE OUTPUT PEOPLE?
        [OUTPUT] = people      # here? or after updating position?
                               # updating position should be useful for next iteration
                               # figure out the correct order of outputting stuff

        for person in people:
            # Update ACTIVITY based on time
            # Update the POSITION based on:
                evaluating the position based on what they claimed
                evaluate if there is a desired position or targeted movement



        ########## THE TIME CAN BE 5*288
        ########## we change activity every five mins | Update Activity
        ########## but we move every min?             | Update Position
        ########## how this can be usefull?
                   in avoiding future conflicts or starting the activity without
                   conflict? I am not sure if this will work or not


[5]

>   Visualization:
    there are two options to visualize cells!
    1. based on the envelope and what cells are allocated and what in conflict
    2. based on every person and his claimed cells and cells in conflict

    are e.cells_in_conflict identical with ALL person.conflicts?
    This is a very important question
    may help solving the delay in the conflict rendering!


    in the allocated cells save the person this cell went to!!


[6]

>   the task of Enveleope class is to allocate cells
    what happens in the next time iteration?
    we refresh everything so all the cells are zero again?
    or we keep a memory for the building
    so it know what its previous state was and decides something according to that
    or this is done by the people?
    # the Envelope has no memory.. it just


[7]

>  notes about changing person. need_centers(), desire_center(), all_centers(), claimed_centers()
        #______________ there's a repeating patterns in these Functions
                      # how to rewrite them in more effecient way?

            # IMPORTANT: these functions differentiate between needs and desire cells
            # in the activity matrix we're reading from the activity group!

            # they all return 3D points.. maybe we can make them return the positions
            # only to avoid confusion with the other functions
            # should these return positions and stay within the person class?
            # I think so!!!!!
            # these are not part of the visualization but part of the person himself!

            # so when we use the General Function with these we will have something like:
            # voxelize(person.need_centers())
            # rename them from centers to cells or positions?
            # they will return positions but it's better to call them cells?


[8]

>  # initiating an attributes for person called need within a function called need!
        # the problem with initiateing an attribute within a method and not inside __init__
        # is the fact that you need to run this function first to create the attribute!
        # so the attribute is useless without the function itself!

        # don't you ever call a function and an attribute with the same name!!
        # specially when you create the attribute within the function
        # like what you're doing here!
        # if you called to attribute before the function it will return the method name
        # if you called the function the first time and the attribute was initiated
        # you can't call the function again because the attribute took it's name
        # in this case this is the Error returned:
        # TypeError: 'list' object is not callable
        # because the attribute was a list and I put () after it to call the function

[9]

>  [Summary]?
    The roles of the classes!
    * Envelope : takes people with certain positions and activities and tries to place them
                 by allocating its cells based on these people's priorities

    * Person   : evaluates what is given to him by the Envelope in relation to what he
                 needs or wants and thus behave according to that!
                 The two main behaviours of a person:
                 - Updating Activity: based on his schedule
                 - Updating Pisitions: based on Satisfaction

"""

#___________________________________________________#
#printouts


envelope.claimed_cells_readable()
# returns:
# a dictionary inside dictionary
key           :  value
cell.position :  { person1.name: claiming_value, person2.name: claiming_value }

{(0, 3): {'John': 1}, (0, 4): {'John': 1}, (1, 2): {'John': 2}, (1, 3): {'John': 2}, (1, 4): {'John': 2}, (1, 6): {'Maya': 1}, (2, 2): {'John': 2}, (2, 3): {'John': 2}, (2, 4): {'John': 2}, (2, 5): {'Maya': 2}, (2, 6): {'Maya': 2, 'Hadi': 1}, (2, 7): {'Maya': 2, 'Hadi': 1}, (3, 2): {'John': 2}, (3, 3): {'John': 2}, (3, 4): {'John': 2}, (3, 5): {'Maya': 2, 'Hadi': 2}, (3, 6): {'Maya': 2, 'Hadi': 2}, (3, 7): {'Maya': 2, 'Hadi': 2}, (3, 9): {'Reem': 1}, (4, 2): {'John': 2}, (4, 4): {'John': 2}, (4, 5): {'John': 2, 'Maya': 2, 'Hadi': 2}, (4, 6): {'Maya': 2, 'Hadi': 2}, (4, 7): {'Maya': 2, 'Hadi': 2}, (4, 8): {'Reem': 2}, (4, 9): {'Reem': 2}, (5, 4): {'John': 2}, (5, 5): {'Maya': 2, 'Hadi': 2}, (5, 6): {'Maya': 1, 'Hadi': 2}, (5, 7): {'Maya': 2, 'Hadi': 2}, (5, 8): {'Reem': 2}, (5, 9): {'Reem': 2}, (6, 5): {'Hadi': 2}, (6, 7): {'Hadi': 2}, (6, 8): {'Hadi': 2, 'Reem': 2}, (6, 9): {'Reem': 2}, (7, 7): {'Hadi': 2}, (7, 8): {'Reem': 2}}
#___________________________________________________


envelope.cells_in_conflict_readable()
# returns:
key           :  value
cell.position : [conflict_value, [list of people in conflict ] ]

{(3, 5): [2, ['Maya', 'Hadi']], (3, 6): [2, ['Maya', 'Hadi']], (3, 7): [2, ['Maya', 'Hadi']], (4, 5): [2, ['John', 'Maya', 'Hadi']], (4, 6): [2, ['Maya', 'Hadi']], (4, 7): [2, ['Maya', 'Hadi']], (5, 5): [2, ['Maya', 'Hadi']], (5, 7): [2, ['Maya', 'Hadi']], (6, 8): [2, ['Hadi', 'Reem']]}
#___________________________________________________
envelope.cells_in_conflict()

{<Envelope_Cell.Envelope_Cell object at 0x105c56cf8>: [2, [<Person.Person object at 0x105c5eba8>, <Person.Person object at 0x105c5ec18>]], <Envelope_Cell.Envelope_Cell object at 0x105c56d30>: [2, [<Person.Person object at 0x105c5eba8>, <Person.Person object at 0x105c5ec18>]], <Envelope_Cell.Envelope_Cell object at 0x105c56f28>: [2, [<Person.Person object at 0x105c5eba8>, <Person.Person object at 0x105c5ec18>]], <Envelope_Cell.Envelope_Cell object at 0x105c56f60>: [2, [<Person.Person object at 0x105c5eba8>, <Person.Person object at 0x105c5ec18>]]}

#___________________________________________________

envelope.allocated_cells_readable()
# returns:
key           :  value
cell.position : [status, the_name_of_person_it_went_to ]

{(0, 3): ['Without Conflict', 'John'], (0, 4): ['Without Conflict', 'John'], (1, 2): ['Without Conflict', 'John'], (1, 3): ['Without Conflict', 'John'], (1, 4): ['Without Conflict', 'John'], (1, 6): ['Without Conflict', 'Maya'], (2, 2): ['Without Conflict', 'John'], (2, 3): ['Without Conflict', 'John'], (2, 4): ['Without Conflict', 'John'], (2, 5): ['Without Conflict', 'Maya'], (2, 6): ['Overruled', 'Maya'], (2, 7): ['Overruled', 'Maya'], (3, 2): ['Without Conflict', 'John'], (3, 3): ['Without Conflict', 'John'], (3, 4): ['Without Conflict', 'John'], (3, 9): ['Without Conflict', 'Reem'], (4, 2): ['Without Conflict', 'John'], (4, 4): ['Without Conflict', 'John'], (4, 8): ['Without Conflict', 'Reem'], (4, 9): ['Without Conflict', 'Reem'], (5, 4): ['Without Conflict', 'John'], (5, 6): ['Overruled', 'Hadi'], (5, 8): ['Without Conflict', 'Reem'], (5, 9): ['Without Conflict', 'Reem'], (6, 5): ['Without Conflict', 'Hadi'], (6, 7): ['Without Conflict', 'Hadi'], (6, 9): ['Without Conflict', 'Reem'], (7, 7): ['Without Conflict', 'Hadi'], (7, 8): ['Without Conflict', 'Reem']}

#___________________________________________________

for person in people_classes:
    print(person.conflicts)

key           :  value
cell.position :  conflict_value

{(4, 5): 2}
{(3, 5): 2, (3, 6): 2, (3, 7): 2, (4, 5): 2, (4, 6): 2, (4, 7): 2, (5, 5): 2, (5, 7): 2}
{(3, 5): 2, (3, 6): 2, (3, 7): 2, (4, 5): 2, (4, 6): 2, (4, 7): 2, (5, 5): 2, (5, 7): 2, (6, 8): 2}
{(6, 8): 2}

#___________________________________________________
