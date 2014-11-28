#-------------------------------------------------------------------------------
# Name:        display.py
#
# Purpose:     Display interface for outputting data
#
# Author:      Willie Boag
#-------------------------------------------------------------------------------


class Display:

    def __init__(self):
        raise Exception('cannot instantiate Display base class')

    def displayValues(self, agent, state, message):
        raise Exception('must overload Display::displayValue() in derived class')

    def pause(self):
        raise Exception('must overload Display::pause() in derived class')


