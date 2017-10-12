from StateHandler import StateHandler


class Druid(StateHandler):
    StateHandler.__init__(self, Druid.start, [], Quit, gamedata)
