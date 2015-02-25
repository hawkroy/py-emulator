import sys
from simparse import *

class Emulator(object):
    def __init__(self, name='Emulator', resource={}, parameter={}, entity_list=[]):
        print name
        self.name = name
        self.resource = resource
        self.parameter = parameter
        self.state = HALT
        self.entity_list = entity_list

    def sim_tick(self, entity):
        pass

    def run(self):
        while(self.state == HALT):
            if (self.state == REBOOT):
                re_init()
            for e in self.entity_list:
                e.run()

    def re_init(self):
        pass

class Entity(object):
    def __init__(self, name='entity', emulator = None):
        self.name = name
        self.emulator = emulator
        self.pc = 0
        self.prog = []
    
    def run(self):
        emulator.sim_tick(self.prog[self.pc])

def test():
    prog = None
    resource = {}
    parameter = {}
    entity = []

    if len(sys.argv) == 2:
        data = open(sys.argv[1]).read()
        prog = parse(data, debug=0)

    if prog != None:
        for item in prog:
            if 'PARAMETER' in item:

            if 'RESOURCE' in item:
                print item['RESOURCE']
            if 'ENTITY' in item:
                print item['ENTITY']

if __name__ == "__main__":
    test()
