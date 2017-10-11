from StateHandler import StateHandler


# TODO Retailer Statehandler
class Retailer(StateHandler):
    StateHandler.__init__(self, Retailer.start, [], Quit, gamedata)