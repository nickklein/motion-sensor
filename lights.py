from phue import Bridge
from app import config

class Lights():

    def __init__(self):
        self.bridge = Bridge(config['BRIDGE_IP'])
        self.bridge.connect()

    def turn_on(self, lights):
        self.bridge.set_light(lights, 'on', True)

    def turn_off(self, lights):
        self.bridge.set_light(lights, 'on', False)